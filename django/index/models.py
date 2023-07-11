from django.db import models

# Create your models here.
class Index(models.Model):
    name = models.CharField(max_length=100, default="Dow Jones")
    closing = models.CharField(max_length=100, default="0.00", blank=True, null=True)
    opening = models.CharField(max_length=100, default="0.00", blank=True, null=True)

    def __str__(self):
        return self.title