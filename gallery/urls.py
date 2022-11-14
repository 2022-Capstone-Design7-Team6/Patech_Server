from django.urls import path, include
from rest_framework import routers
from .views import PlantViewSet, PhotoViewSet,homepage,\
    PlantPageAPIVIEW,plantlist,PatechRank,harvest

router = routers.SimpleRouter()
router.register('plants',PlantViewSet)
router.register('photos',PhotoViewSet)


urlpatterns = [
    path('homepage/',homepage),
    path('plantlist/',plantlist),
    path('rank/',PatechRank.as_view()),
    path('plantpage/',PlantPageAPIVIEW.as_view()),
    path('harvest/',harvest),
    # path('plantpage/',plantpage),
    path('',include(router.urls)),
]