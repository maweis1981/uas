#!/usr/bin/env python
# encoding: utf-8
"""
usershowprocessor.py

Created by wenzhenwei on 2012-03-28.
Copyright (c) 2012 snda inc. All rights reserved.
"""

import sys
import os

import Pyro4
import redis

from init import *

class RedisProcessor(object):

	def example(self):
		# uri = raw_input("what is the Pyro uri of the database handler object?").strip()
		# database_url = raw_input("please input your database url:").strip()
		# database_info = adapter.DatabaseHandler()
		# database_info = Pyro4.Proxy('PYRO:obj_46d0af449b2941c5bb4d0fb4a2f80fa3@localhost:65459')
		database_info = Pyro4.Proxy("PYRONAME:database_handler")
		data = database_info.info('test')
		print data
		return data
	
	def userShow(self, userid, level=2, require=None):
		# first redis
#		redisHandler = Pyro4.Proxy("PYRONAME:redis_handler")
#		data = redisHandler.userShow(userid, args)
#		if data != None:
#			return data
#		dbHandler = Pyro4.Proxy("PYRONAME:database_handler")
#		data = dbHandler.userShow(userid, args)
		if userid == None:
			return None
		r = redis.Redis(host=REDISADDR, port=REDISPORT, db=0)
		if r == None:
			return None
		data = r.get(userid)
		return data

	def userPut(self, userid, value):
		if userid == None:
			return
		r = redis.Redis(host=REDISADDR, port=REDISPORT, db=0)
		r.set(userid, value)
		return

		

# userProcessor = UserProcessor()
# daemon = Pyro4.Daemon()
# uri = daemon.register(userProcessor)
# 
# print "Ready, User Processor Uri is [%s] " % uri
# daemon.requestLoop()

daemon = Pyro4.Daemon(host=LOCALADDR)
rp = RedisProcessor()
rp_uri = daemon.register(rp)
ns = Pyro4.locateNS(host=PYRONSADDR, port=PYRONSPORT)
ns.register("redis_processor", rp_uri)
daemon.requestLoop()
# uri = daemon.register(database_handler)
# ns.register("database_handler", uri)
# print "Ready, object uri = ", uri
# daemon.requestLoop()
# -----alternatively, using serverDatabaseHandler-----
#Pyro4.Daemon.serveSimple(
#	{
#		RedisProcessor():"redis_processor",
#	},
#	host=LOCALADDR,
#	ns = True, verbose = True)
