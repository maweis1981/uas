#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py
 
Created by wenzhenwei on 2012-03-29.
Copyright (c) 2012 snda inc. All rights reserved.
"""
import os,sys

sys.path.append(os.path.dirname(os.getcwd()))

print sys.path

import conf

print conf.uasconf.LOGPATH
