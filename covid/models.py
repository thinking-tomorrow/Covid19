from django.db import models

class CountryData(models.Model):
    name = models.TextField(primary_key=True)
    totalcase = models.IntegerField()
    activecase = models.IntegerField()
    newcase = models.IntegerField()
    deaths = models.IntegerField()
    newdeath = models.IntegerField()
    recovered = models.IntegerField()
    tests = models.IntegerField()
    flag = models.ImageField()
    total_pop = models.IntegerField()
    death_pop = models.IntegerField()
    test_pop = models.IntegerField()
    continent = models.TextField()

class News(models.Model):
    heading = models.CharField(max_length=100)
    body = models.TextField()
    link = models.TextField()
    img = models.ImageField()
    date = models.DateField()

    class Meta:
        verbose_name_plural = "news"


class CountryNews(models.Model):
    country = models.CharField(max_length=100)
    title   = models.CharField(max_length=100)
    link    = models.TextField() 
    date    = models.DateField()

    class Meta:
        verbose_name_plural = 'CountryNews'


class DailyData(models.Model):

    country = models.TextField()
    totalcase = models.IntegerField()
    newcase = models.IntegerField()
    deaths = models.IntegerField()
    newdeath = models.IntegerField()
    date = models.DateField()

class Predictions(models.Model):

    date = models.TextField()
    t = models.IntegerField()
    total_prediction = models.IntegerField()
    active_prediction = models.IntegerField()
    recoveries_predicition = models.IntegerField()
    deaths_prediction = models.IntegerField()