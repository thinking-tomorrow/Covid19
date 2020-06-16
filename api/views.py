from django.http import HttpResponse, JsonResponse

import covid.views as cv
import json


def india(request):
    data = {'data': cv.india_state_data()}
    return JsonResponse(data)

def state(request, state_name):
    a = {'a' : cv.state_data(state_name)}
    b = {'b':a['a'][0]}
    print(b)


    return JsonResponse(b)