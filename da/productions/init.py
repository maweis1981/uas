#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py
 
Created by wenzhenwei on 2012-03-29.
Copyright (c) 2012 snda inc. All rights reserved.
"""

import os,sys,inspect
import logging

curFilePath = os.path.abspath(os.path.dirname(inspect.stack()[1][1]))
sys.path.append(os.path.dirname(curFilePath))

'''
import conf


# init logger
logger = logging.getLogger("dalogger")
formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(message)s')
file_handler = logging.FileHandler(conf.daconf.LOGPATH + "/da.log")
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler(sys.stderr)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

logger.setLevel(logging.DEBUG)

logging.basicConfig(filename = conf.daconf.LOGPATH + "/da.log", format='%(name)-12s %(asctime)s %(levelname)-8s %(message)s', level=logging.DEBUG)

from conf.daconf import LOCALADDR


# init Pyro
#import Pyro4
#Pyro4.locateNS(host="192.168.91.216", port=9090)
PYRONSADDR = "192.168.91.48"
PYRONSPORT = 9999

'''
#init mysql
MYSQLADDR = "localhost"
#MYSQLADDR = "192.168.91.171"
MYSQLPORT = 3306
MYSQLUSER = "root"
MYSQLPWD = "idea"

