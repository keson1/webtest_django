#!/usr/bin/env python
# encoding: utf-8
'''
@author: Limz
@mail: limz@yisa.com
@name: urls.py
@Create time: 2018/5/8 11:22
@IDE: PyCharm
@Description:
'''
from django.conf.urls import url
import views

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^register/', views.register, name='register'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^loginauth/', views.loginauth)
]
