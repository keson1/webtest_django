#!/usr/bin/env python
# -*- coding: utf-8 -*-
import psutil
from subprocess import Popen, PIPE
import datetime

#cpu信息
def get_cpu():
    cpu_time = psutil.cpu_times_percent(interval=1)
    percent = psutil.cpu_percent(interval=1)
    return percent

#内存信息
class get_mem():
    mem = psutil.virtual_memory()
    used = mem.used/1024/1024
    percent = mem.percent
    total = mem.total/1024/1024
    available = mem.available

#磁盘信息
def get_disk():
    disks = []
    partitions = psutil.disk_partitions()
    for disk in partitions:
        info = {}
        if disk.mountpoint == '/boot':
            continue
        total = psutil.disk_usage(disk.mountpoint).total/1024/1024
        percent = psutil.disk_usage(disk.mountpoint).percent
        info['mountpoint'] = disk.mountpoint
        info['total'] = total
        info['percent'] = percent
        disks.append(info)
    return disks

#系统启动时间
def get_boottime():
    boottime =  datetime.datetime.fromtimestamp(psutil.boot_time ()).strftime("%Y-%m-%d %H:%M:%S")
    return boottime


#收集系统信息
def collect():
    sys_info = {'boottime': get_boottime(),
                'cpuusage': get_cpu(),
                'memtotal': get_mem.total, 
                'memusage': get_mem.percent,
                'disks': get_disk(),  
               }
    print sys_info


collect()
