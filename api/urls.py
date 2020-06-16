from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('api/india', views.india, name='india'),
    path('api/india/<str:state_name>',views.state,name='state')
]