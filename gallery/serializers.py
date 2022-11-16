from rest_framework import serializers
from users.serializers import ProfileSerializer
from .models import Plant,Photo,Price
from django.utils import timezone


class Base64ImageField(serializers.ImageField):   

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

       
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')           
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')
            
            file_name = str(uuid.uuid4())[:12] 
           
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension



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
    image = Base64ImageField(
        max_length=None, use_url=True, required=False
    )
    class Meta:
        model = Photo
        fields = "__all__" 

class SimplePhotoSerializer(serializers.ModelSerializer):
    # plant= PlantSerializer(read_only=True)
    my_date = serializers.SerializerMethodField('removetime')
    def removetime(self, photo):
      return photo.date.date() 
    class Meta:
        model = Photo
        fields = ("image","my_date") 


class PhotoCreateSerializer(serializers.ModelSerializer):
    plant= PlantSerializer(read_only=True)
    class Meta:
        model = Photo
        fields = ("plant","image","text","event_water","event_harvest","event_chgpot","date","size","length","weight")


class BPhotoCreateSerializer(serializers.ModelSerializer):
    plant = PlantSerializer(read_only=True)
    beforeimage = Base64ImageField(
        max_length=None, use_url=True, required=False,source="image"
    )
    class Meta:
        model = Photo
        fields = ("plant","beforeimage","text","event_water","event_harvest","event_chgpot","date","size","length","weight")

class APhotoCreateSerializer(serializers.ModelSerializer):
    plant = PlantSerializer(read_only=True)
    afterimage = Base64ImageField(
        max_length=None, use_url=True, required=False,source="image"
    )
    class Meta:
        model = Photo
        fields = ("plant","afterimage","text","event_water","event_harvest","event_chgpot","date","size","length","weight")


class PhotoTimelineSerializer(serializers.ModelSerializer):
    # plant= PlantSerializer(read_only=True)
    class Meta:
        model = Photo
        fields = ("pk","image","event_water","event_harvest","event_chgpot","text","date") 


class HomePage_PlantSerializer(serializers.ModelSerializer):

    d_day= serializers.SerializerMethodField(method_name="CalDate")
    class Meta:
        model = Plant
        fields = ("pk","plant_name","plant_species","d_day","harvest_date") 
    def CalDate(self,obj):
        return (timezone.now()-obj.start_date).days 


class PlantPage_PlantSerializer(serializers.ModelSerializer):

    start_date = serializers.SerializerMethodField(method_name='removetime')
    d_day= serializers.SerializerMethodField(method_name="CalDate")
    class Meta:
        model = Plant
        fields = ("pk","plant_name","plant_species","start_date","d_day","harvest_date") 
    def CalDate(self,obj):
        return (timezone.now()-obj.start_date).days 
    def removetime(self, obj):
      return obj.start_date.date() 

class RecentPlantSerializer(serializers.ModelSerializer):
    plant = HomePage_PlantSerializer(read_only=True)
    class Meta:
        model = Photo
        fields = ("pk","plant","image",)



class GraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ("date","size","length","weight","event_water","event_harvest","event_chgpot")


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