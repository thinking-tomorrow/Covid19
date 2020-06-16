from django.http import HttpResponse, JsonResponse
import covid.views as cv
import json
import requests
from covid.models import CountryData, DailyData
from django.views.decorators.csrf import csrf_exempt

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
def webhook(request):
    # response = {'status': 'failed'}
    # if request.method == 'POST':
    #     request = json.loads(request.body)
    #     params = request['queryResult']['queryText']['parameters']

    #     if params['status']:
    #         if params['geo-country']:
    #             # get country specific data
    #             if params['date-time']:
    #                 # get daily data
    #             else:
    #                 # get overall country wise data
    #                 country_raw(params['geo-country'])

    #         else:
    #             # get world data
    #             pass
    reply = {
        "fulfillmentText": "I am good....",
    }

    return JsonResponse(reply)