from datetime import datetime
from rest_framework import serializers
from flower.models import Flower as flower

from django.db import models
from django.db.models import IntegerField, CharField
from django_mysql.models import ListTextField
# Create your models here.


class FlowerSerializer(serializers.Serializer):
    id = serializers.CharField()
    create_date = serializers.CharField()
    update_date = serializers.CharField()
    title = serializers.CharField()
    grade = serializers.CharField()
    step = serializers.CharField()
    color = serializers.CharField()
    log_id = serializers.ListField(child=serializers.IntegerField())
    event_id = serializers.ListField(child=serializers.IntegerField())
    user_id = serializers.CharField()

    class Meta:
        model = flower
        fileds = '__all__'

    def create(self, validated_data):
        return flower.objects.create(**validated_data)

    def update(self, instance, validated_data):
        flower.objects.filter(pk=instance.id).update(**validated_data)