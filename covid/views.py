from django.shortcuts import render, redirect
from django.db.models import Max
from .models import News, CountryData, CountryNews, DailyData

import requests
from os import path
from bs4 import BeautifulSoup
from datetime import datetime
#from fbprophet import Prophet
import pandas as pd

country_dict = {"USA": "United States of America", "UK": "United Kingdom", "UAE": "United Arab Emirates", 
                "S. Korea": "Korea South", "Czechia": "Czech Republic", "North Macedonia": "Macedonia", 
                "Ivory Coast": "Cote d Ivoire", "DRC": "Democratic Republic of the Congo", "Taiwan": "Republic of China",
                "Réunion": "France", "Palestine": "Palestinian territory", "Congo": "Republic of the Congo",
                "Guinea-Bissau": "Guinea Bissau", "Faeroe Islands": "Faroe Islands", "Cabo Verde": "Cape Verde",
                "Eswatini": "Swaziland", "CAR": "Central African Republic", "Timor-Leste": "East Timor", "Curaçao": "Curacao",
                "St. Vincent Grenadines": "Saint Vincent and the Grenadines", "Turks and Caicos": "Turks and Caicos Islands",
                "British Virgin Islands": "Virgin Islands British", "St. Barth": "Saint Barthelemy", "Caribbean Netherlands": "Netherlands",
                "Saint Pierre Miquelon": "Saint Pierre and Miquelon"}


def scrape_world():
    source = requests.get('https://www.worldometers.info/coronavirus/').text
    soup = BeautifulSoup(source, 'lxml')

    totals = soup.find_all('div', class_='maincounter-number')
    world_data = []
    for total in totals:
        world_data.append(total.span.text)

    return world_data


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
<<<<<<< HEAD

=======
'''
def predictions2(country):
>>>>>>> 6d9aa8f64b360208da43e5e39844e4578448a32f

def predictions2(country):
    if country == 'World':
        world = DailyData.objects.filter(country='World')
        world_values = world.values('date','totalcase')
        country_data = pd.DataFrame.from_records(world_values)
        country = 'World'
    else:
        if country == 'United States':
            country='US'
        data = requests.get('https://pomber.github.io/covid19/timeseries.json').json()
        country_data = data[country]
        country = 'Other'


    
    df = pd.DataFrame(country_data)
    
    if country == 'World':
        df.rename(columns={'date': 'ds', 'totalcase': 'y'}, inplace=True)
    else:
        df.rename(columns={'date': 'ds', 'confirmed': 'y'}, inplace=True)

    m = Prophet(changepoint_prior_scale=5, interval_width=1)
    m.fit(df)
    
    future = m.make_future_dataframe(periods=15)
    forecast = m.predict(future)
    updated_forecast = forecast[['ds', 'yhat_upper']]

    tail_updated_forecast = updated_forecast.tail(15)

    tail_updated_forecast.set_index('ds', inplace=True)

    return tail_updated_forecast


def predict_country(country):
    url = "https://pomber.github.io/covid19/timeseries.json"
    countries = requests.get(url).json()
    countries['World'] = True
    countries['US'] = True

    x = country
    r = [country for country in countries if country == x]
    
    if len(r) != 0:
        df = predictions2(country)
        df.rename(columns={'ds':'dates','yhat_upper':'predictions'},inplace=True)
        df.reset_index(inplace=True)
        df = df.to_json()
        return {'data':df}

    else:
        return {'data':'failed'}
'''
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

    news = CountryNews.objects.filter(country=country_name).order_by('-id')[:9]
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

def predictions(request):

    countries = []

    for country in CountryData.objects.all():

        countries.append(country.name)

    print(countries)

    return render(request,'predict.html',{'countries':countries})