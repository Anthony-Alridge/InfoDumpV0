# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-11 16:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamer', '0005_auto_20160501_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='focus',
            name='keywords',
            field=models.ManyToManyField(to='streamer.KeyWords'),
        ),
    ]