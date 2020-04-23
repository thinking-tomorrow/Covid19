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

class News(models.Model):
    heading = models.CharField(max_length=50)
    body = models.TextField()
    img = models.ImageField()
    date = models.DateField()

    class Meta:
        verbose_name_plural = "news"

