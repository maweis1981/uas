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
WEBROOT = os.path.dirname(script_path())
LOGPATH = WEBROOT + "/log"
CONFPATH = os.getcwd()

