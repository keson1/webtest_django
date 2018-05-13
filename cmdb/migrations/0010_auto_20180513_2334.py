# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-05-13 15:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0009_auto_20180513_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nodes',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmdb.Projects'),
        ),
        migrations.AlterField(
            model_name='nodes',
            name='up_time',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
