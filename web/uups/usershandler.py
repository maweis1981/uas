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
from init import *

import json

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
			print action
			if action == "show":
				"""
				/0/show?level={%d|0:basic,1:simple,...}&require={%json|["name","img",...]}
				"""
				level = self.get_argument("level", default=2)
				require = self.get_argument("require", default=None)
				ns = Pyro4.locateNS(host=PYRONSADDR, port=PYRONSPORT)
				uri = ns.lookup("user_show_processor")
				usProcessor = Pyro4.Proxy(uri)
				#print dir(usProcessor)
				data = usProcessor.show(userid, level=level, require=require)
				data = simplejson.loads(data)
				return self.render('usershow.json',data = data)

			if action == "base":
				"""
				/0/base
				"""
				ns = Pyro4.locateNS(host=PYRONSADDR, port=PYRONSPORT)
				uri = ns.lookup("user_show_processor")
				usProcessor = Pyro4.Proxy(uri)
				#print dir(usProcessor)
				data = usProcessor.apiUserBaseData(userid)
                                print '**********************************'
                                print data
                                print '=================================='
                                jsonData = json.dumps(data, ensure_ascii=False, indent=4, encoding='utf8')
                                print jsonData
                                print '**********************************'
				#data = simplejson.loads(data)
				return self.render('userbase.json',data = jsonData)
                                #return self.write(simplejson.loads(jsonData))
#return self.render('usershow.json',data = data)

			if action == "full":
				"""
				/0/show?level={%d|0:basic,1:simple,...}&require={%json|["name","img",...]}
				"""
				level = self.get_argument("level", default=2)
				require = self.get_argument("require", default=None)
				ns = Pyro4.locateNS(host=PYRONSADDR, port=PYRONSPORT)
				uri = ns.lookup("user_show_processor")
				usProcessor = Pyro4.Proxy(uri)
				#print dir(usProcessor)
				data = usProcessor.apiUserFullData(userid)
                                print '**********************************'
                                print json.dumps(data, ensure_ascii=False, indent=4, encoding='utf8')
                                print '**********************************'
				#data = simplejson.loads(data)
				return self.render('userfull.json',data = data)

			elif action == "sync":
				print userid
				nameserver = Pyro4.locateNS(host=PYRONSADDR,port=PYRONSPORT)
				print nameserver				
				uri = nameserver.lookup('user_sync_processor')
				print uri
				userShowProcessor = Pyro4.Proxy(uri)
				print userShowProcessor
				data = userShowProcessor.sync(userid, self.request.body)
				print data
				return self.render('usersync.json',data = data)
			elif action == "update":
				pass
			elif action == "add":
				pass
			elif action == "delete":
				pass
			else:
				logging.error("ip: " + self.request.remote_ip + " " + action)
				data = "unknown action"
			
		#return self.write(data)
		return self.render('usershow.json',data = data)
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

	def post(self, paths):
		self.set_header("Content-Type", "application/json; charset=UTF-8")
		data = None
		# first match /users/%user_id%/action?param
		#userProcessor = Pyro4.Proxy('PYRONAME:user_processor')
		#data = userProcessor.example()

		rosinglema = UsersHandler.resingle.match(paths)
		if rosinglema != None:
			userid = rosinglema.group(1)
			action = rosinglema.group(2)
			print '0000000'
			print action
			print action=="show"
			if action == "show":
				print 'action is show'
				"""
				/0/show?level={%d|0:basic,1:simple,...}&require={%json|["name","img",...]}
				"""
				level = self.get_argument("level", default=0)
				require = self.get_argument("require", default=None)
				print '======================='
				ns = Pyro4.locateNS(host=PYRONSADDR, port=PYRONSPORT)
				uri = ns.lookup("user_show_processor")
				usProcessor = Pyro4.Proxy(uri)
				#print dir(usProcessor)
				print '======================='
				data = usProcessor.show(userid, level=level, require=require)
				print '======================='
				print data
			elif action == "sync":
				print userid
				nameserver = Pyro4.locateNS(host=PYRONSADDR,port=PYRONSPORT)
				print nameserver				
				uri = nameserver.lookup('user_sync_processor')
				print uri
				userShowProcessor = Pyro4.Proxy(uri)
				print userShowProcessor
				data = userShowProcessor.sync(userid, self.request.body)
				print data
				return self.render('usersync.json', data = data)
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

