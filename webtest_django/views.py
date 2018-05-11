#!/usr/bin/env python
# encoding: utf-8
'''
@author: Limz
@mail: limz@yisa.com
@name: views.py
@Create time: 2018/5/8 11:28
@IDE: PyCharm
@Description:
'''

from django.shortcuts import redirect

def index(request):
    return redirect('/accounts/login/')