from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Max
from .models import News, CountryData, CountryNews, DailyData

import sys
import json
import urllib
import requests
import pandas as pd
from os import path
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from datetime import datetime, timedelta


country_dict = {"USA": "United States of America", "UK": "United Kingdom", "UAE": "United Arab Emirates", 
                "S. Korea": "Korea South", "Czechia": "Czech Republic", "North Macedonia": "Macedonia", 
                "Ivory Coast": "Cote d Ivoire", "DRC": "Democratic Republic of the Congo", "Taiwan": "Republic of China",
                "Réunion": "France", "Palestine": "Palestinian territory", "Congo": "Republic of the Congo",
                "Guinea-Bissau": "Guinea Bissau", "Faeroe Islands": "Faroe Islands", "Cabo Verde": "Cape Verde",
                "Eswatini": "Swaziland", "CAR": "Central African Republic", "Timor-Leste": "East Timor", "Curaçao": "Curacao",
                "St. Vincent Grenadines": "Saint Vincent and the Grenadines", "Turks and Caicos": "Turks and Caicos Islands",
                "British Virgin Islands": "Virgin Islands British", "St. Barth": "Saint Barthelemy", "Caribbean Netherlands": "Netherlands",
                "Saint Pierre Miquelon": "Saint Pierre and Miquelon"}


def my_int(str):
    if str.strip().isnumeric():
        return int(str)
    else:
        return 0


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


def india_state_data():
    url_state = 'https://api.covid19india.org/data.json'
    request_state = requests.get(url_state)
    data_state = request_state.json()

    url_district = 'https://api.covid19india.org/v2/state_district_wise.json'
    request_district = requests.get(url_district)
    data_district = request_district.json()

    states = data_state['statewise'][1:]

    for state in states:
        district_raw = [obj for obj in data_district if obj['state'] == state['state']]
        districts = district_raw[0]['districtData']

        state['districts'] = districts

    return states


def home(request):
    world_data = scrape_world()

    recoveries_list = world_data[2].split(',')
    recoveries = ''
    for recovery in recoveries_list:
        recoveries+=recovery

    death_list = world_data[1].split(',')
    deaths = ''
    for death in death_list:
        deaths+=death

    print(recoveries)
    print(deaths)
    total_outcome = int(recoveries) + int(deaths)

    print(total_outcome)

    recovery_percent = (int(recoveries) / int(total_outcome)) * 100

    death_percent = 100 - recovery_percent

    worlddailydata = DailyData.objects.filter(country='World')
    return render(request, 'home.html',
                  {'world_total': world_data[0], 'world_death': world_data[1], 'world_recovery': world_data[2],
                   'world_daily_data': worlddailydata, 'closed_cases':total_outcome, 'recovery_percent':recovery_percent,
                   'death_percent':death_percent})


def graphs(request):
    #daily_data()
    world_daily_data = DailyData.objects.filter(country='World')

    countries_to_exclude = ['International']
    max_date = DailyData.objects.aggregate(Max('date'))['date__max']
    percentage_data = DailyData.objects.exclude(country__in=countries_to_exclude).filter(date__exact=str(max_date)).order_by('-totalcase')

    for data in world_daily_data:
        data.date = str(data.date)

    return render(request,'graphs.html', {'world_daily_data' : world_daily_data[32:], 'percentage_data': percentage_data})


def news(request):
    #scrape_news()
    latest_news = News.objects.all().order_by('-id')
    return render(request, 'news.html', {'latest_news': latest_news})


def country(request):
    # scrape()
    countries = CountryData.objects.order_by('-totalcase')
    return render(request, 'country.html', {'countries': countries})
    

def country_detail(request, country_name):

    if country_name == 'India':

        return redirect('india')

    news = CountryNews.objects.filter(country=country_name).order_by('-id')
    #country_daily_data(country_name)

    dailydata = DailyData.objects.filter(country=country_name)

    country_data = CountryData.objects.get(name__iexact=f'{country_name}')
    return render(request, 'country_detail.html', {'country': country_data, 'latest_news': news, 'countrydailydata':dailydata[32:]})


def world(request):
    world_data = scrape_world()
    worlddailydata = DailyData.objects.filter(country='World')
    return render(request, 'world.html', {'world_total': world_data[0], 'world_death': world_data[1], 'world_recovery': world_data[2], 'worlddailydata' : worlddailydata})


def search(request):

    if request.method == "POST":
        data = request.POST['data']
        news = News.objects.filter(heading__contains=data).order_by('-id')
        return render(request,'news.html', {'latest_news':news})
    else:
        pass

    return redirect('/')


def news_detail(request, news_id):
    news = News.objects.filter(id=news_id)
    return render(request, 'news-detail.html', {'news': news})


def about(request):
    return render(request,'about.html')    


def tips(request):
    return render(request,'tips.html')

def india(request):
    news = CountryNews.objects.filter(country="India").order_by('-id')
    # country_daily_data(country_name)

    states = india_state_data()

    dailydata = DailyData.objects.filter(country="India")

    country_data = CountryData.objects.get(name__iexact="India")
    return render(request, 'india.html',
                  {'country': country_data, 'latest_news': news, 'countrydailydata': dailydata[32:], 'states':states})

def state(request, state_name):

    return render(request,'state.html',{'state':state_name})

