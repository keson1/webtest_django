# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponseRedirect
from form import LoginUserForm, registerForm
from django.contrib import auth
from django.contrib.auth.models import User
import time
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, JsonResponse

def login(request):
    return render(request, "accounts/login.html")

def loginauth(request):
    f = LoginUserForm(request.POST)
    ret = {'status': False, 'reason': ''}
    if request.method == 'POST':
        if f.is_valid():
            auth.login(request, f.get_user())
            ret['status'] = True
        else:
            ret['reason'] = 'codewrong'
    return JsonResponse(ret)

def register(request):
    ret = {'status': False, 'reason': ''}
    if request.method == 'POST':
        username = request.POST.get('user', '')
        password = request.POST.get('code', '')
        email = request.POST.get('email', '')
        register_time = time.strftime("%Y-%m-%d %H:%M:%S")
        is_exist = User.objects.filter(username=username)
        if is_exist:
            ret['reason'] = 'already existed'
        else:
            try:
                User.objects.create_user(username=username, password=password, date_joined=register_time, email=email)
                ret['status'] = True
            except Exception:
                ret['reason'] = 'failed'
    return JsonResponse(ret)

@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')
