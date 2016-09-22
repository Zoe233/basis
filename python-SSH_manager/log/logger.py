#/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Feng Guofu"

import time
import os

def log(ip,describe,user='admin'):
    cur_time = time.strftime("%Y-%m-%d %X",time.localtime())
    with open('log'+os.sep+'os.log','a', encoding='utf-8') as f:
        f.write("%s%8s%18s\t%s\n" %(cur_time,user,ip,describe))
