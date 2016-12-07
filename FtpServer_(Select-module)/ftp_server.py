#/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Feng Guofu"

import os
from core.ftp_server import main

DATA_DIR = 'data'+os.sep+'server_data'
os.chdir( DATA_DIR )  # 切换到数据存放目录

main()