from django.db import models

# Create your models here.
class Index(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()

    def __str__(self):
        return self.title