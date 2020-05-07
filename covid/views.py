from django.shortcuts import render
from django.http import HttpResponse
from .models import News, CountryData, CountryNews, DailyData
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from os import path
import requests
import urllib
import sys
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

        if name in country_dict:
            name = country_dict[name]

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
        my_country.total_pop    = my_int(rows[8])
        my_country.death_pop    = my_int(rows[9])
        my_country.test_pop     = my_int(rows[11])
        my_country.continent    = rows[12]
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


def dailydatacountrywise(country):

    daily = DailyData()

    url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"

    df = pd.read_csv(url)

    df.rename(columns={'location':'Country'},inplace=True)

    date = str(datetime.now() - timedelta(days=1))[:10]
    fil = df['date'] == date
    df = df[fil]

    df.set_index('Country', inplace=True)

    daily.country = str(country)
    daily.totalcase = df.at[str(country),'total_cases']
    daily.newcase = df.at[str(country),'new_cases']
    daily.deaths = df.at[str(country),'total_cases']
    daily.newdeath = df.at[str(country),'new_deaths']
    daily.date = date

    daily.save()


def daily_data():
    print("here")
    url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
    columns = {'location', 'date', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths'}
    df = pd.read_csv(url, usecols=columns, index_col='location')
    df.rename(columns={'location':'Country'},inplace=True)
    print("here 1")

    world_df = df.loc['World']

    for index, row in world_df.iterrows():
        print(index)
        daily = DailyData()
        daily.country = str(index)
        daily.totalcase = row['total_cases'] 
        daily.newcase = row['new_cases']
        daily.deaths = row['total_deaths']
        daily.newdeath = row['new_deaths']
        daily.date = row['date']
        daily.save()


def country_daily_data(country):
    print("here")
    url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
    columns = {'location', 'date', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths'}
    df = pd.read_csv(url, usecols=columns, index_col='location')
    df.rename(columns={'location':'Country'},inplace=True)
    print("here 1")

    world_df = df.loc[str(country)]

    for index, row in world_df.iterrows():
        print(index)
        daily = DailyData()
        daily.country = str(index)
        daily.totalcase = row['total_cases'] 
        daily.newcase = row['new_cases']
        daily.deaths = row['total_deaths']
        daily.newdeath = row['new_deaths']
        daily.date = row['date']
        daily.save()

def scrape_country_news():

    countries = CountryData.objects.all()

    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"

    for country in countries:
        query = f"Covid {country.name}"
        query = query.replace(' ', '+')
        URL = f"https://google.com/search?q={query}"


        headers = {"user-agent": USER_AGENT}
        resp = requests.get(URL, headers=headers)

        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, "html.parser")

            for g in soup.find_all('div', class_='r'):
                anchors = g.find_all('a')
                if anchors:
                    link = anchors[0]['href']
                    title = g.find('h3').text
                    item = {
                        "title": title,
                        "link": link
                    }

                    if 'wikipedia.org' in link or 'worldometer' in link:
                        continue
                    
                    news = CountryNews()
                    news.country = country.name
                    news.link = link
                    news.title = title
                    news.date = str(datetime.now())[:10]
                    news.save()


def home(request):
    # scrape_country_news()
    # daily_data()
    news = News.objects.all()
    return render(request, 'home.html', {'latest_news': news})


def graphs(request):
    world_daily_data = DailyData.objects.filter(country='World')
    
    for data in world_daily_data:
        data.date = str(data.date)
        print(data.date)

    return render(request,'graphs.html', {'world_daily_data' : world_daily_data[32:]})


def news(request):
    #scrape_news()
    latest_news = News.objects.all()
    return render(request, 'news.html', {'latest_news': latest_news})


def country(request):
    # scrape()
    countries = CountryData.objects.order_by('-totalcase')
    return render(request, 'country.html', {'countries': countries})
    

def country_detail(request, country_name):
    news = CountryNews.objects.filter(country=country_name)
    #country_daily_data(country_name)

    dailydata = DailyData.objects.filter(country=country_name)

    print(dailydata)

    country_data = CountryData.objects.get(name__iexact=f'{country_name}')
    return render(request, 'country_detail.html', {'country': country_data, 'latest_news': news, 'countrydailydata':dailydata})


def world(request):
    world_data = scrape_world()
    worlddailydata = DailyData.objects.filter(country='World')
    return render(request, 'world.html', {'world_total': world_data[0], 'world_death': world_data[1], 'world_recovery': world_data[2], 'worlddailydata' : worlddailydata})


def search(request):

    if request.method == "POST":
        data = request.POST['data']
        news = News.objects.filter(heading__contains=data)
        return render(request,'news.html', {'latest_news':news})
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
        return render(request,'country.html',{'countries':countries})


def about(request):
    return render(request,'about.html')

#DailyData.objects.all().delete()