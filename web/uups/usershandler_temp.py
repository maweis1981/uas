#!/usr/bin/env python
# encoding: utf-8
"""
usershandler.py

Created by wenzhenwei on 2012-03-28.
Copyright (c) 2012 snda inc. All rights reserved.
"""

import os,sys,re
from basehandler import *
import Pyro4
import logging

class UsersHandler(BaseHandler):

	resingle = re.compile(r'(\d+)/(\w+)')

	def get(self, paths):
		self.set_header("Content-Type", "application/json; charset=UTF-8")
		data = None
		# first match /users/%user_id%/action?param
		#userProcessor = Pyro4.Proxy('PYRONAME:user_processor')
		#data = userProcessor.example()

		rosinglema = UsersHandler.resingle.match(paths)
		if rosinglema != None:
			userid = rosinglema.group(1)
			action = rosinglema.group(2)

			if action == "show":
				"""
				/0/show?level={%d|0:basic,1:simple,...}&require={%json|["name","img",...]}
				"""
				level = self.get_argument("level", default=0)
				require = self.get_argument("require", default=None)
				Pyro4.locateNS(host="192.168.91.216")
				usProcessor = Pyro4.Proxy('PYRONAME:user_show_processor')
				#print dir(usProcessor)
				data = usProcessor.show(userid, level=level, require=require)
			elif action == "sync":
				pass
			elif action == "update":
				pass
			elif action == "add":
				pass
			elif action == "delete":
				pass
			else:
				logging.error("ip: " + self.request.remote_ip + " " + action)
				data = "unknown action"
			
		return self.write(data)
		#		print data
		# for d in data:
			# return d
		# return self.write('----')
		#return self.write(simplejson.dumps(data))		 
		# users = []
		#		 for i in range(10):
		#			 user = {'id':12345,'name':'maven','range_id':'%d' % i,'endfix':'end_string'}
		#			 users.append(user)
		# return self.write(simplejson.dumps(users)) 


