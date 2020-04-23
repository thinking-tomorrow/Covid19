from django.contrib import admin
from .models import CountryData, News

admin.site.register(CountryData)
admin.site.register(News)