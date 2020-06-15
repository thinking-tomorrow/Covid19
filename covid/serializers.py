from rest_framework import serializers

from .models import CountryData

class CountryDataSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:

        name = CountryData
        fields = ('name','totalcase','activecase','newcase','deaths','newdeath','recovered',
                  'tests','continent')
