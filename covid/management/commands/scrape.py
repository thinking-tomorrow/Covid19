from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
from covid.models import News, CountryData, CountryNews, DailyData
from datetime import datetime, timedelta
from os import path
import urllib
import sys
import pandas as pd
from django.db.models import Max

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

def scrape_all():
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

class Command(BaseCommand):
    help = "collect jobs"
    # define logic of command
    def handle(self, *args, **options):
        scrape_all()