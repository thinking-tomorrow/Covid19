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

class News(models.Model):
    heading = models.CharField(max_length=100)
    body = models.TextField()
    link = models.TextField()
    img = models.ImageField()
    date = models.DateField()

    class Meta:
        verbose_name_plural = "news"
