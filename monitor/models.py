# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Pagedata(models.Model):
    ip = models.GenericIPAddressField(max_length=20, unique=True)
    region = models.CharField(max_length=15, null=True)
    totaldata = models.IntegerField()
    passtime = models.CharField(max_length=20)
    status = models.CharField(max_length=30,null=True)
    querytime = models.CharField(max_length=50, blank=True)
    totaluser = models.CharField(max_length=30, null=True, blank=True)
    totallog = models.CharField(max_length=100, blank=True)
    todaylog = models.CharField(max_length=50, blank=True)
