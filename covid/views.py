from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Max
from .models import News, CountryData, CountryNews, DailyData, Predictions
from rest_framework import viewsets

import sys
import json
import urllib
import requests
import pandas as pd
from os import path
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from .serializers import CountryDataSerializer, DailyDataSerializer

country_dict = {"USA": "United States of America", "UK": "United Kingdom", "UAE": "United Arab Emirates", 
                "S. Korea": "Korea South", "Czechia": "Czech Republic", "North Macedonia": "Macedonia", 
                "Ivory Coast": "Cote d Ivoire", "DRC": "Democratic Republic of the Congo", "Taiwan": "Republic of China",
                "Réunion": "France", "Palestine": "Palestinian territory", "Congo": "Republic of the Congo",
                "Guinea-Bissau": "Guinea Bissau", "Faeroe Islands": "Faroe Islands", "Cabo Verde": "Cape Verde",
                "Eswatini": "Swaziland", "CAR": "Central African Republic", "Timor-Leste": "East Timor", "Curaçao": "Curacao",
                "St. Vincent Grenadines": "Saint Vincent and the Grenadines", "Turks and Caicos": "Turks and Caicos Islands",
                "British Virgin Islands": "Virgin Islands British", "St. Barth": "Saint Barthelemy", "Caribbean Netherlands": "Netherlands",
                "Saint Pierre Miquelon": "Saint Pierre and Miquelon"}


class CountryDataViewSet(viewsets.ModelViewSet):
    queryset = CountryData.objects.all().order_by('name')
    serializer_class = CountryDataSerializer

class DailyDataViewSet(viewsets.ModelViewSet):
    queryset = DailyData.objects.all().order_by('name')
    serializer_class = DailyDataSerializer

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

def scrape():
    source = requests.get('https://www.worldometers.info/coronavirus/').text
    soup = BeautifulSoup(source, 'lxml')

    countries = soup.find_all('tr')
    countries = countries[9:221]

    for country in countries:

        rows = country.find_all('td')
        rows = list(map(lambda x:str(x.text).replace(',', ''), rows))

        name = rows[1]

        if name in country_dict:
            name = country_dict[name]

        if not path.isfile(f'media/flag/{name}.png'):
            country = name.replace(' ', '_').lower()
            url = f'http://img.freeflagicons.com/thumb/rectangular_icon_with_shadow/{country}/{country}_640.png'
            r = requests.get(url, allow_redirects=True, headers={"User-Agent": "XY"})
            open(f'media/flag/{name}.png', 'wb').write(r.content)

        my_country              = CountryData()
        my_country.name         = name
        my_country.totalcase    = my_int(rows[2])
        my_country.activecase   = my_int(rows[7])
        my_country.newcase      = my_int(rows[3].replace('+', ''))
        my_country.deaths       = my_int(rows[4])
        my_country.newdeath     = my_int(rows[5].replace('+', ''))
        my_country.recovered    = my_int(rows[6])
        my_country.tests        = my_int(rows[11])
        my_country.total_pop    = my_int(rows[9])
        my_country.death_pop    = my_int(rows[10])
        my_country.test_pop     = my_int(rows[12])
        my_country.continent    = rows[14]
        my_country.flag         = f'media/flag/{name}.png'

        if name == 'United States of America':
            my_country.name = 'United States'

        my_country.save()


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


def state_data(state):
    url_state = 'https://api.covid19india.org/data.json'
    request_state = requests.get(url_state)
    data_state = request_state.json()

    states = data_state['statewise'][1:]
    x = [obj for obj in states if obj['state'] == state]
    return x



def district_data(state):
    url_district = 'https://api.covid19india.org/v2/state_district_wise.json'
    request_district = requests.get(url_district)
    data_district = request_district.json()

    district_raw = [obj for obj in data_district if obj['state'] == state]
    districts = district_raw[0]['districtData']

    return districts


def state_daily_data(state_code):
    url_daily = 'https://api.covid19india.org/states_daily.json'
    request_daily = requests.get(url_daily)
    data_daily = request_daily.json()['states_daily']

    date      = [x["date"] for x in data_daily if x["status"] == 'Confirmed']
    confirmed = [x[state_code] for x in data_daily if x['status'] == 'Confirmed']
    recovered = [x[state_code] for x in data_daily if x['status'] == 'Recovered']
    deceased  = [x[state_code] for x in data_daily if x['status'] == 'Deceased']

    return {'date': date, 'confirmed': confirmed, 'recovered': recovered, 'deceased': deceased}


def district_daily_data(state, district):
    url_daily = 'https://api.covid19india.org/districts_daily.json'
    request_daily = requests.get(url_daily)
    data_daily = request_daily.json()['districtsDaily'][state][district]

    date      = [x["date"] for x in data_daily]
    active    = [x["active"] for x in data_daily]
    confirmed = [x["confirmed"] for x in data_daily]
    recovered = [x["recovered"] for x in data_daily]
    deceased  = [x["deceased"] for x in data_daily]

    return {'date': date, 'active': active, 'confirmed': confirmed, 'recovered': recovered, 'deceased': deceased}


def home(request):
    world_data = scrape_world()

    recoveries=int(world_data[2].replace(',', ''))
    deaths = int(world_data[1].replace(',', ''))

    total_outcome = int(recoveries) + int(deaths)
    recovery_percent = round((int(recoveries) / int(total_outcome)) * 100, 2)
    death_percent = round(100 - recovery_percent, 2)

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
    #scrape()
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
    states_data = state_data(state_name)

    state_code = states_data[0]['statecode'].lower()


    state_wise_data = state_daily_data(state_code)
    state_date = state_wise_data['date']
    state_data_confirmed = state_wise_data['confirmed']
    state_data_recovered = state_wise_data['recovered']
    state_data_deceased = state_wise_data['deceased']
    #print(state_wise_data)
    districts = district_data(state_name)

    '''df = pd.DataFrame(state_data_confirmed)
    print(df)
    df = df.cumsum()
    print(df)'''

    total_confirmed = []

    counter = 0

    for confirmed in state_data_confirmed:
        confirmed = int(confirmed)
        if counter == 0:
            total_confirmed.append(confirmed)
        else:
            day_total_confirmed = total_confirmed[counter-1] + confirmed
            total_confirmed.append(day_total_confirmed)
        counter+=1

    return render(request,'state.html',{'state':state_name , 'districts' : districts, 'states_data':states_data , 'state_confirmed':state_data_confirmed, 'state_date':state_date, 'state_recovered':state_data_recovered, 'total_confirmed':total_confirmed})