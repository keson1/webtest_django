# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponseRedirect
from form import LoginUserForm,registerForm
from django.contrib import auth
from django.contrib.auth.models import User
import time
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse

def login(request):
    f = LoginUserForm(request.POST)
    error = ''
    if request.method == 'POST':
        if f.is_valid():
            auth.login(request, f.get_user())
            return HttpResponseRedirect('/main/')
        else:
            error = '登录失败'
    context = {'form': f,
               'error': error,
               }
    return render(request, "accounts/login.html", context)

def register(request):
    error = ''
    f = registerForm(request.POST)
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        email = request.POST.get('email', '')
        register_time = time.strftime("%Y-%m-%d %H:%M:%S")
        is_exist = User.objects.filter(username=username)
        if is_exist:
            error = '用户名已存在'
        else:
            try:
                User.objects.create_user(username=username, password=password, date_joined=register_time, email=email)
                error = '添加成功'
            except Exception:
                error = '添加失败'
    context = {
        'form': f,
        'error': error,
    }
    return render(request, 'accounts/register.html', context)

@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')
