from rest_framework import serializers
# pip install Django django-rest-framework
from .models import LocationData as loc


class LocationSerializer(serializers.Serializer):
    location = serializers.CharField()
    category = serializers.CharField()
    address = serializers.CharField()

    class Meta:
        model = loc
        fileds = '__all__'