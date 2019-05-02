from django.db import models

# Create your models here.

class Address(models.Model):
    pin = models.CharField(max_length=50)

class UserDetails(models.Model):
    name = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    address = models.ManyToManyField(Address)

    def __str__(self):
        return self.name