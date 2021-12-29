from datetime import datetime

from django.db import models
from django.db.models import IntegerField, CharField
from django_mysql.models import ListTextField
# Create your models here.


class Flower(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    title = models.TextField()
    grade = models.IntegerField()
    step = models.IntegerField()
    color = models.TextField()
    log_id = ListTextField(base_field=IntegerField(), null=True)
    event_id = ListTextField(base_field=IntegerField(), null=True)
    user_id = models.IntegerField()

    class Meta:
        db_table = 'flower'

    def __str__(self):
        return f"{self.pk}"
