from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Price(models.Model):
    species = models.IntegerField(primary_key=True)
    price = models.IntegerField(default=0)
    date = models.DateField(default=timezone.now)
class Plant(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name = 'plants') # 작성자
    plant_name = models.CharField(max_length=20) # 식물 닉네임
    plant_species = models.IntegerField() # 식물종 0:대파,1:양파, 2:쪽파
    start_date =models.DateTimeField(default=timezone.now) # 등록 날짜
    water_date = models.DateTimeField(null=True) # 최근 물 준 날짜
    harvest_date = models.DateTimeField(null=True) # 수확 예상 시기
    harvest_weight = models.FloatField(default=0)#수확예상무게
    pot_image = models.ImageField(upload_to ='post/',null=True)
    pot_size = models.FloatField(default=20) # 화분 사이즈
    pot_ratio = models.FloatField(default=0.4)# 초기 화분 비율

    class Meta:
        ordering = ["-start_date"]
class Photo(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True) # 작성자
    plant = models.ForeignKey(Plant,on_delete=models.CASCADE,related_name = 'plants') # 식물 정보
    image = models.ImageField(upload_to ='post/',null=True) # 사진 
    beforeimage = models.ImageField(upload_to ='post/',null=True) # 사진 
    text = models.CharField(max_length=200,null=True) # 문자
    date = models.DateTimeField(default=timezone.now) # 날짜
    event_water = models.BooleanField(default=False)
    event_harvest = models.BooleanField(default=False)
    event_chgpot = models.BooleanField(default=False)
    size = models.FloatField(default=0) # 계산 면적
    length = models.FloatField(default=0) #계산 길이
    weight = models.FloatField(default=0) #계산 무게
    class Meta:
        ordering = ['-date']

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Plant)
def create_plant(sender, instance, created, **kwargs):
    if created:
        Photo.objects.create(plant=instance,author=instance.author,image=instance.pot_image)

# Create your models here.
