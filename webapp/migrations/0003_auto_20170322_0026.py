# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-22 00:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_auto_20170322_0024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publications',
            name='Service',
            field=models.CharField(max_length=50),
        ),
    ]
