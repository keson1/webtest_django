# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-05-20 06:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='pagedata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField(unique=True)),
                ('region', models.CharField(max_length=15, null=True)),
                ('totaldata', models.IntegerField()),
                ('passtime', models.CharField(max_length=20)),
                ('status', models.CharField(max_length=30, null=True)),
                ('querytime', models.CharField(blank=True, max_length=50)),
                ('totaluser', models.CharField(blank=True, max_length=30, null=True)),
                ('totallog', models.CharField(blank=True, max_length=100)),
                ('todaylog', models.CharField(blank=True, max_length=50)),
            ],
        ),
    ]
