from django.shortcuts import render
from django.http import HttpResponse
from .models import News

def home(request):
    return render(request, 'home.html')

def news(request):
    latest = News.objects.all()
    return render(request, 'news.html', {'latest': latest})

def country(request, country_name='all'):
    return render(request, 'country.html', {'country': country_name})

def world(request):
    return render(request, 'world.html')