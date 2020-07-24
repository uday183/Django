from django.db import models

# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=120,null=True,blank=True)
    place = models.CharField(max_length=120,null=True,blank=True)
    country = models.CharField(max_length=120,null=True,blank=True)

    def __str__(self):
        return self.name