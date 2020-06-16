from django.http import HttpResponse, JsonResponse

import covid.views as cv
import json


def india(request):
    data = {'data': cv.india_state_data()}
    return JsonResponse(data)

def state(request, state_name):
    data = {'data': cv.state_data(state_name)}
    return JsonResponse(data)