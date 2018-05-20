#!/usr/bin/env python
# encoding: utf-8
'''
@author: Limz
@mail: limz@yisa.com
@name: chashuju.py
@time: 2018/4/3 10:57
@Description:查询页面数据量，用户数，操作数。
模块说明：PageInfo：页面数据,UserInfo：用户信息数据。
属性说明：PageInfo().get_time：最后过车时间，PageInfo().get_total：当日过车数， UserInfo().get_user：用户数， UserInfo().get_op_total：操作总数
需要修改的变量web_ip:ip地址,version:版本号("1",第一版，"3",第三版)，account,password:页面登录账户密码，dbpasswd：数据库密码。
'''

import requests
from datetime import datetime
from datetime import timedelta
from lxml import etree
import time
import cookielib
import json
import threading
import os
import yaml
import re
import Queue
import sys
import MySQLdb
import logging
import schedule



class PageInfo():
    def __init__(self, account, password, web_ip, version, date):
        self.account = account
        self.password = password
        self.web_ip = web_ip
        self.version = version
        self.date = date
        self.num = 0
        self.session = requests.session()
        self.cookies_file = web_ip + ".txt"
        self.session.cookies = cookielib.LWPCookieJar(self.cookies_file)
        self.agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
        self.header = {
            'HOST': self.web_ip,
            "User_Agent": self.agent
        }

    def get_data_third(self):
        # 第三版
        pass_time = ""
        total_records = ""
        post_url = "http://%s/?c=login&m=do_login" % self.web_ip
        past_data = {
            "account": self.account,
            "password": self.password
        }
        try:
            self.session.post(post_url, data=past_data, headers=self.header, allow_redirects=True)
            self.session.cookies.save(ignore_discard=True, ignore_expires=True)
        except Exception:
            pass_time = "error"
            total_records = 0
        else:
            for t in range(self.num, -1, -1):
                t_date = self.date
                get_token_url = "http://%s/?c=api&m=get_token" % self.web_ip
                r1 = self.session.get(get_token_url, headers=self.header)
                token = json.loads(r1.text)['data'][0]['token']
                post_url1 = "http://%s/?c=api&m=deal_post_data&jump_url=inquiry_model&token=%s" % (self.web_ip, token)
                post_data1 = {"source_id": "0",
                            "brand_id": "0",
                            "model_id": "0",
                            "year_id": "0",
                            "color_id": "-1",
                            "plate_number": "",
                            "plate_type_id": "-1",
                            "begin_date": t_date,
                            "b_h": "00",
                            "b_m": "00",
                            "b_s": "00",
                            "end_date": t_date,
                            "e_h": "23",
                            "e_m": "59",
                            "e_s": "59",
                            "begin_date2": "",
                            "b_h_2": "",
                            "b_m_2": "",
                            "b_s_2": "",
                            "end_date2": "",
                            "e_h_2": "",
                            "e_m_2": "",
                            "e_s_2": "",
                            "location_id": "",
                            "region_id": ""
                            }
                self.session.post(post_url1, data=post_data1, headers=self.header, allow_redirects=False)
                get_record_url = 'http://%s/?c=inquiry_model&m=ajax_load&token=%s&jump_url=' % (self.web_ip, token)
                r3 = self.session.get(get_record_url)
                total_records = json.loads(r3.text)['totalRecords']
                try:
                    pass_time = json.loads(r3.text)['data'][0][u"captureTime"]
                except Exception as e:
                    pass_time = "error" 
        return total_records,pass_time
    
    @property
    def get_total(self):
        if self.version == 3:
            return self.get_data_third()[0] 
        else:
            return self.get_data_first()[0]

    @property
    def get_time(self):
        if self.version == 3:
            return self.get_data_third()[1]
        else:
            return self.get_data_first()[1]

    def get_data_first(self):
        # 第一版
        total_records = ""
        pass_time = ""
        post_url = "http://%s/front/index.php?c=login&m=do_login" % self.web_ip
        past_data = {
            "account": self.account,
            "password": self.password
        }
        try:
            self.session.post(post_url, data=past_data, headers=self.header)
        except Exception as e:
            total_records = 0
            pass_time = "error"
        else:
            self.session.cookies.save(ignore_discard=True, ignore_expires=True)
            for x in range(self.num, -1, -1):
                t_date = self.date
                get_url = "http://%s/front/index.php?d=inquiry&c=model_search&m=results&group=0&brand_id=0&model_id=0&year_id=0&year_show_id=0&source_id=0&isHavePlate_number=1&plate_number=&begin_date=%s&b_h=0&b_m=0&b_s=0&end_date=%s&e_h=23&e_m=59&e_s=59&location_id=" % (self.web_ip, t_date, t_date)
                r = self.session.get(get_url)
                html = etree.HTML(r.text)
                try:
                    total_records = html.xpath('//*[@id="wraps"]/div[1]/div[3]/div[1]/div[1]/div/p[2]/span[1]/text()')[0]
                    pass_time = html.xpath('//*[@id="middle"]/div[2]/ul/li[1]/p[2]/text()')[0][5:]
                except Exception as e:
                    total_records = 0
                    pass_time = "error"
        return total_records,pass_time

