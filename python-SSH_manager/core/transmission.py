#/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Feng Guofu"

import paramiko


def ssh_trans(ip, port, user, password, local, remote):
    '''
    ssh传输文件
    :param ip: IP地址
    :param port: ssh端口
    :param user: 用户名
    :param password: 密码
    :param local: 本机路径
    :param remote: 远端路径
    :return:
    '''
    # 异常处理
    try:
        # 创建连接实例
        transport = paramiko.Transport((ip,port))
        # 建立连接
        transport.connect(username=user, password=password)
        # 创建传输实例
        sftp = paramiko.SFTPClient.from_transport(transport)
    except paramiko.ssh_exception.SSHException as e:
        print("\033[31m网络错误：%s %s\033[0m" %(ip,e))
    except Exception as e:
        print("\033[31m未知错误：%s %s\033[0m" %(ip,e))
    else:
        try:
            # 将文件上传到服务器
            sftp.put(local, remote)
        except OSError as e:
            print("\033[31m%s系统IO错误：%s\033[0m"%(ip, e))
        except Exception as e:
            print("\033[31m%s操作错误：%s\033[0m"%(ip, e))
        else :
            print("\033[32;1m%s：%s文件上传成功！！！\033[0m"%(ip,local))
        finally:
            # 不能在第一级try那里用finally，因为异常，不生成transport变量
            transport.close()
