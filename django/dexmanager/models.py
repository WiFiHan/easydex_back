from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class SrcDex(models.Model):
    #Common fields for investing Dexes and economic Dexes
    title = models.CharField(max_length=256)
    values = models.JSONField(null=True, blank=True)
    watching_users = models.ManyToManyField(User, blank=True, related_name='watching_dex', through='UserDex')
    updated_at = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True)
    tags = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=256, blank=True)
    isInvest = models.BooleanField(default=True)
    category = models.CharField(max_length=256, null=True)

    # for economic Dexes
    unit = models.CharField(max_length=256, null=True)
    period = models.CharField(max_length=64, null=True)

    # for investing Dexes
    reduced_title = models.CharField(max_length=64, null=True)
    closing = models.CharField(max_length=256, null=True)
    description = models.TextField(blank=True, null=True)
    url = models.URLField(null=True, blank=True)
    search_keyword = models.JSONField(null=True, blank=True)

class HankyungTitle(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField(blank=True)
    updated_at = models.DateTimeField(default=timezone.now)

class UserDex(models.Model):
    #Refer Like class of our Seminar
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    srcDex = models.ForeignKey(SrcDex, on_delete=models.CASCADE)
    added_at = models.DateTimeField(default=timezone.now)
