# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-23 12:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_product_current_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bid',
            old_name='id_product',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='bid',
            old_name='id_user',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='category',
            old_name='parent_id',
            new_name='parent',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='id_category',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='id_seller',
            new_name='seller',
        ),
        migrations.RenameField(
            model_name='rateproduct',
            old_name='id_product',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='rateuser',
            old_name='id_rated_user',
            new_name='rated_user',
        ),
        migrations.RenameField(
            model_name='rateuser',
            old_name='id_rating_user',
            new_name='rating_user',
        ),
    ]
