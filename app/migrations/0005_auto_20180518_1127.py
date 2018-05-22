# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-18 09:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20180518_0942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='city',
            field=models.CharField(blank=True, max_length=40),
        ),
        migrations.AlterField(
            model_name='profile',
            name='country',
            field=models.CharField(blank=True, max_length=40),
        ),
        migrations.AlterField(
            model_name='profile',
            name='creation_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='profile',
            name='postal_code',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='street',
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
