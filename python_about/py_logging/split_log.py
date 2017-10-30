#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author : mj
"""分割形式有两种：RotatingFileHandler（按照文件大小分割）、TimedRotatingFileHandler（按照时间间隔分割）"""
import time
import logging
import logging.handlers
logging.basicConfig()
myapp = logging.getLogger('myapp')
myapp.setLevel(logging.INFO)
filehandler = logging.handlers.TimedRotatingFileHandler("D:/python_zhanyong/git_branch_mj/a01/myapps.log", when='S', interval=1, backupCount=40)
filehandler.suffix = "%Y-%m-%d_%H-%M-%S.log"
myapp.addHandler(filehandler)

for i in range(50):
    time.sleep(0.1)
    # time.sleep(1)
    myapp.info(str(i)+",test")