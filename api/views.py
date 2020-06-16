from django.http import HttpResponse, JsonResponse

import covid.views as cv
import json


def india(request):
    data = {'data': cv.india_state_data()}
    return JsonResponse(data)