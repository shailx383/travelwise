from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class s1(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    people=models.CharField(max_length=4)
    type=models.CharField(max_length=3)
    city=models.CharField(max_length=100)
    country = models.CharField(max_length=100)

class city(models.Model):
    city_code=models.IntegerField(primary_key=True)
    country=models.CharField(max_length=100)
    city_name = models.CharField(max_length=100)
    currency=models.CharField(max_length=100)
    continent=models.CharField(max_length=100)
    weather=models.CharField(max_length=3)

class attractions(models.Model):
    attract_id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=100)
    city=models.ForeignKey(city, to_field="city_code", on_delete=models.CASCADE)
    cost = models.IntegerField()
    type = models.CharField(max_length=3)
    time = models.CharField(max_length=3)
    desc = models.TextField(max_length=250)

class s2(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    weather = models.CharField(max_length=3)
    start_date = models.DateField()
    budget = models.CharField(max_length=3)

class s3(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    rooms = models.IntegerField()
    ppl = models.IntegerField()
    type = models.CharField(max_length=9)

class s4(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    tran = models.CharField(max_length=4)

