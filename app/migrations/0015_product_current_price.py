# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-23 10:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20180523_1011'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='current_price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]