# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from pymongo import MongoClient
import pymongo
import json, time
from cmdb.models import Nodes, Projects
import os
from models import Pagedata
from datetime import datetime

def index(request):
    projectcount = Projects.objects.count()
    nodecount = Nodes.objects.count()
    projectall = Projects.objects.all()
    projectdic = {}
    memwarndatalist = memwarnchartinfo()
    diskwarndatalist = diskwarnchartinfo()
    pingwarndatalist = pingwarnchartinfo()
    for project in projectall:
        nodes = project.nodes_set.all()
        ips = {}
        for node in nodes:
            ips[node.nodename] = node.ipaddr
        projectdic[project.projectname] = ips
    return render(request,"monitor/index.html",{"projectall":projectdic, "projectcount":projectcount, "nodecount":nodecount, "memwarndatalist": memwarndatalist, "diskwarndatalist": diskwarndatalist, "pingwarndatalist": pingwarndatalist})

def received_sys_info(request):
    warndata = {}
    if request.method == 'POST':
        received_json_data = json.loads(request.body)
        ip = received_json_data["ip"]
        received_json_data['timestamp'] = int(time.time())
        client = GetSysData.connect_db()
        db = client[GetSysData.collection]
        collection = db[ip]
        collection.insert_one(received_json_data)
        if int(received_json_data['memory']['percent']) > 80:
            warndata["ip"] = received_json_data["ip"]
            warndata["warntype"] = "mem"
            warndata["warndata"] = received_json_data['memory']['percent']
            warndata["timestamp"] = received_json_data['timestamp']
            db = client["memwarninfo"]
            collection = db[ip]
            collection.insert_one(warndata)
        diskpercent = []
        mountpoint = []
        for disk in received_json_data["disks"]:
            if int(disk['percent']) > 80:
                diskpercent.append(disk['percent'])
                mountpoint.append(disk["mountpoint"])
        if diskpercent:
                warndata["ip"] = received_json_data["ip"]
                warndata["warntype"] = "disk"
                warndata["warndata"] = diskpercent
                warndata["mountpoint"] = mountpoint
                warndata["timestamp"] = received_json_data['timestamp']
                db = client["diskwarninfo"]
                collection = db[ip]
                collection.insert_one(warndata)
        return HttpResponse("Post the system Monitor Data successfully!")
    else:
        return HttpResponse("Your push have errors, Please Check your data!")

def received_page_info(request):
    if request.method == 'POST':
        received_json_data = json.loads(request.body)
        data = received_json_data["data"]
        for pageinfo in data:
            nowtime = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
            if pageinfo["passtime"] == "error" or pageinfo["totaluser"] == "error":
                status = "0"
            else:
                status = "1"
            is_exist = Pagedata.objects.filter(ip=pageinfo["ip"])
            if is_exist:
                r = Pagedata.objects.get(ip=pageinfo["ip"])
                r.region = pageinfo["region"]
                r.totaluser = pageinfo["totaluser"]
                r.totaldata = pageinfo["totaldata"]
                r.totallog = pageinfo["totallog"]
                r.passtime = pageinfo["passtime"]
                r.querytime = nowtime
                r.status = status
                r.save()
            else:
                if pageinfo["passtime"] == "error" or pageinfo["totaluser"] == "error":
                    status = "异常"
                r = Pagedata(ip=pageinfo["ip"], region=pageinfo["region"], totaluser=pageinfo["totaluser"], totaldata=pageinfo["totaldata"], totallog=pageinfo["totallog"], passtime=pageinfo["passtime"], querytime=nowtime, status=status)
                r.save()
        return HttpResponse("Post the system Monitor Data successfully!")
    else:
        return HttpResponse("Your push have errors, Please Check your data!")

