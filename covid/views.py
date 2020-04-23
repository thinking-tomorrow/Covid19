from django.shortcuts import render
from django.http import HttpResponse
from .models import News, CountryData
from bs4 import BeautifulSoup
import requests
import sys

def my_int(str):
    if str.strip().isnumeric():
        return int(str)
    else:
        return 0

def scrape():
    source = requests.get('https://www.worldometers.info/coronavirus/').text
    soup = BeautifulSoup(source, 'lxml')

    countries = soup.find_all('tr')
    countries = countries[9:220]

    for country in countries:
        rows = country.find_all('td')
        rows = list(map(lambda x:str(x.text).replace(',', ''), rows))

        my_country              = CountryData()
        my_country.name         = rows[0]
        my_country.totalcase    = my_int(rows[1])
        my_country.activecase   = my_int(rows[6])
        my_country.newcase      = my_int(rows[2].replace('+', ''))
        my_country.deaths       = my_int(rows[3])
        my_country.newdeath     = my_int(rows[4].replace('+', ''))
        my_country.recovered    = my_int(rows[5])
        my_country.tests        = my_int(rows[10])

        my_country.save()


def home(request):
    return render(request, 'home.html')

def news(request):
    latest_news = News.objects.all()
    return render(request, 'news.html', {'latest_news': latest_news})

def country(request, country_name='all'):
    if country_name == 'all':
        countries = CountryData.objects.order_by('-totalcase')
        return render(request, 'country.html', {'countries': countries})
    else:
        country_data = CountryData.objects.get(name__iexact=f'{country_name}')
        return render(request, 'country.html', {'country': country_data})

def world(request):
    # scrape()
    return render(request, 'world.html')