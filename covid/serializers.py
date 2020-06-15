from rest_framework import serializers

from .models import CountryData

class CountryDataSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:

        model = CountryData
        fields = ('name','totalcase','activecase','newcase','deaths','newdeath','recovered',
                  'tests','continent')