class GetSysData(object):
    collection = 'sysinfo'

    def __init__(self, ip, monitor_item, timing=3600, no=0):
        self.ip = ip
        self.monitor_item = monitor_item
        self.timing = timing
        self.no = no

    @classmethod
    def connect_db(cls):
        mongodb_ip = '192.168.43.221'
        mongodb_port = '27017'
        mongodb_user = ''
        mongodb_pwd = ''
        if mongodb_user:
            uri = 'mongodb://'+mongodb_user+':'+mongodb_pwd+'@'+mongodb_ip+':'+mongodb_port+'/'+cls.collection
            client = MongoClient(uri)
        else:
            client = MongoClient(mongodb_ip, int(mongodb_port))
        return client

    def get_data(self):
        client = self.connect_db()
        db = client[self.collection]
        collection = db[self.ip]
        now_time = int(time.time())
        find_time = now_time-self.timing
        cursor = collection.find({'timestamp': {'$gte': find_time}}, {self.monitor_item: 1, "timestamp": 1}).limit(self.no)
        return cursor

    def get_diskwarndata(self):
        client = self.connect_db()
        db = client["diskwarninfo"]
        collection = db[self.ip]
        now_time = int(time.time())
        find_time = now_time-600
        cursor = collection.find({'timestamp': {'$gte': find_time}}).sort("timestamp",pymongo.DESCENDING).limit(1)
        return cursor

    def get_memwarndata(self):
        client = self.connect_db()
        db = client["memwarninfo"]
        collection = db[self.ip]
        now_time = int(time.time())
        find_time = now_time-600
        cursor = collection.find({'timestamp': {'$gte': find_time}}).sort("timestamp",pymongo.DESCENDING).limit(1)
        return cursor


def host_info(request, ip):
    # 传递磁盘号给前端JS,用以迭代分区图表
    disk = GetSysData(ip, "disks", 3600, 1)
    disk_data = disk.get_data()
    partitions_len = []
    for d in disk_data:
        p = len(d["disks"])
        for x in range(p):
            partitions_len.append(x)
    return render(request, "monitor/hostinfo.html", locals())

def get_mem(request, ip):
    data_time = []
    mem_percent = []
    memtotal = ""
    try:
        mem_data = GetSysData(ip, "memory")
        for doc in mem_data.get_data():
            unix_time = doc['timestamp']
            times = time.localtime(unix_time)
            dt = time.strftime("%m-%d %H:%M", times)
            data_time.append(dt)
            m_percent = doc['memory']['percent']
            mem_percent.append(m_percent)
            memtotal = doc['memory']['total']
        usepercent = int(mem_percent[-1])
        availablepercent = 100 - usepercent
        newesttime = data_time[-1]
    except Exception:
        newesttime = ""
        usepercent = ""
        availablepercent = ""
    data = {"newesttime": newesttime, "usepercent": usepercent, "availablepercent":availablepercent, "memtotal":memtotal}
    return HttpResponse(json.dumps(data))

def get_disk(request, ip, partition):
    data_time = ""
    disk_percent = ""
    disk_name = ""
    disktotal = ""
    try:
        disk = GetSysData(ip, "disks")
        for doc in disk.get_data():
            unix_time = doc['timestamp']
            times = time.localtime(unix_time)
            dt = time.strftime("%m-%d %H:%M", times)
            data_time=dt
            d_percent = doc['disks'][int(partition)]['percent']
            disk_percent=d_percent
            disk_name = doc['disks'][int(partition)]['mountpoint']
            disktotal = doc['disks'][int(partition)]['total']
        availablepercent = 100 - disk_percent
    except Exception:
        availablepercent = ""
    data = {"datatime": data_time, "diskname": disk_name, "diskpercent": disk_percent,"avadiskpercent":availablepercent, "disktotal": disktotal}
    return HttpResponse(json.dumps(data))

def get_cpu(request, ip):
    cpu_percent = []
    data_time = []
    try:
        cpu_data = GetSysData(ip, "cpuusage")
        for doc in cpu_data.get_data():
            unix_time = doc['timestamp']
            times = time.localtime(unix_time)
            dt = time.strftime("%m-%d %H:%M", times)
            data_time.append(dt)
            c_percent = str(doc['cpuusage'])
            cpu_percent.append(c_percent)
        newesttime = data_time[-1]
    except Exception:
        newesttime = ""
    data = {"newesttime": newesttime, "cpupercent": cpu_percent}
    return HttpResponse(json.dumps(data))

