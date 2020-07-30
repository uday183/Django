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

#Aggregations

class Author(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    class Meta:
        verbose_name_plural = '1.Author'

    def __str__(self):
        return self.name

class Publisher(models.Model):
    name = models.CharField(max_length=300)
    class Meta:
        verbose_name_plural = '2.Publisher'
    def __str__(self):
        return self.name

class Books(models.Model):
    name = models.CharField(max_length=300)
    pages = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField()
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    pubdate = models.DateField()

    class Meta:
        verbose_name_plural = '3.Books'
        ordering = ["name"]
    def __str__(self):
        return self.name

class Store(models.Model):
    name = models.CharField(max_length=300)
    books = models.ManyToManyField(Books)

    class Meta:
        verbose_name_plural = '4.Store'
    def __str__(self):
        return self.name