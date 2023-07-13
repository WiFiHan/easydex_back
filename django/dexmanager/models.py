from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class SrcDex(models.Model):
    #Refer Post class of our Seminar
    title = models.CharField(max_length=256)
    values = models.JSONField()
    watching_users =  models.ManyToManyField(User, blank=True, related_name='watching_dex', through='UserDex')


class UserDex(models.Model):
    #Refer Like class of our Seminar
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    srcDex = models.ForeignKey(SrcDex, on_delete=models.CASCADE)
    added_at = models.DateTimeField(default=timezone.now)
