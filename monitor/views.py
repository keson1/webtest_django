# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from pymongo import MongoClient
import json, time
from cmdb.models import Nodes, Projects

def index(request):
    projectall = Projects.objects.all()
    projectdic = {}
    for project in projectall:
        nodes = project.nodes_set.all()
        ips = {}
        for node in nodes:
            ips[node.nodename] = node.ipaddr
        projectdic[project.projectname] = ips
    ipall = Nodes.objects.all()
    print projectdic
    return render(request,"monitor/index.html",{"ipall":ipall, "projectall":projectdic})

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
            print 1
            collection1 = db["warninfo"]
            warndata["ip"] = received_json_data["ip"]
            warndata["warntype"] = "mem"
            warndata["warndata"] = received_json_data['memory']['percent']
            warndata["timestamp"] = received_json_data['timestamp']
            collection1.insert_one(warndata)
        for disk in received_json_data["disks"]:
            if int(disk['percent']) > 80:
                print 2
                collection1 = db["warninfo"]
                warndata["ip"] = received_json_data["ip"]
                warndata["warninfo"] = "disk"
                warndata["warndata"] = disk['percent']
                warndata["mountpoint"] = disk['mountpoint']
                warndata["timestamp"] = received_json_data['timestamp']
                collection1.insert_one(warndata)
        return HttpResponse("Post the system Monitor Data successfully!")
    else:
        return HttpResponse("Your push have errors, Please Check your data!")

def received_warning_info(request):
    if request.method == 'POST':
        received_json_data = json.loads(request.body)
        ip = received_json_data["ip"]
        received_json_data['timestamp'] = int(time.time())
        client = GetSysData.connect_db()
        db = client["warninginfo"]
        collection = db[ip]
        collection.insert_one(received_json_data)
        return HttpResponse("Post the Warning Data successfully!")
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
    data = {"newesttime": newesttime, "usepercent": usepercent, "availablepercent":availablepercent, "memtotal":memtotal}
    return HttpResponse(json.dumps(data))

def get_disk(request, ip, partition):
    data_time = ""
    disk_percent = ""
    disk_name = ""
    disktotal = ""
    disk = GetSysData(ip, "disks")
    for doc in disk.get_data():
        unix_time = doc['timestamp']
        times = time.localtime(unix_time)
        dt = time.strftime("%m-%d %H:%M", times)
        data_time=dt
        d_percent = doc['disks'][int(partition)]['percent']
        disk_percent=d_percent
        disk_name = doc['disks'][int(partition)]['mountpoint']
        disktotal = doc['disks'][int(partition)]['total']/1024
    availablepercent = 100 - disk_percent
    data = {"datatime": data_time, "diskname": disk_name, "diskpercent": disk_percent,"avadiskpercent":availablepercent, "disktotal": disktotal}
    return HttpResponse(json.dumps(data))

def get_cpu(request, ip):
    cpu_percent = []
    data_time = []
    cpu_data = GetSysData(ip, "cpuusage")
    for doc in cpu_data.get_data():
        unix_time = doc['timestamp']
        times = time.localtime(unix_time)
        dt = time.strftime("%m-%d %H:%M", times)
        data_time.append(dt)
        c_percent = str(doc['cpuusage'])
        cpu_percent.append(c_percent)
    newesttime = data_time[-1]
    data = {"newesttime": newesttime, "cpupercent": cpu_percent}
    return HttpResponse(json.dumps(data))