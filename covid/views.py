from django.shortcuts import render
from django.http import HttpResponse
from .models import News, CountryData
from bs4 import BeautifulSoup
from datetime import datetime
from os import path
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

        if not path.isfile(f'media/flag/{name}.png'):
            country = name.replace(' ', '_').lower()
            url = f'http://img.freeflagicons.com/thumb/rectangular_icon_with_shadow/{country}/{country}_640.png'
            r = requests.get(url, allow_redirects=True, headers={"User-Agent": "XY"})
            open(f'media/flag/{name}.png', 'wb').write(r.content)

        my_country              = CountryData()
        my_country.name         = name
        my_country.totalcase    = my_int(rows[1])
        my_country.activecase   = my_int(rows[6])
        my_country.newcase      = my_int(rows[2].replace('+', ''))
        my_country.deaths       = my_int(rows[3])
        my_country.newdeath     = my_int(rows[4].replace('+', ''))
        my_country.recovered    = my_int(rows[5])
        my_country.tests        = my_int(rows[10])
        my_country.flag         = f'media/flag/{name}.png'

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
        last_id = News.objects.latest('id').id
        title = article.a['title']
        url = article.a['href']
        img = article.img['src']

        r = requests.get(img, allow_redirects=True)
        open(f'media/{last_id+1}.jpg', 'wb').write(r.content)

        text_source = requests.get(url).text
        text_soup = BeautifulSoup(text_source, 'lxml')

        div = text_soup.article.find_all('div', class_='left-container')
        text = str()
        ps = div[0].find_all('p', class_=None)
        for p in ps:
            text += p.text

        news = News()
        news.heading = title
        news.body = text
        news.img = str(last_id+1) + '.jpg'
        news.date = str(datetime.now())[:10]
        news.link = url
        news.save()

def home(request):
    news = News.objects.all()
    return render(request, 'home.html',{'latest_news': news})

def news(request):
    # scrape_news()
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

def search(request):

    if request.method == "POST":
        data = request.POST['data']
        news = News.objects.filter(heading__contains=data)
        return render(request,'searchnews.html', {'news':news})
    else:
        pass

    return redirect('/')


def news_detail(request, news_id):
    news = News.objects.filter(id=news_id)
    return render(request, 'news-detail.html', {'news': news})


def searchcountries(request):

    if request.method == 'POST':
        country = request.POST['country']
        countries = CountryData.objects.filter(name__contains=country)
        return render(request,'countrysearchresult.html',{'countries':countries})