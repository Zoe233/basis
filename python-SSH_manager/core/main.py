#/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Feng Guofu"

import os
import sys
import threading
from conf.settings import json_r
from log.logger import log
from .ssh_connect import ssh_conn
from .transmission import ssh_trans


class SSH(object):
    '''执行命令、发送文件'''
    def __init__(self, host_list):
        '''
        构造函数
        :param host_list: 主机列表
        :return:
        '''
        self.host_list = host_list


    def ssh_public(self,task):
        '''
        统一任务分配
        :param task: 任务指令
        :return:
        '''
        while True:
            if task == 'cmd':
                command = input("请输入执行命令(q:返回)：\n>>> ").strip()
                # 输入命令为空，一直输入
                while not command:
                    command = input(">>> ").strip()
                if command == "q" : break
            elif task == 'trans':
                local = input("请输入上传文件的路径(q:返回)：\n>>> ").strip()
                # 输入命令为空，一直输入
                while not local:
                    local = input(">>> ").strip()
                if local == 'q': break
                # 当输入文件不存在，继续输入
                while not os.path.exists(local):
                    print("输入文件不存在。")
                    local = input("请输入上传文件的路径：\n>>> ").strip()
                print("\033[32m远程路径格式：（路径+文件名）\033[0m默认上传到用户宿主目录……")
                remote = input("文件到远程的路径(q:返回)\n>>> ").strip()
                if remote == 'q': break

            t_objs = []
            for i in range(len(self.host_list)):
                host = self.host_list[i]
                ip,port,user,passwd = host['ip'],host['port'],host['user'],host['password']
                if task == 'cmd':
                    log(ip,"执行命令：%s"%command)  # 写入日志
                    t = threading.Thread(target=ssh_conn, args=(ip,port,user,passwd,command))
                elif task == 'trans':
                    log(ip,"上传文件：%s到%s"%(local,remote))  # 写入日志
                    t = threading.Thread(target=ssh_trans, args=(ip,port,user,passwd,local,remote))
                t.start()
                t_objs.append(t)

            print("\033[5;32;1m任务执行中，请等待……\033[0m")
            for t in t_objs:
                t.join()  # t.wait() 等待

    def cmd(self):
        '''
        执行命令
        :return:
        '''
        self.ssh_public('cmd')

    def trans(self):
        '''
        传输文件
        :return:
        '''
        self.ssh_public('trans')


def login():
    '''
    用户登录
    :return: 用户登录状态
    '''
    print("\033[32m*\033[0m"*30)
    print("\033[32m*\t\t简易主机管理系统\033[0m")
    print("\033[32m*\033[0m"*30)
    username = input("请输入用户名：\n>>> ").strip()
    password = input("请输入密码：\n>>> ").strip()
    if username == "admin" and password == "admin":
        print("\033[32;1m你已成功登录主机管理系统……\033[0m")
        log("Manage_platform","登录成功")
        return True
    else:
        print("用户名或密码错误……")
        return False


def main():
    '''
    主函数
    :return:
    '''
    # 如果账户密码错误，一直循环
    n = 0
    while not login():
        n += 1
        # 三次错误退出
        if n > 2: break

    hosts = json_r('conf'+os.sep+'hosts.json')
    while True:
        # 临时存放序号和对应主机组
        print("*"*30)
        print("*\t\t当前主机组：")
        print("*"*30)
        nums = {}
        # 打印主机分组信息
        for index,item in enumerate(hosts):
            print("*%9s %10s" %(index,item))
            nums[index] = item
        print("*"*30)
        choice = input("请选择操作分组的序号（q:退出）\n>>> ").strip()
        if choice == 'q': sys.exit()
        # 选择正常，准备打印主机IP
        elif choice.isdigit() and int(choice) in nums:
            choice = int(choice)
            item = nums[choice]
            print("*"*30)
            print("*\t\t",item,'主机：')
            # 如果存在主机信息，打印
            if hosts[item]:
                print("*"*30)
                for key in hosts[item]:
                    print("*\t\t",key['ip'])
                print("*"*30)
                while True:
                    print("功能选项：\n\t\t0\t\t执行命令 \n\t\t1\t\t传输文件 \n\t\t2\t\t返回上级 ")
                    choice = input("请输入选择操作序号：\n>>> ").strip()
                    # 创建SSH实例
                    ssh = SSH(hosts[item])
                    func = {'0':ssh.cmd, '1':ssh.trans}
                    if choice == '2':
                        break
                    elif choice in func:
                        func[choice]()
                    else:
                        print("序号输入错误")
            # 不存在主机条目：打印空
            else: print("\033[31m%s 主机列表为空……\033[0m"%item)
        else:
            print("序号输入错误")
