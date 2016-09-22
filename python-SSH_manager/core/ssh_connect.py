#/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Feng Guofu"

import paramiko


def ssh_conn(ip, port, user, password, cmd):
    '''
    连接ssh主机，执行命令
    :param ip: IP地址
    :param port: ssh端口
    :param user: 用户名
    :param password: 密码
    :param cmd: 执行命令
    :return:
    '''
    # 创建ssh对象
    ssh = paramiko.SSHClient()
    # 允许连接不在know_hosts文件中的主机
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 异常处理
    try:
        # 连接服务器
        ssh.connect(hostname=ip, port=port, username=user, password=password)
        # 执行命令
        stdin, stdout, stderr = ssh.exec_command(cmd)
    except OSError as e:
        print("\033[31m系统错误：%s %s\033[0m" %(ip,e))
    except Exception as e:
        print("\033[31m未知错误：%s %s\033[0m" %(ip,e))
    else:
        # 获取命令结果
        stdout_result = stdout.read()
        stderr_result = stderr.read()
        result = stdout_result if stdout_result else stderr_result
        print(("\033[32;1m 主机【%s】\033[0m"%ip).center(60,"="))
        if result:
            print(result.decode())
        else:
            print("这种命令作用不大哦，亲……，请组合使用。")
    finally:
        # 关闭连接
        ssh.close()

