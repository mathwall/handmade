# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-29 07:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_auto_20180528_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='buyer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='buyer', to=settings.AUTH_USER_MODEL),
        ),
    ]
