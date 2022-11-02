from django.urls import path
from rest_framework import routers
from .views import PlantViewSet, PhotoViewSet

router = routers.SimpleRouter()
router.register('plants',PlantViewSet)
router.register('photos',PhotoViewSet)
urlpatterns= router.urls