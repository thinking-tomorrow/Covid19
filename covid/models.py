from django.db import models

class CountryData(models.Model):
    name = models.TextField()
    totalcase = models.IntegerField()
    activecase = models.IntegerField()
    newcase = models.IntegerField()
    deaths = models.IntegerField()
    newdeath = models.IntegerField()
    recovered = models.IntegerField()
    tests = models.IntegerField()
