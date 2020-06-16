from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
from django.shortcuts import render, redirect
from django.db.models import Max
from covid.models import News, CountryData, CountryNews, DailyData
from rest_framework import viewsets
from .serializers import CountryDataSerializer, DailyDataSerializer


class CountryDataViewSet(viewsets.ModelViewSet):
    queryset = CountryData.objects.all().order_by('name')
    serializer_class = CountryDataSerializer

class DailyDataViewSet(viewsets.ModelViewSet):
    queryset = DailyData.objects.all().order_by('country')
    serializer_class = DailyDataSerializer