#!/usr/bin/env python
# encoding: utf-8
'''
@author: Limz
@mail: limz@yisa.com
@name: urls.py
@time: 2018/5/16 23:07
@Description:
'''


from django.conf.urls import url
import views

urlpatterns=[
    url(r'^system/$', views.index, name='monitor'),
    #url(r'^manage/del/all/$', manage.drop_sys_info, name='drop_all'),
    #url(r'^manage/del/range/(?P<timing>[0-9])/$', manage.del_monitor_data, name='del_monitor_data'),
    #url(r'^manage/$', manage.index, name='monitor_manage'),
    url(r'^system/(?P<ip>.+)/$', views.host_info, name='host_info'),
    url(r'^get/cpu/(?P<ip>.+)/$', views.get_cpu, name='get_cpu'),
    url(r'^get/mem/(?P<ip>.+)/$', views.get_mem, name='get_mem'),
    url(r'^get/disk/(?P<ip>.+)/(?P<partition>\d+)/$', views.get_disk, name='get_disk'),
    url(r'^received/sys/info/$', views.received_sys_info, name='received_sys_info'),
    url(r'^received/page/info/$', views.received_page_info, name='received_page_info'),
    url(r'^diskwarn/$', views.diskwarn, name='diskwarn'),
    url(r'^memwarn/$', views.memwarn, name='memwarn'),
    url(r'^pingwarn/$', views.pingwarn, name='pingwarn'),
    url(r'^memwarnchart/$', views.memwarnchart, name='memwarnchart'),
    url(r'^diskwarnchart/$', views.diskwarnchart, name='diskwarnchart'),
    url(r'^pingwarnchart/$', views.pingwarnchart, name='pingwarnchart'),
]



