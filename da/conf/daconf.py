#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py
 
Created by wenzhenwei on 2012-03-29.
Copyright (c) 2012 snda inc. All rights reserved.
"""

import os,sys,inspect

def script_path():
	caller_file = inspect.stack()[1][1]         # caller's filename
	return os.path.abspath(os.path.dirname(caller_file))# path
DAROOT = os.path.dirname(script_path())
LOGPATH = DAROOT + "/log"
CONFPATH = DAROOT + "/conf"


import socket
import struct

'''
import fcntl
def get_ip_address(ifname='eth0'):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	return socket.inet_ntoa(fcntl.ioctl(
	    s.fileno(),
	    0x8915,  # SIOCGIFADDR
	    struct.pack('256s', ifname[:15])
	)[20:24])
LOCALADDR = get_ip_address()
'''

LOCALADDR = '127.0.0.1'
