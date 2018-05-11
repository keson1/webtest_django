# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class userInfo(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=30)
    gender = models.CharField(max_length=5)


