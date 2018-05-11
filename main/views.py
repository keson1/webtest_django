# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required()
def main(request):
    username = request.user.username
    return render(request, 'main/main.html', {'username': username})

def index(request):
    return render(request, 'main/index.html')