from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('news', views.news, name='news'),
    path('news-detail/<int:news_id>', views.news_detail, name='news'),
    path('country', views.country, name='country'),
    path('country/<str:country_name>', views.country_detail, name='country'),
    path('world', views.world, name='world'),
    path('tips', views.tips,name='tips'),
    path('search', views.search,name='search'),
    path('searchcountries',views.searchcountries, name='searchcountries'),
    path('about',views.about,name='about'),
    path('graphs',views.graphs,name='graphs'),
    path('search_date/<str:country>',views.search_date,name='search_date')
]