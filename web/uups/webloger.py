#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py
 
Created by wenzhenwei on 2012-03-29.
Copyright (c) 2012 snda inc. All rights reserved.
"""

import logging  
import sys

def init:
	logger = logging.getLogger("uas_web_log")  
	formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(message)s')  
	file_handler = logging.FileHandler("uas_web.log") 
	file_handler.setFormatter(formatter)
	stream_handler = logging.StreamHandler(sys.stderr)  
	logger.addHandler(file_handler)
	logger.addHandler(stream_handler)
