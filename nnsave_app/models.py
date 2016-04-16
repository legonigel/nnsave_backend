from django.contrib.gis.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)

class Location(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=13)
    website = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
