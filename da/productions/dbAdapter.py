#!/usr/bin/env python
# encoding: utf-8
"""
dbAdapter.py

Created by wanghao on 2012-03-13.
Copyright (c) 2012 All rights reserved.
"""
import Pyro4 

from dbWorker import DatabaseWorker
from init import *
from dbConnections import *


class DatabaseHandler(object):

    def __init__(self):
        self.dbConns = DatabaseConnections()
        self.Worker = DatabaseWorker(self.dbConns)
    
    def info(self,url):
        return self.Worker.test_data()
        # return "Your Database Connect URL  is {0}".format(url)
    
    def userShow(self, userid, level=2, require=None):
        if userid == None:
            return None
        return self.Worker.userShow(userid, level, require)

    '''
    def userData(self,user_id):
        return self.Worker.userData(user_id)
    '''
    
    # for user
    # user base data
    def userBaseData(self,user_id):
        return self.Worker.userBaseData(user_id)

    # user full info
    def userFullData(self,user_id):
        return self.Worker.userFullData(user_id)

    def userLookup(self, TelOrEmail='', retType='full'):
        return self.Worker.userLookup(TelOrEmail, retType)

    # for Relation
    def userContacts(self, user_id, commonParam={}):
        #print dict(user_id=user_id,Param=commonParam)
        data = self.Worker.userContacts(user_id, commonParam)
        return data

    def userRelationsIdList(self, user_id, commonParam={}):
        return self.Worker.userRelationsIdList(user_id, commonParam)

    def userRelationData(self, rel_id):
        return self.Worker.userRelationData(rel_id)

    def userContactData(self, rel_id):
        return self.Worker.userContactData(rel_id)

    # for in Relation

    def userInContacts(self, user_id, commonParam={}):
        return self.Worker.userInContacts(user_id, commonParam)
        
    def userInRelationsIdList(self, user_id, commonParam={}):
        return self.Worker.userInRelationsIdList(user_id, commonParam)

    # for friends
    def userFriends(self, user_id, commonParam={}):
        return self.Worker.userFriends(user_id, commonParam)

    # for apps

    def userApps(self, user_id, commonParam={}):
        return self.Worker.userApps(user_id, commonParam)

database_handler = DatabaseHandler()
daemon = Pyro4.Daemon(host=LOCALADDR)
db_uri = daemon.register(database_handler)
ns = Pyro4.locateNS(host=PYRONSADDR, port=PYRONSPORT)
ns.register("database_handler", db_uri)
daemon.requestLoop()

