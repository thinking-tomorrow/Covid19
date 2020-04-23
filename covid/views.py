from django.shortcuts import render

from django.http import HttpResponse, Http404

def home(request):
    return render(request, 'home.html')

def news(request):
    return render(request, 'news.html')

def country(request, country_name='all'):
    return render(request, 'country.html', {'country': country_name})
    # return render(request, 'country.html')

def world(request):
    return render(request, 'world.html')
