from rest_framework import serializers
from users.serializers import ProfileSerializer
from .models import Plant,Photo,Price
from django.utils import timezone


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ("species", "price","date")
class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = ("pk","plant_name","plant_species","start_date","water_date","harvest_date","pot_size","pot_ratio") 

class PlantCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plant
        fields = ("plant_name","plant_species","start_date","water_date","pot_size","pot_ratio") 

class PhotoSerializer(serializers.ModelSerializer):
    # plant= PlantSerializer(read_only=True)
    class Meta:
        model = Photo
        fields = ("pk","plant","image","event","text","date","size","length","weight") 

class PhotoCreateSerializer(serializers.ModelSerializer):
    plant= PlantSerializer(read_only=True)
    class Meta:
        model = Photo
        fields = ("plant","image","text","event","date","size","length","weight")


class BPhotoCreateSerializer(serializers.ModelSerializer):
    plant = PlantSerializer(read_only=True)
    beforeimage = serializers.ImageField(source="image",required=True)
    class Meta:
        model = Photo
        fields = ("plant","beforeimage","text","event","date","size","length","weight")

class APhotoCreateSerializer(serializers.ModelSerializer):
    plant = PlantSerializer(read_only=True)
    afterimage = serializers.ImageField(source="image",required=True)
    class Meta:
        model = Photo
        fields = ("plant","afterimage","text","event","date","size","length","weight")


class PhotoTimelineSerializer(serializers.ModelSerializer):
    # plant= PlantSerializer(read_only=True)
    class Meta:
        model = Photo
        fields = ("pk","image","event","text","date") 


class HomePage_PlantSerializer(serializers.ModelSerializer):

    d_day= serializers.SerializerMethodField(method_name="CalDate")
    class Meta:
        model = Plant
        fields = ("pk","plant_name","plant_species","d_day","harvest_date") 
    def CalDate(self,obj):
        return (timezone.now()-obj.start_date).days 

class RecentPlantSerializer(serializers.ModelSerializer):
    plant = HomePage_PlantSerializer(read_only=True)
    class Meta:
        model = Photo
        fields = ("pk","plant","image",)

class GraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ("date","size","length","weight","event")


# 가장 최근 식물 2개
# 최근 시세 (시세 가져온 일자, 가격)
# user nickname
# 파테크 지표 (ex) “치킨 한 마리”
 
# 파 리스트 - (최대5개) 사용자가 최근에 일지를 등록한 순/
# 카테고리(대파, 양파, 쪽파)/
# 파 이름/
# 식물 이미지 (가장 최근에 촬영한 사진)/
# D+80 정보(int)/
# 수확예정 정보/