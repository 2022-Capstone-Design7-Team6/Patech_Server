from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Plant(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name = 'plants')
    plant_name = models.CharField(max_length=20)
    plant_species = models.IntegerField()
    start_date =models.DateTimeField(default=timezone.now)
    water_date = models.DateTimeField(null=True)


class Photo(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    plant_id = models.ForeignKey(Plant,on_delete=models.CASCADE,related_name = 'photos')
    image = models.ImageField(upload_to ='post/',default='default.png')
    text = models.CharField(max_length=50,null=True)
    date = models.DateTimeField(default=timezone.now)


# Create your models here.
