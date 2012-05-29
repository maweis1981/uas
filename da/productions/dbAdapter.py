#!/usr/bin/env python
# encoding: utf-8
"""
dbAdapter.py

Created by Peter Ma on 2012-03-13.
Copyright (c) 2012 Maven Studio. All rights reserved.
"""
import Pyro4 

from dbWorker import DatabaseWorker
from init import *


class DatabaseHandler(object):
	def info(self,url):
		d = DatabaseWorker()
		return d.test_data()
		# return "Your Database Connect URL  is {0}".format(url)
	
	def userShow(self, userid, level=2, require=None):
		if userid == None:
			return None
		d = DatabaseWorker()
		return d.userShow(userid, level, require)

	'''
	def userData(self,user_id):
		d = DatabaseWorker()
		return d.userData(user_id)
	'''
	
	# for user
	# user base data
	def userBaseData(self,user_id):
		d = DatabaseWorker()
		return d.userBaseData(user_id)

	# user full info
	def userFullData(self,user_id):
		d = DatabaseWorker()
		return d.userFullData(user_id)

	def userLookup(self, TelOrEmail='', retType='full'):
		d = DatabaseWorker()
		return d.userLookup(TelOrEmail, retType)

	# for Relation
	def userContacts(self, user_id, commonParam={}):
		d = DatabaseWorker()
		print dict(user_id=user_id,Param=commonParam)
		return d.userContacts(user_id, commonParam)

	def userRelationsIdList(self, user_id, commonParam={}):
		d = DatabaseWorker()
		return d.userRelationsIdList(user_id, commonParam)

	def	userRelationData(self, rel_id):
		d = DatabaseWorker()
		return d.userRelationData(rel_id)

	def	userContactData(self, rel_id):
		d = DatabaseWorker()
		return d.userContactData(rel_id)

	# for in Relation

	def	userInContacts(self, user_id, commonParam={}):
		d = DatabaseWorker()
		return d.userInContacts(user_id, commonParam)
		
	def userInRelationsIdList(self, user_id, commonParam={}):
		d = DatabaseWorker()
		return d.userInRelationsIdList(user_id, commonParam)

	# for friends
	def userFriends(self, user_id, commonParam={}):
		d = DatabaseWorker()
		return d.userFriends(user_id, commonParam)

	# for apps

	def userApps(self, user_id, commonParam={}):
		d = DatabaseWorker()
		return d.userApps(user_id, commonParam)

database_handler = DatabaseHandler()
daemon = Pyro4.Daemon(host=LOCALADDR)
db_uri = daemon.register(database_handler)
ns = Pyro4.locateNS(host=PYRONSADDR, port=PYRONSPORT)
ns.register("database_handler", db_uri)
daemon.requestLoop()

