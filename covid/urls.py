from django.contrib import admin
from django.urls import path,include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'countrydata', views.CountryDataViewSet)
router.register(r'dailydata', views.DailyDataViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('news', views.news, name='news'),
    path('news-detail/<int:news_id>', views.news_detail, name='news'),
    path('country', views.country, name='country'),
    path('country/<str:country_name>', views.country_detail, name='country'),
    path('world', views.world, name='world'),
    path('tips', views.tips,name='tips'),
    path('search', views.search,name='search'),
    #path('searchcountries',views.searchcountries, name='searchcountries'),
    path('about',views.about,name='about'),
    path('graphs',views.graphs,name='graphs'),
    path('india',views.india, name="india"),
    path('india/<str:state_name>',views.state,name="india"),
    path('api', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]