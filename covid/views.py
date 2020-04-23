from django.shortcuts import render
from .models import News
from django.http import HttpResponse

def home(request):
    return render(request, 'home.html')

def news(request):

    latest = News.objects.all()

    print(latest)

    return render(request, 'news.html',{'latest': latest})