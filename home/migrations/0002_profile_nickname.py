# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-11 16:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='nickname',
            field=models.CharField(default='rand', max_length=15),
            preserve_default=False,
        ),
    ]
