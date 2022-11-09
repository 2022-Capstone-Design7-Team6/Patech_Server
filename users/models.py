from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user= models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    nickname = models.CharField(max_length=20,default="Unknown")
    depa_weight = models.FloatField(default=0)
    jjokpa_weight = models.FloatField(default=0)
    onion_weight = models.FloatField(default=0)

@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwangs):
    if created:
        Profile.objects.create(user=instance)

