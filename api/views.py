from django.http import HttpResponse, JsonResponse
import covid.views as cv
import json
from covid.models import CountryData

def home(request):
    return HttpResponse("OUR API")


def india(request):
    data = {'data': cv.india_state_data()}
    return JsonResponse(data)


def country(request, country_name):
    try:
        country_data = CountryData.objects.get(name__iexact=f'{country_name}')
        payload = { 'name': country_data.name, 
                    'total_case' : country_data.totalcase, 
                    'active_case': country_data.activecase,
                    'total_death': country_data.deaths,
                    'recovered'  : country_data.recovered,
                    'total_tests': country_data.tests
                }
        return JsonResponse({'status': 'success', 'data': payload})
    except Exception as e:
        return JsonResponse({'status': 'failed'})


def country_daily(request, country_name, date):
    return JsonResponse({'status': 'testing', 'date': date})