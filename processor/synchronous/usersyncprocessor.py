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

class UserSyncProcessor(object):

	def example(self):
		# uri = raw_input("what is the Pyro uri of the database handler object?").strip()
		# database_url = raw_input("please input your database url:").strip()
		# database_info = adapter.DatabaseHandler()
		# database_info = Pyro4.Proxy('PYRO:obj_46d0af449b2941c5bb4d0fb4a2f80fa3@localhost:65459')
		database_info = Pyro4.Proxy("PYRONAME:database_handler")
		data = database_info.info('test')
		print data
		return data
	
	def sync(self, userid, data):
		# first redis
#		redisHandler = Pyro4.Proxy("PYRONAME:redis_handler")
#		data = redisHandler.userShow(userid, args)
#		if data != None:
#			return data
#		dbHandler = Pyro4.Proxy("PYRONAME:database_handler")
#		data = dbHandler.userShow(userid, args)
		rdata = {"meta": {"code":200, "message":"success"}, "data":{}}
		jdata = None
		try:
			jdata = json.loads(data)
			jdata = jdata["data"]
		except:
			rdata["meta"]["code"] = 101
			rdata["meta"]["message"] = "input format error"
			return rdata

		ns = Pyro4.locateNS(host=PYRONSADDR, port=PYRONSPORT)
		uri = ns.lookup("redis_processor")
		redisProcessor = Pyro4.Proxy(uri)
		for ju in jdata:
			#data = redisProcessor.userShow(userid, )
			redisProcessor.userPut(ju["id"], json.dumps(ju))
		return rdata
		

# userProcessor = UserProcessor()
# daemon = Pyro4.Daemon()
# uri = daemon.register(userProcessor)
# 
# print "Ready, User Processor Uri is [%s] " % uri
# daemon.requestLoop()
daemon = Pyro4.Daemon(host=LOCALADDR)
up = UserSyncProcessor()
up_uri = daemon.register(up)
ns = Pyro4.locateNS(host=PYRONSADDR, port=PYRONSPORT)
ns.register("user_sync_processor", up_uri)
daemon.requestLoop()


#daemon = Pyro4.Daemon()
#ns = Pyro4.locateNS(host=PYRONSADDR, port=PYRONSPORT)
#
## uri = daemon.register(database_handler)
## ns.register("database_handler", uri)
## print "Ready, object uri = ", uri
## daemon.requestLoop()
## -----alternatively, using serverDatabaseHandler-----
#Pyro4.Daemon.serveSimple(
#	{
#		UserSyncProcessor():"user_sync_processor",
#	},
#	host=LOCALADDR,
#	ns = True, verbose = True)
