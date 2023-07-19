from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import json

# Create your models here.
class SrcDex(models.Model):
    #Refer Post class of our Seminar
    title = models.CharField(max_length=256)
    closing = models.CharField(max_length=256, default="1000")
    values = models.JSONField(null=True, blank=True)
    watching_users = models.ManyToManyField(User, blank=True, related_name='watching_dex', through='UserDex')
    updated_at = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True)
    tags = models.JSONField(blank=True, null=True, default={'1': 123, '2': 342, '3': 152})
    category = models.CharField(max_length=256, blank=True)
    isInvest = models.BooleanField(default=True)
    url = models.URLField(blank=True)

    


    def get_list(self):
        if self.tags:
            return json.loads(self.tags)
        return []

    def set_list(self, value):
        self.tags = json.dumps(value)

class UserDex(models.Model):
    #Refer Like class of our Seminar
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    srcDex = models.ForeignKey(SrcDex, on_delete=models.CASCADE)
    added_at = models.DateTimeField(default=timezone.now)
