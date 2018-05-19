#!/usr/bin/env python
# encoding: utf-8
'''
@author: Limz
@mail: limz@yisa.com
@name: paramiko_ssh.py
@time: 2018/3/20 10:57
@Description:
'''

import paramiko
from pymongo import MongoClient
import pymongo
import time
import os
def ssh(ip,password,port,cmdlist):
    try:
        # 创建SSH对象
        result = []
        ssh = paramiko.SSHClient()
        # 允许连接不在know_hosts文件中的主机
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 连接服务器
        ssh.connect(hostname=ip, port=port, username='root', password=password, timeout=5)
        # 执行命令
        for cmd in cmdlist:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            # 获取命令结果
            result1 = stdout.read()
            result.append(result1)
        ssh.close()
        return result
    except Exception, e:
        result = ['error']
        return result

#c = ssh('192.168.43.221', 'yisa123456', '22', ['hostname','df -h|awk \'{print $2,$5,$6}\'|grep -vE \'(/dev|/run|/sys|Use|/boot)\''])
#print c

class GetSysData(object):
    collection = 'sysinfo'

    def __init__(self, ip, monitor_item, timing=3600, no=0):
        self.ip = ip
        self.monitor_item = monitor_item
        self.timing = timing
        self.no = no

    @classmethod
    def connect_db(cls):
        mongodb_ip = '192.168.171.200'
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
#if __name__ == "__main__":
#    ip = "192.168.171.1"
#    client = GetSysData(ip, "disks")
#    a = client.get_diskwarndata()
#    print a
#    for i in a:
#        print i
#    server = "192.168.171.200"
#    result = os.system('ping 192.168.171.200')
#    print result