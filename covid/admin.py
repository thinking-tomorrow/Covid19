from django.contrib import admin
from .models import CountryData, News, CountryNews

admin.site.register(CountryData)
admin.site.register(News)
admin.site.register(CountryNews)