# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-30 07:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_rateproduct_rating_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
