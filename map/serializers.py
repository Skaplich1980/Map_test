from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from .models import *

# TODO PhotoSerializer
class PhotoReadSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = Photo
        fields = "__all__"

    # drf-spectacular сообщаем тип возвращаемый для отображения правильного API схемы
    @extend_schema_field(serializers.CharField())
    def get_image_url(self, obj):
        # URL к картинке формирование
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            return request.build_absolute_uri(obj.image.url)
        return None

class PhotoWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ["id", "image", "order", "place", "description"]

    def validate(self, attrs):
        place = attrs.get("place")
        order = attrs.get("order")

        # Проверяем, есть ли уже фото с таким порядком
        if Photo.objects.filter(place=place, order=order).exists():
            # красивое отображение ошибки, если у нас будет введён одинаковый порядок
            raise serializers.ValidationError(
                {"order": f"Для места '{place}' уже существует фото с порядком {order}"}
            )
        return attrs

# TODO PlaceSerializer
class PlaceReadSerializer(serializers.ModelSerializer):
    photos = PhotoReadSerializer(many=True, read_only=True)
    class Meta:
        model = Place
        fields = [
            "id",
            "title",
            "short_desc",
            "long_desc",
            "latitude",
            "longitude",
            "photos",
        ]

class PlaceWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = [
            "title",
            "short_desc",
            "long_desc",
            "latitude",
            "longitude",
        ]

# GeoJSON формируем сериализатором
class PlaceGeoJSONSerializer(serializers.ModelSerializer):
    """
    Сериализатор для представления модели Place в формате GeoJSON (RFC 7946).

    GeoJSON — это стандарт обмена географическими данными на основе JSON.
    Он используется для описания геометрических объектов (точек, линий, полигонов)
    и их свойств. В данном случае каждая локация (Place) представляется как объект
    типа "Feature", содержащий геометрию (координаты точки) и свойства (атрибуты места).

    Возврат в форме:
    {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [<longitude>, <latitude>]
        },
        "properties": {
            "id": <int>,              # Уникальный идентификатор места
            "title": <str>,           # Название локации
            "short_desc": <str>       # Краткое описание
        }
    }

    Поля сериализатора:
    - type: всегда "Feature" (по стандарту GeoJSON).
    - geometry: словарь с типом геометрии ("Point") и координатами [долгота, широта].
    - properties: словарь с дополнительными данными о месте, которые будут использоваться
      фронтендом для отображения информации на карте.

    - Подходит для интеграции с фронтендом, который ожидает данные в формате GeoJSON
      для отрисовки точек на карте.

    Соответствие стандарту:
    - Формат соответствует спецификации RFC 7946 (IETF, 2016).
    - Координаты в порядке [долгота, широта].

    для списка объектов нужно использовать FeatureCollection на уровне вьюшки
    """
    # методы могут меняться в зависимость от согласования с фронтом и дополнительных требований
    type = serializers.SerializerMethodField()
    geometry = serializers.SerializerMethodField() # формирование координат
    properties = serializers.SerializerMethodField() # свойства места, правильно нужно согласовывать с фронтом

    class Meta:
        model = Place
        fields = ["type", "geometry", "properties"]

    def get_type(self, obj):
        return "Feature"

    def get_geometry(self, obj):
        return {
            "type": "Point",
            "coordinates": [obj.longitude, obj.latitude],
        }

    def get_properties(self, obj):
        return {
            "id": obj.id,
            "title": obj.title,
            "short_desc": obj.short_desc,
        }
