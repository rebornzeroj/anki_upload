# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-03-02 02:53
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0004_auto_20170301_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stats',
            name='upload_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 2, 2, 53, 30, 901901)),
        ),
    ]