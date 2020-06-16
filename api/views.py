from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Max
from covid.models import News, CountryData, CountryNews, DailyData
from rest_framework import viewsets
from .serializers import CountryDataSerializer, DailyDataSerializer

import covid.views as cv
import json

class CountryDataViewSet(viewsets.ModelViewSet):
    queryset = CountryData.objects.all().order_by('name')
    serializer_class = CountryDataSerializer

class DailyDataViewSet(viewsets.ModelViewSet):
    queryset = DailyData.objects.all().order_by('country')
    serializer_class = DailyDataSerializer

def india(request):
    data = {'data': cv.india_state_data()}
    return JsonResponse(data)