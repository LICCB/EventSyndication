# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-22 01:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EventInfo',
            fields=[
                ('EventID', models.AutoField(primary_key=True, serialize=False)),
                ('EventName', models.CharField(max_length=50)),
                ('EventDescription', models.TextField()),
                ('EventMeetLocation', models.CharField(max_length=50)),
                ('EventDestination', models.CharField(max_length=50)),
                ('EventStart', models.DateTimeField()),
                ('EventEnd', models.DateTimeField()),
                ('PostingID', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Postings',
            fields=[
                ('PostingID', models.AutoField(primary_key=True, serialize=False)),
                ('Facebook', models.BooleanField()),
                ('MeetUp', models.BooleanField()),
                ('EventBrite', models.BooleanField()),
            ],
        ),
    ]
