from django.db import models
# Create your models here.
class User(models.Model):
    username=models.CharField(max_length=18,primary_key=True)
    passwd=models.CharField(max_length=16)
    phno=models.CharField(max_length=10)
    email=models.EmailField(max_length=254)
    name=models.CharField(max_length=30)
