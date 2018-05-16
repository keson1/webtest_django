#!/usr/bin/env python
# -*- coding: utf-8 -*-
import psutil
from subprocess import Popen, PIPE
import datetime, os
import socket, json, logging
import schedule, time
import requests, threading

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
#ip
def get_ip():
    try:
        hostname = socket.getfqdn(socket.gethostname())
        ipaddr = socket.gethostbyname(hostname).replace('.','')
    except Exception as msg:
        print(msg)
        ipaddr = ''
    return ipaddr

#设置日志
def log(log_name, path=None):
    logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(levelname)s %(message)s',
                datefmt='%Y%m%d %H:%M:%S',
                filename=path+log_name,
                filemode='ab+')
    return logging.basicConfig

#post数据函数
def post_data(url, data):
    try:
        r = requests.post(url, data)
        if r.text:
            logging.info(r.text)
        else:
            logging.info("Server return http status code: {0}".format(r.status_code))
    except Exception as msg:
        logging.info(msg)
    return True

server_ip = '192.168.1.8'
log("agent.log","/root/")

#收集系统信息
def collect_info_post():
    logging.info('Get the system infos from host:')
    mem = {'total':get_mem.total,'percent':get_mem.percent}
    sys_info = {'boottime': get_boottime(),
                'cpuusage': get_cpu(),
                'memory': mem, 
                'disks': get_disk(),
                'ip': get_ip(),  
               }   
    logging.info(sys_info)
    json_data = json.dumps(sys_info)
    logging.info('----------------------------------------------------------')
    post_data("http://{0}/monitor/received/sys/info/".format(server_ip), json_data)
    return True

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

def get_pid():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    pid = str(os.getpid())
    with open(BASE_DIR+"/adminsetd.pid", "wb+") as pid_file:
        pid_file.writelines(pid)

if __name__ == "__main__":
    get_pid()
    collect_info_post()
    schedule.every(300).seconds.do(run_threaded, collect_info_post)
    while True:
        schedule.run_pending()
        time.sleep(1)

