# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http.response import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from models import Projects, Nodes
from paramiko_ssh import ssh

def projectadd(request):
    tips = ''
    if request.method == 'POST':
        name = request.POST.get('projectname', '')
        remark = request.POST.get('remark', '')
        is_exist = Projects.objects.filter(projectname=name)
        if is_exist:
            tips = 'existed'
        else:
            r = Projects(projectname=name, remark=remark)
            r.save()
            tips = 'ok'
    return JsonResponse({'tips': tips})

@login_required()
def projectmanage(request):
    r = Projects.objects.all()
    return render(request,"cmdb/projectmanage.html",{'project':r})

def projectdel(request):
    id = request.GET.get('id','')
    try:
        r = Projects.objects.filter(pk=id)
        r.delete()
        tips = 'success'
    except Exception:
        tips = ''
    return JsonResponse({'tips': tips})

def projectmod(request):
    id = request.GET.get('id', '')
    projectname = request.GET.get('projectname', '')
    remark = request.GET.get('remark', '')
    q1 = Projects.objects.filter(projectname=projectname)
    q2 = q1.exclude(pk=id)
    #print q2
    if q2:
        tips = 'existed'
    else:
        try:
            r = Projects.objects.get(pk=id)
            r.projectname = projectname
            r.remark = remark
            r.save()
            tips = 'success'
        except Exception as e:
            #print e
            tips = ''
    return JsonResponse({'tips':tips})

@login_required()
def assetinfo(request):
    id = request.GET.get('id', '')
    projectlist = Projects.objects.all()
    if id:
        p = Projects.objects.get(pk=id)
        nodes = p.nodes_set.all()
        project = {'id': p.id, 'projectname': p.projectname}
    else:
        project = {'id': 0,'projectname': '请选择项目'}
        nodes = {}
    return render(request,"cmdb/assetinfo.html",{'projectlist': projectlist, 'project': project,'nodes': nodes})

def nodeadd(request):
    projectid = request.GET.get('projectid', '')
    ip = request.GET.get('ip', '')
    port = request.GET.get('port', '')
    pwd = request.GET.get('pwd', '')
    nodename = request.GET.get('nodename', '')
    num = request.GET.get('num', '')
    pos = request.GET.get('pos', '')
    rem = request.GET.get('rem', '')
    time = request.GET.get('time', '')
    #print projectid, ip, port, pwd, nodename
    p = Nodes.objects.filter(project_id=int(projectid))
    is_exist = p.filter(ipaddr=ip)
    if is_exist:
        tips = 'existed'
    else:
        try:
            r = Nodes(project_id=projectid, ipaddr=ip, sshport=port, rootpwd=pwd, nodename=nodename, asset_num=num, position=pos, remark=rem, up_time=time)
            r.save()
            tips = 'success'
        except Exception as e:
            print e
            tips = 'error'
    return JsonResponse({'tips': tips})

def nodedel(request):
    id = request.GET.get('id','')
    try:
        r = Nodes.objects.filter(pk=id)
        r.delete()
        tips = 'success'
    except Exception:
        tips = ''
    return JsonResponse({'tips': tips})

def nodemod(request):
    id = request.GET.get('id', '')
    projectid = request.GET.get('projectid', '')
    port = request.GET.get('port', '')
    pwd = request.GET.get('pwd', '')
    ip = request.GET.get('ip', '')
    nodename = request.GET.get('nodename', '')
    q1 = Nodes.objects.filter(ipaddr=ip)
    print q1
    q2 = q1.exclude(pk=id)
    print q2
    if q2:
        tips = 'existed'
    else:
        try:
            r = Nodes.objects.get(pk=id)
            r.project_id = projectid
            r.sshport = port
            r.rootpwd = pwd
            r.nodename = nodename
            r.ipaddr = ip
            r.save()
            tips = 'success'
        except Exception as e:
            #print e
            tips = ''
    return JsonResponse({'tips':tips})

def collectdevinfo(request):
    cmdlist = ['dmidecode |grep -A16 \'System Information$\'|grep -E \'Manufacturer|Product\'',  # 厂商
               'dmidecode -t 4 |grep Version | uniq',  # cup
               'dmidecode -t 17 | grep \'Size:\'|grep -v \'No Module Installed\'',  # 内存
               '/usr/bin/lsusb |grep Aladdin |wc -l',  # 加密狗
               'cat /proc/scsi/scsi | grep \'Model:\'',  # 硬盘厂商
               'fdisk -l | grep \'Disk /dev/s\'|awk -F\' \' \'{print $2 $3 $4}\'']  # 硬盘
    info = Nodes.objects.all()
    tips = ''
    for i in info:
        ip = i.ipaddr
        port = i.sshport
        pwd = i.rootpwd
        id = i.id
        devinfo = ssh(ip, pwd, port, cmdlist)
        if devinfo[0] == 'error':
            vender = 0
            cpu_model = 0
            mem = 0
            aladdin = 0
            disk_vender = 0
            disk = 0
        else:
            vender = devinfo[0].replace('\t','').strip().replace('\n', '')
            cpu_model = devinfo[1].replace('\t','').strip().replace('\n', '')
            mem = devinfo[2].replace('\t','').strip().replace('\n', '')
            aladdin = devinfo[3].strip()
            disk_vender = devinfo[4].replace('\t','').strip().replace('\n', '')
            disk = devinfo[5].strip()
        #print id, vender,cpu_model,mem,aladdin,disk_vender,disk
        try:
            r = Nodes.objects.get(pk=id)
            r.vendor = vender
            r.cpu_model = cpu_model
            r.memory = mem
            r.aladin = aladdin
            r.disk_vender = disk_vender
            r.disk = disk
            r.save()
            tips = 'success'
        except Exception as e:
            tips = 'error'
    return JsonResponse({'tips': tips})

def selectdevinfo(request):
    id = request.GET.get('id','')
    r = Nodes.objects.get(pk=id)
    res = {'ip':r.ipaddr, 'nodename':r.nodename, 'assetnum': r.asset_num, 'vendor':r.vendor, 'up_time': r.up_time, 'cpu_model':r.cpu_model,'cpu_num':r.cpu_num,
        'memory':r.memory, 'disk':r.disk, 'disk_vendor':r.disk_vender, 'aladin':r.aladin, 'position':r.position}
    return JsonResponse(res)



