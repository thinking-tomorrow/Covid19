from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
<<<<<<< HEAD
    path('',        views.home, name='home'),
    path('news',    views.news, name='news'),
    path('country', views.country, name='country'),
    path('country/<str:country_name>', views.country),
    path('world',   views.world, name='world')
]
=======
    path('',views.home, name='home'),
    path('news',views.news, name='news')
]

>>>>>>> 673e31d9c1ef36bdd6f547deaf4c6ffb75d0385f
