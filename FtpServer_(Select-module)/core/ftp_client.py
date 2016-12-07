#/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Feng Guofu"

import socket
import json
import sys
import os
import time
from model.prettytable import PrettyTable


class Ftp_client(object):
    """FTP 客户端"""
    def __init__(self):
        '''
        构造函数
        :return:
        '''
        self.client = socket.socket()


    def start(self):
        '''
        主启动函数
        :return:
        '''
        while True:
            cmd = input('>>> ').strip()
            if len(cmd) == 0 : continue

            cmd_str = cmd.split()[0]  # 获取命令
            if len(cmd.split()) == 2 and hasattr(self, cmd_str):
                func = getattr(self, cmd_str)
                func(cmd)
            else:  # 或使用：pprint.pprint(sys.path) pprint模块格式化数据
                cmd_help = PrettyTable([' 支持命令 ',' 命令说明 '])
                cmd_help.add_row(['put filename','上传文件'])
                cmd_help.add_row(['get filename','下载文件'])
                print('\033[32m%s\033[0m' %cmd_help)

    def put(self, cmd):
        '''
        客户端上传函数
        :param cmd: 上传命令
        :return:
        '''
        filename = cmd.split()[1]
        if os.path.isfile(filename):
            self.client.send(cmd.encode('utf-8'))
            # 防止粘包，等服务器确认
            server_response = self.client.recv(1024).decode()
            trans_size = 0
            file_size = os.stat(filename).st_size
            if file_size == 0 :
                print("禁止上传空文件！")
            else:
                n = 0
                with open(filename, 'rb') as f:
                    for line in f:
                        self.client.send(line)
                        trans_size += len(line)
                        # 调用进度条函数
                        if trans_size == file_size: n = 100  # 如果文件只一行，进度条满格
                        n = self.progress(trans_size,file_size,n)
                    else:
                        time.sleep(0.5)  # 发送结束指令前，防止粘包，则指令无效
                        print("\n文件上传完成。 文件大小：[%s]字节" %trans_size)
                        self.client.send(b'put done(status:200)')  # 告诉服务端上传完成
        else :
            print("上传文件不存在……")


    def get(self, cmd):
        '''
        客户端下载函数
        :param cmd: 下载命令
        :return:
        '''
        self.client.send(cmd.encode('utf-8'))
        data = self.client.recv(1024)
        file_msg = json.loads(data.decode())
        file_status = file_msg['status']
        filename = file_msg['filename']
        if file_status == 550:
            print("下载文件不存在……")
        elif file_status == 200:
            receive_size = 0
            file_size = file_msg['size']
            n = 0
            with open(filename, 'wb') as f:
                while receive_size < file_size:
                    data = self.client.recv(1024)
                    f.write(data)
                    receive_size += len(data)
                    # 调用进度条函数
                    if receive_size == file_size: n = 100
                    n = self.progress(receive_size,file_size,n)
                else:
                    print("\n文件下载完成。大小：%s 字节"%receive_size)


    def progress(self,current,total,num):
        '''
        显示传输进度
        :param current: 当前已传输大小
        :param total: 总大小
        :param num: 打印‘#’个数
        :return num: # 个数
        '''
        if current/total*100 >= num:
            view = '\r[%-50s]%d%%'%('#'*int(num/2),num)
            sys.stdout.write(view)
            sys.stdout.flush()
            num += 1
        return num
        # 注意此处return不能在if里面，否则返回None值，程序报错


    def connect(self,ip,port):
        '''
        连接ip、端口信息
        :param ip:
        :param port:
        :return:
        '''
        self.client.connect((ip, port))


def main():
    client = Ftp_client()
    client.connect("localhost",9000)
    client.start()