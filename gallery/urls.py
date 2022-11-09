from django.urls import path, include
from rest_framework import routers
from .views import PlantViewSet, PhotoViewSet,homepage,PlantPageAPIVIEW,plantlist

router = routers.SimpleRouter()
router.register('plants',PlantViewSet)
router.register('photos',PhotoViewSet)


urlpatterns = [
    path('homepage/',homepage),
    path('plantlist/',plantlist),
    path('plantpage/',PlantPageAPIVIEW.as_view()),
    # path('plantpage/',plantpage),
    path('',include(router.urls)),
]