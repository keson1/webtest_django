# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from cmdb.models import Projects, Nodes

@login_required()
def main(request):
    projectlist = []
    projectcount = Projects.objects.count()
    nodecount = Nodes.objects.count()
    projects = Projects.objects.all()
    for project in projects:
        projectname = project.projectname
        projectid = project.id
        projectdata = {"projectname":projectname, "projectid": projectid}
        projectlist.append(projectdata)
    username = request.user.username
    return render(request, 'main/main.html', {'username': username, 'projectlist': projectlist, "projectcount": projectcount, "nodecount": nodecount})

@login_required()
def index(request):
    username = request.user.username
    return render(request, 'main/main.html', {'username': username})