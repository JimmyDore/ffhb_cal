# Create your models here.
from django.db import models

class Club(models.Model):
    url = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    #Examples of model fields
    #models.DateTimeField('date published')
    #models.ForeignKey(Question, on_delete=models.CASCADE)
    #models.CharField(max_length=200)
    #models.IntegerField(default=0)
