# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-06 05:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TradeNet', '0006_auto_20161205_2334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='company',
            field=models.CharField(max_length=200),
        ),
        migrations.DeleteModel(
            name='Company',
        ),
    ]
