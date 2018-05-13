#!/usr/bin/env python
# encoding: utf-8
'''
@author: Limz
@mail: limz@yisa.com
@name: urls.py
@Create time: 2018/5/8 16:46
@IDE: PyCharm
@Description:
'''


from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^index', views.index, name='index'),
]