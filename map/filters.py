import django_filters
from .models import Place

# фильтр по границам карты
# /api/places/?min_lat=55.7&max_lat=55.9&min_lng=37.5&max_lng=37.7
# вернёт все точки в этом прямоугольнике
class PlaceFilter(django_filters.FilterSet):
    min_lat = django_filters.NumberFilter(field_name="latitude", lookup_expr="gte")
    max_lat = django_filters.NumberFilter(field_name="latitude", lookup_expr="lte")
    min_lng = django_filters.NumberFilter(field_name="longitude", lookup_expr="gte")
    max_lng = django_filters.NumberFilter(field_name="longitude", lookup_expr="lte")

    class Meta:
        model = Place
        fields = ["min_lat", "max_lat", "min_lng", "max_lng"]