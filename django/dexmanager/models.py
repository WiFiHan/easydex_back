from django.db import models

# Create your models here.
class Dex(models.Model):
    title = models.CharField(max_length=256)
    values = models.JSONField()