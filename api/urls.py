from django.contrib import admin
from django.urls import path,include
from . import views

# from rest_framework import routers


# router = routers.DefaultRouter()
# router.register(r'countrydata', views.CountryDataViewSet)
# router.register(r'dailydata', views.DailyDataViewSet)

urlpatterns = [

    path('api/india', views.india, name='india'),

    # path('api', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]