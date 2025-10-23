from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *

# Роутер для ViewSet'ов
router = DefaultRouter()
router.register(r"places", PlaceView, basename="places")
router.register(r"photos", PhotoView, basename="photos")

urlpatterns = [
    # JWT авторизация
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # FeatureCollection
    path("places/geojson/", PlacesGeoJSONView.as_view(), name="places_geojson"),

    # Подключаем все маршруты роутера
    path('', include(router.urls)),
]
