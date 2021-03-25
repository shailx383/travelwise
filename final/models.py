from django.db import models
from plan1.models import city
# Create your models here.

class acc(models.Model):
    city = models.ForeignKey(city, to_field = "city_code", on_delete = models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.IntegerField()
    cost_per_night = models.IntegerField()

class transport(models.Model):
    id = models.IntegerField(primary_key = True)
    type = models.CharField(max_length = 5)
    name = models.CharField(max_length = 20)
    cost_per_head = models.IntegerField()
    clas = models.CharField(max_length = 12)

class flights(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 50)
    cost_per_head = models.IntegerField()
    clas = models.CharField(max_length = 14)
    country=models.CharField(max_length=100)
