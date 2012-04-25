#!/usr/bin/env python
# encoding: utf-8
"""
usershowprocessor.py

Created by wenzhenwei on 2012-03-28.
"""

import sys
import os

import Pyro4
import redis

from init import *

class UserShowProcessor(object):

	def example(self):
		# uri = raw_input("what is the Pyro uri of the database handler object?").strip()
		# database_url = raw_input("please input your database url:").strip()
		# database_info = adapter.DatabaseHandler()
		# database_info = Pyro4.Proxy('PYRO:obj_46d0af449b2941c5bb4d0fb4a2f80fa3@localhost:65459')
		database_info = Pyro4.Proxy("PYRONAME:database_handler")
		data = database_info.info('test')
		print data
		return data
	
	def show(self, userid, **args):
		# first redis
#		redisHandler = Pyro4.Proxy("PYRONAME:redis_handler")
#		data = redisHandler.userShow(userid, args)
#		if data != None:
#			return data
#		dbHandler = Pyro4.Proxy("PYRONAME:database_handler")
#		data = dbHandler.userShow(userid, args)
		ns = Pyro4.locateNS(host=PYRONSADDR, port=PYRONSPORT)
		redisProcessor = Pyro4.Proxy("PYRONAME:redis_processor")
		data = redisProcessor.userShow(userid, args)
		if data == None:
			data = 'no user of ' + userid
		return data
		

print 'start.'
daemon = Pyro4.Daemon(host=LOCALADDR)
print 'create daemon.'

up = UserShowProcessor()
print 'create up instance'
up_uri = daemon.register(up)
print 'register up'
print up_uri
print 'add to nameserver'
ns = Pyro4.locateNS(host='192.168.91.216', port=9999)
ns.register('user.show',up_uri)
print 'add to nameserver done.'

daemon.requestLoop()
print 'start daemon done.'
