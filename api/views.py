from django.http import HttpResponse, JsonResponse
import covid.views as cv
import json
import requests
from covid.models import CountryData, DailyData
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import requests

def home(request):
    return HttpResponse("OUR API")


def india_raw():
    data = {'data': cv.india_state_data()}
    return data

@csrf_exempt
def india(request):
    return JsonResponse(india_raw())


def country_raw(country_name):
    try:
        country_data = CountryData.objects.get(name__iexact=f'{country_name}')
        payload = { 'name': country_data.name, 
                    'total_case' : country_data.totalcase, 
                    'active_case': country_data.activecase,
                    'total_death': country_data.deaths,
                    'recovered'  : country_data.recovered,
                    'total_tests': country_data.tests
                }
        return {'status': 'success', 'data': payload}
    except Exception as e:
        return {'status': 'failed'}

@csrf_exempt
def country(request, country_name):
    return JsonResponse(country_raw(country_name))


def country_daily_raw(country_name, date):
    try:
        daily_data = DailyData.objects.filter(country=country_name)
        data = list(filter(lambda x: str(x.date) == date, daily_data))[0]
        
        payload = { 
            'name'       : data.country, 
            'total_case' : data.totalcase, 
            'total_death': data.deaths,
            'new_case'   : data.newcase,
            'new_death'  : data.newdeath
        }

        return {'status': 'success', 'data': payload}
    except:
        return {'status': 'failed'}        

@csrf_exempt
def country_daily(request, country_name, date):
    return JsonResponse(country_daily_raw(country_name, date))


def state_raw(state_name):
    try:
        data = cv.state_data(state_name)[0]
        keys = ["state", "active", "confirmed", "deaths", "recovered", "statecode"]
        payload = {key: data[key] for key in keys}
        return {"status": "success", "data":payload}
    except Exception as e:
        return {'status': 'failed'}

@csrf_exempt
def state(request, state_name):
    return JsonResponse(state_raw(state_name))


@csrf_exempt
def world(request):
    return JsonResponse(country_raw('World'))


@csrf_exempt
def world_daily(request, date):
    return JsonResponse(country_daily_raw('World', date))


@csrf_exempt
def webhook(request):
    response = "Sorry! Didn't get that!"
    if request.method == 'POST':
        
        request = json.loads(request.body)
        params = request['queryResult']['parameters']

        if params['status']:
            if params['geo-country']:
                # get country specific data
                if params['date-time']:
                    date = params['date-time'][0][:10]
                    date = date.replace('2021', '2020')
                    data = country_daily_raw(params['geo-country'], date)

                    if data['status'] == 'failed':
                        response = "Sorry! Internal server error"
                    else:
                        data = data['data']
                        response = f"On {date} {data['new_case']} people were newly affected and {data['new_death']} newly died in {data['name']}. As of {date} {data['total_case']} people have been affected and {data['total_death']} have died."
                else:
                    # get overall country wise data
                    data = country_raw(params['geo-country'])
                    
                    if data['status'] == 'failed':
                        response = "Sorry! Internal server error"
                    else:
                        data = data['data']
                        response = f"A total of {data['total_case']} people have been affected in {data['name']} and out of them {data['total_death']} have died and {data['recovered']} has recovered while {data['total_tests']} have been tested."
            else:
                # get world data
                if params['date-time']:
                    date = params['date-time'][0][:10]
                    date = date.replace('2021', '2020')
                    data = country_daily_raw('World', date)
                    if data['status'] == 'failed':
                        response = "Sorry! Internal server error"
                    else:
                        data = data['data']
                        response = f"On {date} {data['new_case']} people were newly affected and {data['new_death']} newly died worldwide. As of {date} {data['total_case']} people have been affected and {data['total_death']} have died."
                else:
                    # get overall country wise data
                    data = country_raw('World')
                    
                    if data['status'] == 'failed':
                        response = "Sorry! Internal server error"
                    else:
                        data = data['data']
                        response = f"A total of {data['total_case']} people have been affected worldwide and out of them {data['total_death']} have died and {data['recovered']} has recovered."

        reply = {"fulfillmentText": response}
    else:
        reply = {'status': 'failed'}

    return JsonResponse(reply)


def predict(request, country):
    data = cv.predict_country(country)
    return JsonResponse(data)

def resources(request, state):
    data = requests.get('https://api.covid19india.org/resources/resources.json').json()
    data_df = pd.DataFrame(data['resources'])
    data_df.set_index('state', inplace=True)

    df = data_df.loc[state]
    sorted_df = df[(df['category'] == 'CoVID-19 Testing Lab') | (df['category'] == 'Government Helpline') | (df['category'] == 'Hospitals and Centers') | (df['category'] == 'Quarantine Facility') | (df['category'] == 'Fever Clinic')]

    new_df = sorted_df.to_json()

    data = {'data':new_df}

    return JsonResponse(data)