# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-22 00:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Publications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Status', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=500)),
                ('EventID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.EventInfo')),
            ],
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=50)),
                ('IsEnabled', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='publications',
            name='Service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='webapp.Services'),
        ),
    ]
