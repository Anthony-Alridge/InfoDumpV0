# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-22 13:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamer', '0015_auto_20160822_1335'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filemodel',
            name='file_name',
        ),
        migrations.AlterField(
            model_name='focus',
            name='keywords',
            field=models.ManyToManyField(to='streamer.KeyWords'),
        ),
    ]