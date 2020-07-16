from django.db import models
# from django.contrib.auth.models import User
# Create your models here.
import json

class Employee(models.Model):
    rank = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    count = models.IntegerField()
    median = models.IntegerField()

    def __str__(self):
        return self.name





