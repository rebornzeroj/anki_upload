# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-03-01 18:22
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stats',
            name='upload_time',
            field=models.DateField(default=datetime.datetime(2017, 3, 1, 18, 22, 54, 462811)),
        ),
    ]
