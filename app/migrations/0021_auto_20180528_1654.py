# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-28 14:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_auto_20180528_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='end_date_of_sale',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='start_date_of_sale',
            field=models.DateField(),
        ),
    ]
