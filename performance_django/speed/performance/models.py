from django.db import models
import uuid


#https://realpython.com/create-django-index-without-downtime/
# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=120,null=True,blank=True)
    place = models.CharField(max_length=120,null=True,blank=True)
    country = models.CharField(max_length=120,null=True,blank=True)
    serial_number = models.UUIDField(default=uuid.uuid4, db_index=True)

    def __str__(self):
        return self.name