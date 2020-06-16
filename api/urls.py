from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('api', views.home, name='home'),
    path('api/india', views.india, name='india'),
    path('api/country/<str:country_name>', views.country, name='country'),
    path('api/country/daily/<str:country_name>/<str:date>', views.country_daily, name='country_daily'),
]