def diskwarn(request):
    data = diskwarninfo()
    return JsonResponse(data)

def diskwarninfo():
    nodeall = Nodes.objects.all()
    count = 0
    diskwarndatalist = []
    for node in nodeall:
        ip = node.ipaddr
        diskwarn = GetSysData(ip, "disks")
        for doc in diskwarn.get_diskwarndata():
            if doc:
                count += 1
                unix_time = doc['timestamp']
                times = time.localtime(unix_time)
                dt = time.strftime("%m-%d %H:%M", times)
                diskwarndata={"time":dt, "mountpoint":doc["mountpoint"], "ip":doc["ip"], "percent": doc["warndata"]}
                diskwarndatalist.append(diskwarndata)
    data = {"count": count, "warninfo": diskwarndatalist}
    return data

def memwarn(request):
    data = memwarninfo()
    return JsonResponse(data)

def memwarninfo():
    nodeall = Nodes.objects.all()
    count = 0
    memwarndatalist = []
    for node in nodeall:
        ip = node.ipaddr
        memwarn = GetSysData(ip, "mem")
        for doc in memwarn.get_memwarndata():
            if doc:
                count += 1
                unix_time = doc['timestamp']
                times = time.localtime(unix_time)
                dt = time.strftime("%m-%d %H:%M", times)
                memwarndata={"time":dt, "ip":doc["ip"], "percent": doc["warndata"]}
                memwarndatalist.append(memwarndata)
    data = {"count": count, "warninfo": memwarndatalist}
    return data

def memwarnchartinfo():
    data = memwarninfo()
    warninfo = data["warninfo"]
    warndatalist = []
    for info in warninfo:
        ip = info["ip"]
        percent = info["percent"]
        time = info["time"]
        node = Nodes.objects.get(ipaddr=ip)
        nodename = node.nodename
        projectname = node.project.projectname
        warndata = {"ip": ip, "percent": percent, "time": time, "nodename": nodename, "projectname": projectname}
        warndatalist.append(warndata)
    return warndatalist

def memwarnchart(request):
    warndatalist = memwarnchartinfo()
    return render(request,"monitor/memwarn.html",{"warndatalist": warndatalist})

def diskwarnchart(request):
    warndatalist = diskwarnchartinfo()
    return render(request,"monitor/diskwarn.html",{"warndatalist": warndatalist})

def diskwarnchartinfo():
    data = diskwarninfo()
    warninfo = data["warninfo"]
    warndatalist = []
    for info in warninfo:
        num = len(info["mountpoint"])
        for n in xrange(num):
            percent = info["percent"][n]
            mountpoint = info["mountpoint"][n]
            ip = info["ip"]
            time = info["time"]
            node = Nodes.objects.get(ipaddr=ip)
            nodename = node.nodename
            projectname = node.project.projectname
            warndata = {"ip": ip, "percent": percent, "time": time, "nodename": nodename, "projectname": projectname,
                        "mountpoint": mountpoint}
            warndatalist.append(warndata)
    return warndatalist

def pingwarninfo():
    nodes = Nodes.objects.all()
    count = 0
    errorip = []
    for node in nodes:
        ip = node.ipaddr
        result = os.system('ping '+ip+' -n 2')
        if result == 0:
            node.status = "1"
            node.save()
        else:
            node.status = "0"
            node.save()
            count += 1
            errorip.append(ip)
    data = {"count": count, "warninfo": errorip}
    return data

def pingwarn(request):
    data = pingwarninfo()
    return JsonResponse(data)

def pingwarnchartinfo():
    warndatalist = []
    nodes = Nodes.objects.filter(status=0)
    for node in nodes:
        ip = node.ipaddr
        nodename = node.nodename
        projectname = node.project.projectname
        warndata = {"ip": ip, "nodename": nodename, "projectname": projectname}
        warndatalist.append(warndata)
    return warndatalist

def pingwarnchart(request):
    warndatalist = pingwarnchartinfo()
    return render(request,"monitor/pingwarn.html",{"warndatalist": warndatalist})


