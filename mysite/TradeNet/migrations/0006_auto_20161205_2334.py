# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-06 05:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TradeNet', '0005_ownedstock_transaction'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='currentRev',
            new_name='size_score',
        ),
        migrations.RemoveField(
            model_name='company',
            name='profit',
        ),
    ]