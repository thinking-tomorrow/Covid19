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

def tips(request):
    return render(request,'tips.html')

def scrape():
    source = requests.get('https://www.worldometers.info/coronavirus/').text
    soup = BeautifulSoup(source, 'lxml')

    countries = soup.find_all('tr')
    countries = countries[9:221]

    for country in countries:

        rows = country.find_all('td')
        rows = list(map(lambda x:str(x.text).replace(',', ''), rows))

        name = rows[0]
        
        country = '-'.join(name.split())
        url = f"https://www.countries-ofthe-world.com/flags-normal/flag-of-{country}.png"


        my_country              = CountryData()
        my_country.name         = name
        my_country.totalcase    = my_int(rows[1])
        my_country.activecase   = my_int(rows[6])
        my_country.newcase      = my_int(rows[2].replace('+', ''))
        my_country.deaths       = my_int(rows[3])
        my_country.newdeath     = my_int(rows[4].replace('+', ''))
        my_country.recovered    = my_int(rows[5])
        my_country.tests        = my_int(rows[10])
        my_country.flag         = url

        my_country.save()


def scrape_world():
    source = requests.get('https://www.worldometers.info/coronavirus/').text
    soup = BeautifulSoup(source, 'lxml')

    totals = soup.find_all('div', class_='maincounter-number')
    world_data = []
    for total in totals:
        world_data.append(total.span.text)

    return world_data


def scrape_news():
    source = requests.get('https://www.indiatimes.com/').text
    soup = BeautifulSoup(source, 'lxml')

    articles = soup.find_all('div', class_='card-div')
    articles = articles[0:len(articles)-1]

    for article in articles:
        title = article.a['title']
        url = article.a['href']
        img = article.img['src']

        r = requests.get(url, allow_redirects=True)
        open(f'', 'wb').write(r.content)


        news = News()
        news.heading(title)
        news.body(url)
        news.img()
        news.date()
        news.save()


def home(request):
    return render(request, 'home.html')

def news(request):
    latest_news = News.objects.all()
    return render(request, 'news.html', {'latest_news': latest_news})

def country(request, country_name='all'):
    if country_name == 'all':
        # scrape()
        countries = CountryData.objects.order_by('-totalcase')
        return render(request, 'country.html', {'countries': countries})
    else:
        country_data = CountryData.objects.get(name__iexact=f'{country_name}')
        return render(request, 'country.html', {'country': country_data})

def world(request):
    world_data = scrape_world()
    return render(request, 'world.html', {'world_total': world_data[0], 'world_death': world_data[1], 'world_recovery': world_data[2]})
