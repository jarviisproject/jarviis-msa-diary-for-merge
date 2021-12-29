from datetime import datetime

from django.db import models
from diary.models import Diary as diary

# Create your models here.
from rest_framework import serializers
from userlog.models import UserLog as userlog


class DiarySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    diary_date = serializers.CharField()
    weather = serializers.CharField()
    location = serializers.CharField()
    drawing = serializers.CharField()
    contents = serializers.CharField()
    memo = serializers.CharField()
    # log_id = serializers.CharField()
    log_id = serializers.ListField(child=serializers.IntegerField())
    user_id = serializers.IntegerField()

    class Meta:
        model = diary
        fileds = '__all__'

    def create(self, validated_data):
        return diary.objects.create(**validated_data)

    def update(self, instance, validated_data):
        diary.objects.filter(pk=instance.id).update(**validated_data)