#!/usr/bin/env python
# encoding: utf-8
'''
@author: Limz
@mail: limz@yisa.com
@name: urls.py
@time: 2018/5/12 18:27
@Description:
'''


from django.conf.urls import url
import  views

urlpatterns = [
    url(r'^projectmanage/', views.projectmanage, name='projectmanage'),
    url(r'^projectadd/', views.projectadd, name='projectadd'),
    url(r'^projectdel/', views.projectdel, name='projectdel'),
    url(r'^projectmod/', views.projectmod, name='projectmod'),
    url(r'^assetinfo/', views.assetinfo, name='assetinfo'),
    url(r'^nodeadd/', views.nodeadd, name='nodeadd'),
    url(r'^nodedel/', views.nodedel, name='nodedel'),
    url(r'^nodemod/', views.nodemod, name='nodemod'),
    url(r'^collectdevinfo/', views.collectdevinfo, name='collectdevinfo'),
    url(r'^selectdevinfo/', views.selectdevinfo, name='selectdevinfo'),
    url(r'^batchinput/', views.batchinput, name='batchinput'),
]