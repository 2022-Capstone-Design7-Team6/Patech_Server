from rest_framework import serializers
from users.serializers import ProfileSerializer
from .models import Plant,Photo

class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = ("pk","plant_name","plant_species","start_date","water_date") 

class PlantCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = ("plant_name","plant_species","start_date","water_date") 

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ("pk","plant_id","image","text","date") 

class PhotoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ("plant_id","image","text","date") 