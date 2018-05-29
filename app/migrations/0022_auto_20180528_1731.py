# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-28 15:31
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0021_auto_20180528_1654'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='medium_rate',
            new_name='avg_rate',
        ),
        migrations.AddField(
            model_name='product',
            name='buyer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='buyer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='product',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller', to=settings.AUTH_USER_MODEL),
        ),
    ]
