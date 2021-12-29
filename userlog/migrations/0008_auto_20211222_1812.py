# Generated by Django 3.2.5 on 2021-12-22 09:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userlog', '0007_alter_userlog_log_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlog',
            name='address',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='userlog',
            name='location',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='userlog',
            name='log_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 22, 18, 12, 49, 327414)),
        ),
        migrations.AlterField(
            model_name='userlog',
            name='log_type',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='userlog',
            name='weather',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='userlog',
            name='x',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='userlog',
            name='y',
            field=models.TextField(null=True),
        ),
    ]