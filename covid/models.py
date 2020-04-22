from django.db import models

class Data(models.Model):
    totalcase = models.IntegerField()
    activecase = models.IntegerField()
    newcase = models.IntegerField()
    deaths = models.IntegerField()
    newdeath = models.IntegerField()
    recovered = models.IntegerField()
    tests = models.IntegerField()
