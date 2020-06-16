from django.contrib import admin
from django.urls import path,include
from . import views
import covid.views as view
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'countrydata', view.CountryDataViewSet)
router.register(r'dailydata', view.DailyDataViewSet)

urlpatterns = [

    path('', views.home,name='home'),


]