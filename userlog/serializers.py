from datetime import datetime

from django.db import models

# Create your models here.
from rest_framework import serializers
from userlog.models import UserLog as userlog


class UserLogSerializer(serializers.Serializer):
    id = serializers.CharField()
    location = serializers.CharField(allow_blank=True)
    address = serializers.CharField(allow_blank=True)
    x = serializers.CharField(allow_blank=True)
    y = serializers.CharField(allow_blank=True)
    log_date = serializers.CharField()
    weather = serializers.CharField()
    log_type = serializers.CharField()
    contents = serializers.CharField()
    # item = serializers.CharField()
    user_id = serializers.CharField()

    class Meta:
        model = userlog
        fileds = '__all__'

    def create(self, validated_data):
        return userlog.objects.create(**validated_data)

    def update(self, instance, validated_data):
        userlog.objects.filter(pk=instance.id).update(**validated_data)