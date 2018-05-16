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
    #url(r'^system/(?P<hostname>.+)/(?P<timing>\d+)/$', system.host_info, name='host_info'),
    #url(r'^get/cpu/(?P<hostname>.+)/(?P<timing>\d+)/$', system.get_cpu, name='get_cpu'),
    #url(r'^get/mem/(?P<hostname>.+)/(?P<timing>\d+)/$', system.get_mem, name='get_mem'),
    #url(r'^get/disk/(?P<hostname>.+)/(?P<timing>\d+)/(?P<partition>\d+)/$', system.get_disk, name='get_disk'),
    #url(r'^get/net/(?P<hostname>.+)/(?P<timing>\d+)/(?P<net_id>\d+)/$', system.get_net, name='get_net'),
    url(r'^received/sys/info/$', views.received_sys_info, name='received_sys_info'),
]



