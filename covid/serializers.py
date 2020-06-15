from rest_framework import serializers

from .models import CountryData, DailyData

class CountryDataSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:

        model = CountryData
        fields = ('name','totalcase','activecase','newcase','deaths','newdeath','recovered',
                  'tests','continent')

class DailyDataSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:

        model = DailyData
        fields = ('country','totalcase','newcase','deaths','newdeath','date')
