#/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Feng Guofu"
import json
import os


def json_w(file,obj):
    '''
    json系列化写入数据
    :param file: 写入文件
    :param obj: 序列化的数据
    :return:
    '''
    with open(file, 'w') as f:
        json.dump(obj,f)


def json_r(file):
    '''
    json序列化读取数据
    :param file: json读取文件
    :return: json下载 对象
    '''
    with open(file,'r') as f:
        obj = json.load(f)
    return obj


if __name__ == '__main__':
    # 如果不存在配置文件，
    host_file = 'hosts.json'
    if not os.path.exists(host_file):
        hosts = {
            'web':[
                {'ip':'192.168.0.55', 'port':22,'user':'root','password':'Ijylyz27'},
                {'ip':'192.168.0.56', 'port':22,'user':'root','password':'123456'},
                {'ip':'192.168.0.170','port':22,'user':'root','password':'1234qwer'},
            ],
            'db':[
                {'ip':'172.17.0.10', 'port':22,'user':'root','password':'liyanhong'},
                {'ip':'172.17.0.11', 'port':22,'user':'root','password':'mahuateng'},
                {'ip':'172.17.0.12', 'port':22,'user':'root','password':'mayun'},
            ],
            'test':[
                {'ip':'192.168.8.140', 'port':22,'user':'root','password':'abc123'},
                {'ip':'192.168.8.130', 'port':22,'user':'root','password':'fengguofu'},
                {'ip':'192.168.8.131', 'port':22,'user':'root','password':'jslzya'},
            ],
        }
        json_w(host_file, hosts)
        print("已生成主机列表新配置文件。")
    else:
        print("配置文件未改动，如需更改请删除原文件")

