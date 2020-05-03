from django.contrib import admin
from .models import CountryData, News, CountryNews, DailyData

admin.site.register(CountryData)
admin.site.register(News)
admin.site.register(CountryNews)
admin.site.register(DailyData)