#/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Feng Guofu"

import select
import socket
import queue
import os
import json


class Ftp_server(object):
    """Ftp server"""
    def __init__(self, ip, port):
        '''
        构造函数
        :param ip: 监听IP
        :param port: 监听端口
        :return:
        '''
        self.server = socket.socket()
        self.host = ip
        self.port = port
        self.msg_dic = {}  # 存队列
        self.inputs = [self.server,]  # 交给select检测的列表。没有其他连接之前，检测自己。
        self.outputs = []  # 你往里面放什么，下一次就出来了
        self.file_flag = {}  # 存客户端下载文件临时传输信息
        self.file_up_flag = {}  # 存客户端上传文件的文件名


    def start(self):
        '''
        主启动函数
        :return:
        '''
        self.server.bind((self.host,self.port))
        self.server.listen(1000)
        self.server.setblocking(False)  # 设置成非阻塞模式，accept和recv都非阻塞
        while True:
            readable, writeable, exceptional = select.select(self.inputs, self.outputs, self.inputs)  # 定义检测
            for r in readable:
                self.readable(r)
            for w in writeable:  # 要返回给客户端的连接列表
                self.writeable(w)
            for e in exceptional:  # 如果连接断开，删除连接相关数据
                self.clean(e)


    def readable(self, ser):
        '''
        处理活动的从客户端传来的数据连接
        :param ser: socket server自己
        :return:
        '''
        if ser is self.server:  # 有数据，代表来了一个新连接
            conn, addr = self.server.accept()
            print("来了个新连接",addr)
            self.inputs.append(conn)  # 把连接加到检测列表里，如果这个连接活动了，就说明数据来了
            self.msg_dic[conn] = queue.Queue()  # 初始化一个队列，后面存要返回给这个客户端的数据
        else:
            try :
                data = ser.recv(1024)  # 注意这里是r，而不是conn，多个连接的情况
                cmd = data.decode()
                cmd_str = cmd.split()[0]  # 获取命令
                if len(cmd.split()) == 2 and hasattr(self, cmd_str):
                    print("收到指令：",cmd)
                    filename = cmd.split()[1]
                    func = getattr(self, cmd_str)
                    func(ser, filename)
                else:  # 如果不存在方法，说明传输是文件数据
                    self.upload(ser, data)
            except ConnectionResetError as e:  # 抓住客户端下载一半断开的异常
                print("客户端断开了",ser)
                self.clean(ser)
            except UnicodeDecodeError as e :  # 当解码错误，说明传输是数据
                self.upload(ser, data)


    def writeable(self, conn):
        '''
        处理活动的传回客户端的数据连接
        :param conn: 客户端连接
        :return:
        '''
        try :
            data_to_client = self.msg_dic[conn].get()  # 在字典里取数据
            conn.send(data_to_client)  # 返回给客户端
        except Exception as e :
            print("客户端异常端口，传输中断")
            self.clean(conn)
            del self.file_flag[conn]
        else:
            self.outputs.remove(conn)  # 删除这个数据，确保下次循环的时候不返回这个已经处理完的连接了。
            filename = self.file_flag[conn][2]
            size = self.file_flag[conn][0]
            trans_size = self.file_flag[conn][1]
            if trans_size < size :  # 如果没有传完，继续传输
                self.load(conn, filename, size)
            else:  # 传完，则删除传输记录信息
                del self.file_flag[conn]


    def clean(self, conn):
        '''
        连接完成，收尾处理工作
        :param conn: 客户端连接
        :return:
        '''
        if conn in self.outputs:
            self.outputs.remove(conn)  # 清理已断开的连接
        if conn in self.inputs:
            self.inputs.remove(conn)  # 清理已断开的连接
        if conn in self.msg_dic:
            del self.msg_dic[conn]   # 清理已断开的连接


    def put(self, conn, filename):
        '''
        客户端上传函数
        :param conn: 客户端连接
        :param filename: 上传文件名
        :return:
        '''
        if filename == "done(status:200)":  # 收到客户端上传结束指令
            f = self.file_up_flag[conn]
            f.close()
            del self.file_up_flag[conn]  # 上传结束，清理上传文件名
        else :
            if os.path.isfile(filename):
                self.rename(filename,filename+'.bak')
            print("开始接收文件数据……")
            conn.send(b'200')  # 准备接收数据
            self.file_up_flag[conn] = filename  # 放上传文件到文件上传列表


    def upload(self, conn, data):
        '''
        客户端上传，数据接收函数
        :param conn: 客户端连接
        :param data: 客户端上传数据
        :return:
        '''
        if conn in self.file_up_flag:  # 如果已建立连接，则接收数据
            filename = self.file_up_flag[conn]
            f = open(filename, 'ab')
            f.write(data)


    def get(self, conn, filename):
        '''
        客户端下载函数
        :param conn: 客户端连接
        :param filename: 下载文件名
        :return:
        '''
        msg_dic = {  # 下载文件信息
            "action" : "get",
            "filename" : filename,
            "size" : None,
            "status" : 550
        }
        if os.path.isfile(filename):
            size = os.stat(filename).st_size
            msg_dic['size'] = size
            msg_dic['status'] = 200
        conn.send(json.dumps(msg_dic).encode('utf-8'))
        if msg_dic['status'] == 200:  # 如果文件存在，调用load，放文件内容到队列里
            self.load(conn, filename, size)


    def load(self, conn, filename, size):
        '''
        客户端下载，数据传输函数
        :param conn:
        :param filename:
        :param size:
        :return:
        '''
        if conn in self.file_flag:  # 存在下载记录，记录已传输位置
            trans_size = self.file_flag[conn][1]
        else:  # 第一次下载，传输文件
            trans_size = 0
        with open(filename, "rb") as f:
            f.seek(trans_size)  # seek到已传数据位置
            data = f.readline()
            self.msg_dic[conn].put(data)  # 放数据到队列
            self.outputs.append(conn)
            trans_size += len(data)
            self.file_flag[conn] = [size, trans_size, filename]  # 记录文件传输信息


    def rename(self,old_name, new_name):
        '''
        重命名
        :param old_name:
        :param new_name:
        :return:
        '''
        if os.path.exists(new_name):  # 判断文件是否存在
            os.remove(new_name)		# 删除文件
        os.rename(old_name, new_name)


def main():
    ip, port = 'localhost',9000
    ftp = Ftp_server(ip, port)
    ftp.start()