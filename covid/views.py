from django.shortcuts import render
<<<<<<< HEAD

from django.http import HttpResponse, Http404
=======
from .models import News
from django.http import HttpResponse
>>>>>>> 673e31d9c1ef36bdd6f547deaf4c6ffb75d0385f

def home(request):
    return render(request, 'home.html')

def news(request):
<<<<<<< HEAD
    return render(request, 'news.html')

def country(request, country_name='all'):
    return render(request, 'country.html', {'country': country_name})
    # return render(request, 'country.html')

def world(request):
    return render(request, 'world.html')
=======

    latest = News.objects.all()

    print(latest)

    return render(request, 'news.html',{'latest': latest})
>>>>>>> 673e31d9c1ef36bdd6f547deaf4c6ffb75d0385f