class UserInfo():
    def __init__(self, dbpassword, web_ip, day):
        self.dbpasswd = dbpassword
        self.web_ip = web_ip    
        self.day = day
 
    def logchaxun(self):
        try:
            conn = MySQLdb.connect(
                host=self.web_ip,
                port=3306,
                user='yisa_oe',
                passwd=self.dbpasswd,
                db='yisa_oe',
            )
            day = self.day
            sql1 = "select count(*) from user"
            sql2 = "select count(*) from user_log where account!='admin' and time_value < '%s 23:59:59'" % day
            #sql3 = "select count(*) from user_log where account!='admin' and time_value >= '%s 00:00:00' and time_value < '%s 23:59:59'" % (day,day)
    
            cur = conn.cursor()
            cur.execute(sql1)
            info = cur.fetchone()
    
            cur.execute(sql2)
            info1 = cur.fetchone()
            #cur.execute(sql3)
            #info2 = cur.fetchone()
            cur.close()
            conn.close()
            user = int(info[0])   
            log = int(info1[0])  
        except Exception:
            user = "error"
            log = "error"
        return user,log
    
    @property
    def get_user(self):
        return self.logchaxun()[0] 


    @property
    def get_op_valid(self):
        return self.logchaxun()[1]

def postgetdata():
    config_file = open(os.path.dirname(os.path.abspath(__file__)) + '/config.yaml')
    config = yaml.safe_load(config_file)
    config_file.close()
    date = datetime.strftime(datetime.now(), "%Y%m%d")
    day = datetime.strftime(datetime.now(), "%Y-%m-%d")
    datalist = []
    for i in config['third'].keys():
        pageinfo = PageInfo("admin", config['third'][i]["password"], config['third'][i]["web_ip"], 3, date)
        totaldata = pageinfo.get_total
        passtime = pageinfo.get_time
        userinfo = UserInfo(config['third'][i]["dbpassword"], config["third"][i]["web_ip"], day)
        totaluser = userinfo.get_user
        totallog = userinfo.get_op_valid
        data = {"ip": config['third'][i]["web_ip"], "region": i, "totaldata": totaldata, "passtime": passtime,
                "totaluser": totaluser, "totallog": totallog}
        datalist.append(data)
    for i in config['first'].keys():
        pageinfo = PageInfo("yisa_oe", config['first'][i]["password"], config['first'][i]["web_ip"], 1, date)
        totaldata = pageinfo.get_total
        passtime = pageinfo.get_time
        userinfo = UserInfo(config['first'][i]["dbpassword"], config["first"][i]["web_ip"], day)
        totaluser = userinfo.get_user
        totallog = userinfo.get_op_valid
        data = {"ip": config['first'][i]["web_ip"], "region": i, "totaldata": totaldata, "passtime": passtime,
                "totaluser": totaluser, "totallog": totallog}
        datalist.append(data)
    psotdata = json.dumps({"data":datalist})
    postfun(psotdata)
    return True

server_ip = "51.1.2.26:8000"
def postfun(data):
    url = "http://{0}/monitor/received/page/info/".format(server_ip)
    try:
        r = requests.post(url, data)
        if r.text:
            print(r.text)
        else:
            print("Server return http status code: {0}".format(r.status_code))
    except Exception as msg:
        print(msg)
    return True

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='out.log',
                        filemode='wb+')

    console = logging.StreamHandler()
    formatter = logging.Formatter('%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    request_log = logging.getLogger("requests.packages.urllib3")
    request_log.setLevel(logging.ERROR)
    postgetdata()
    schedule.every(300).seconds.do(run_threaded, postgetdata)
    while True:
        schedule.run_pending()
        time.sleep(1)





