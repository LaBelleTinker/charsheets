# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-17 20:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20160517_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='effect',
            name='bonus_amount',
            field=models.IntegerField(default=None, null=True),
        ),
    ]
