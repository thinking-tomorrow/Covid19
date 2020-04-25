from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',        views.home, name='home'),
    path('news',    views.news, name='news'),
    path('country', views.country, name='country'),
    path('country/<str:country_name>', views.country, name='country'),
    path('world',   views.world, name='world'),
    path('tips',views.tips,name='tips')
]