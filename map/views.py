# views.py

from django.shortcuts import render
from .serializers import *
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drf_spectacular.utils import extend_schema, OpenApiResponse, inline_serializer
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .filters import *

def index(request):
    # стартовая страница
    return render(request, "map/index.html")

# TODO PlaceView
@extend_schema(
    tags=["places"],
    responses={200: PlaceReadSerializer},
)
class PlaceView(viewsets.ModelViewSet):
    """
    CRUD для мест.
    - GET /api/places/ -> список мест (читательский сериализатор)
    - POST /api/places/ -> создание (писательский сериализатор)
    - GET /api/places/{id}/ -> детально с фото
    """
    queryset = Place.objects.all().order_by("id")
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    # прописываем свой класс фильтрации
    filterset_class = PlaceFilter

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return PlaceReadSerializer
        else:
            return PlaceWriteSerializer


# TODO PhotoView
@extend_schema(
    tags=["photos"],
    responses={200: PhotoReadSerializer},
)
class PhotoView(viewsets.ModelViewSet):
    """
    CRUD для фотографий.
    - хранит файлы через ImageField (MEDIA)
    - отдаёт абсолютные URL для фронтенда
    """
    queryset = Photo.objects.select_related("place").all().order_by("order", "id")
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return PhotoReadSerializer
        else:
            return PhotoWriteSerializer

# TODO PlacesGeoJSONView
@extend_schema(
    tags=["places"],
    responses={
        200: inline_serializer( # FeatureCollection контейнер с полями, это сообщение drf-spectacular о структуре в виде inline_serializer
            name="PlaceFeatureCollection",
            fields={
                "type": serializers.CharField(default="FeatureCollection"),
                "features": PlaceGeoJSONSerializer(many=True),
            }
            # в итоге ответ будет описан корректно
        )
    },
)
class PlacesGeoJSONView(APIView):
    """
    Возвращает FeatureCollection (RFC 7946) для всех Place.

    FeatureCollection - это набор географических объектов (features), объединённых в одну коллекцию.
    Это как контейнер, в котором хранятся разные геообъекты: точки, линии, полигоны и т.д.
    "geometry" — геометрия объекта
    "properties" — произвольные свойства объекта

    Эндпоинт: GET /api/places/geojson/

    пример
    {
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [30.5, 50.5]
      },
      "properties": {
        "name": "Точка интереса"
      }
    },
    {
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[30, 10], [40, 40], [20, 40], [10, 20], [30, 10]]]
      },
      "properties": {
        "name": "Зона покрытия"
      }
    }
  ]
}

    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        places = Place.objects.all()
        features = PlaceGeoJSONSerializer(places, many=True).data
        collection = {
            "type": "FeatureCollection",
            "features": features,
        }
        return Response(collection, status=status.HTTP_200_OK)