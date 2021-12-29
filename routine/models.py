from datetime import datetime

from django.db import models
from django.db.models import IntegerField, CharField
from django_mysql.models import ListTextField


# Create your models here.


class Routine(models.Model):
    create_date = models.DateTimeField(default=datetime.now())
    log_repeat = models.IntegerField()
    priority = models.IntegerField()
    grade = models.IntegerField()
    contents = models.TextField(null=True)
    location = models.TextField(null=True)
    cron = ListTextField(base_field=CharField(max_length=255), null=True)
    days = ListTextField(base_field=CharField(max_length=255), null=True)
    hours = ListTextField(base_field=CharField(max_length=255), null=True)
    log_id = ListTextField(base_field=IntegerField(), null=True)      # fk
    user_id = models.IntegerField()     # fk

    class Meta:
        db_table = 'routine'

    def __str__(self):
        return f'{self.pk}'