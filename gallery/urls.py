from django.urls import path, include
from rest_framework import routers
from .views import PlantViewSet, PhotoViewSet,homepage,\
    PlantPageAPIVIEW,plantlist,PatechRank,harvest,getphotos,plantnamecheck\
        ,nicknamecheck,calchavestdate,updateallhdate

router = routers.SimpleRouter()
router.register('plants',PlantViewSet)
router.register('photos',PhotoViewSet)


urlpatterns = [
    path('homepage/',homepage),
    path('plantlist/',plantlist),
    path('rank/',PatechRank.as_view()),
    path('plantpage/<int:plant_id>',PlantPageAPIVIEW.as_view()),
    path('harvest/',harvest),
    path('getphotos/<int:plant_id>',getphotos),
    path('plantnamecheck/',plantnamecheck),
    path('nicknamecheck/',nicknamecheck),
    path('calchavestdate/',calchavestdate),
    path('updateallhdate/',updateallhdate),
    # path('plantpage/',plantpage),
    path('',include(router.urls)),
]