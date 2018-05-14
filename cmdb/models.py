# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Projects(models.Model):
    projectname = models.CharField(max_length=20)
    remark = models.CharField(max_length=100, null=True)

class Nodes(models.Model):
    ipaddr = models.GenericIPAddressField(max_length=20, unique=True)
    nodename = models.CharField(max_length=15, null=True)
    sshport = models.IntegerField()
    rootpwd = models.CharField(max_length=20)
    project = models.ForeignKey(Projects)
    status = models.IntegerField(null=True)
    asset_num = models.CharField(max_length=50, blank=True)
    asset_type = models.CharField(max_length=30, null=True, blank=True)
    vendor = models.CharField(max_length=100, blank=True)
    up_time = models.CharField(max_length=50, blank=True)
    cpu_model = models.CharField(max_length=100, blank=True)
    cpu_num = models.CharField(max_length=100, blank=True)
    memory = models.CharField(max_length=30, blank=True)
    disk = models.CharField(max_length=255, blank=True)
    disk_vender = models.CharField(max_length=255, blank=True)
    aladin = models.CharField(max_length=255, blank=True)
    position = models.CharField(max_length=100, blank=True)
    remark = models.TextField(max_length=200, blank=True)
    graphics = models.CharField(max_length=200, blank=True)