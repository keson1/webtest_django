# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-05-13 03:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0002_projects_remark'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assetinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ipaddr', models.GenericIPAddressField(unique=True)),
                ('nodename', models.CharField(max_length=15, null=True)),
                ('sshport', models.IntegerField(max_length=10)),
                ('rootpwd', models.CharField(max_length=20)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmdb.Projects')),
            ],
        ),
    ]