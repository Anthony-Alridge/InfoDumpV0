# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-13 20:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamer', '0011_auto_20160729_2028'),
    ]

    operations = [
        migrations.AddField(
            model_name='filemodel',
            name='name',
            field=models.CharField(default='blah', max_length=256),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='filemodel',
            name='file_field',
            field=models.FileField(upload_to='files'),
        ),
        migrations.AlterField(
            model_name='focus',
            name='keywords',
            field=models.ManyToManyField(to='streamer.KeyWords'),
        ),
    ]
