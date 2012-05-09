#!/usr/bin/env python
# encoding: utf-8
"""
usershowprocessor.py

Created by wenzhenwei on 2012-03-28.
Copyright (c) 2012 snda inc. All rights reserved.
"""

import sys
import os
import json

import Pyro4
import redis

from init import *

class UserShowProcessor(object):
	
	def show(self, userid, level=2, require=None):
		ns = Pyro4.locateNS(host=PYRONSADDR, port=PYRONSPORT)
		uri = ns.lookup("redis_processor")
		redisProcessor = Pyro4.Proxy(uri)
		data = redisProcessor.userShow(userid, level, require)
		if data == None:
			uri = ns.lookup("database_handler")
			dbProcessor = Pyro4.Proxy(uri)
			data = dbProcessor.userShow(userid, level, require)
			
		return json.dumps(data,ensure_ascii=True,encoding='utf8')
		

daemon = Pyro4.Daemon(host=LOCALADDR)
up = UserShowProcessor()
up_uri = daemon.register(up)
ns = Pyro4.locateNS(host=PYRONSADDR, port=PYRONSPORT)
ns.register("user_show_processor", up_uri)
daemon.requestLoop()