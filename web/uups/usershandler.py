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
import time

from sqlalchemy import *
import MySQLdb

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
            action = action.lower()
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
                

            elif action == "base":
                """
                /0/base
                """
                ns = Pyro4.locateNS(host=PYRONSADDR, port=PYRONSPORT)
                uri = ns.lookup("user_show_processor")
                usProcessor = Pyro4.Proxy(uri)
                #print dir(usProcessor)
                data = usProcessor.userBaseData(userid)
                print '**********************************'
                print data
                print '=================================='
                jsonData = json.dumps(data, ensure_ascii=False, indent=4, encoding='utf8')
                print jsonData
                print '**********************************'
                #data = simplejson.loads(data)
                return self.render('userbase.json',data = jsonData)
                #return self.write(simplejson.loads(jsonData))

            elif action == "full":
                """
                /0/show?level={%d|0:basic,1:simple,...}&require={%json|["name","img",...]}
                """
                level = self.get_argument("level", default=2)
                require = self.get_argument("require", default=None)
                ns = Pyro4.locateNS(host=PYRONSADDR, port=PYRONSPORT)
                uri = ns.lookup("user_show_processor")
                usProcessor = Pyro4.Proxy(uri)
                #print dir(usProcessor)
                data = usProcessor.userFullData(userid)
                print '**********************************'
                jsonData = json.dumps(data, ensure_ascii=False, indent=4, encoding='utf8')
                print jsonData
                print '**********************************'
                #data = simplejson.loads(data)
                return self.render('userfull.json',data = data)

            elif action == "lookup":
                """
                /0/show?level={%d|0:basic,1:simple,...}&require={%json|["name","img",...]}
                """
                tel = self.get_argument("tel", default='')
                mail = self.get_argument("email", default='')
                retType = self.get_argument("rettype", default='full')
                print retType
                ns = Pyro4.locateNS(host=PYRONSADDR, port=PYRONSPORT)
                uri = ns.lookup("user_show_processor")
                usProcessor = Pyro4.Proxy(uri)
                #print dir(usProcessor)
                if tel != '' :
                    data = usProcessor.userLookup(tel,retType)
                elif mail != '' :
                    data = usProcessor.userLookup(mail,retType)
                print '**********************************'
                jsonData = json.dumps(data, ensure_ascii=False, indent=4, encoding='utf8')
                print jsonData
                print '**********************************'
                return self.render('userfull.json',data = data)

            elif action == "contacts":
                """
                /0/show?level={%d|0:basic,1:simple,...}&require={%json|["name","img",...]}
                """
                ioffset = self.get_argument("offset", default=None)
                ilimit = self.get_argument("limit", default=None)
                ns = Pyro4.locateNS(host=PYRONSADDR, port=PYRONSPORT)
                uri = ns.lookup("user_show_processor")
                usProcessor = Pyro4.Proxy(uri)
                #print dir(usProcessor)
                param = {}
                if ioffset != None :
                    param['offset']= ioffset
                if ilimit != None :
                    param['limit'] = ilimit
                print userid, param
                data = usProcessor.userContacts(userid,param)
                print data
                print '**********************************'
                jsonData = json.dumps(data, ensure_ascii=False, indent=4)
                print jsonData
                print '**********************************'
                #data = simplejson.loads(data)
                return self.render('userfull.json',data = data)

            elif action == "relationlist":
                """
                /0/show?level={%d|0:basic,1:simple,...}&require={%json|["name","img",...]}
                """
                ioffset = self.get_argument("offset", default=None)
                ilimit = self.get_argument("limit", default=None)
                ns = Pyro4.locateNS(host=PYRONSADDR, port=PYRONSPORT)
                uri = ns.lookup("user_show_processor")
                usProcessor = Pyro4.Proxy(uri)
                #print dir(usProcessor)
                param = {}
                if ioffset != None :
                    param['offset']= ioffset
                if ilimit != None :
                    param['limit'] = ilimit
                print userid, param
                data = usProcessor.userRelationsIdList(userid,param)
                print data
                print '**********************************'
                jsonData = json.dumps(data, ensure_ascii=False, indent=4, encoding='utf8')
                print jsonData
                print '**********************************'
                #data = simplejson.loads(data)
                return self.render('userfull.json',data = data)

            elif action == "relationdata":
                relid = self.get_argument("relid", default=None)
                ns = Pyro4.locateNS(host=PYRONSADDR, port=PYRONSPORT)
                uri = ns.lookup("user_show_processor")
                usProcessor = Pyro4.Proxy(uri)
                #print dir(usProcessor)
                data = usProcessor.userRelationData(relid)
                print data
                print '**********************************'
                jsonData = json.dumps(data, ensure_ascii=False, indent=4, encoding='utf8')
                print jsonData
                print '**********************************'
                #data = simplejson.loads(data)
                return self.render('userfull.json',data = data)

            elif action == "contactdata":
                relid = self.get_argument("relid", default=None)
                ns = Pyro4.locateNS(host=PYRONSADDR, port=PYRONSPORT)
                uri = ns.lookup("user_show_processor")
                usProcessor = Pyro4.Proxy(uri)
                #print dir(usProcessor)
                data = usProcessor.userContactData(relid)
                print data
                print '**********************************'
                jsonData = json.dumps(data, ensure_ascii=False, indent=4, encoding='utf8')
                print jsonData
                print '**********************************'
                #data = simplejson.loads(data)
                return self.render('userfull.json',data = data)

            elif action == "inrelationlist":
                ioffset = self.get_argument("offset", default=None)
                ilimit = self.get_argument("limit", default=None)
                ns = Pyro4.locateNS(host=PYRONSADDR, port=PYRONSPORT)
                uri = ns.lookup("user_show_processor")
                usProcessor = Pyro4.Proxy(uri)
                param = {}
                if ioffset != None :
                    param['offset']= ioffset
                if ilimit != None :
                    param['limit'] = ilimit
                print userid, param
                data = usProcessor.userInRelationsIdList(userid,param)
                print data
                print '**********************************'
                jsonData = json.dumps(data, ensure_ascii=False, indent=4, encoding='utf8')
                print jsonData
                print '**********************************'
                #data = simplejson.loads(data)
                return self.render('userfull.json',data = data)

            elif action == "incontacts" :
                """
                /0/show?level={%d|0:basic,1:simple,...}&require={%json|["name","img",...]}
                """
                ioffset = self.get_argument("offset", default=None)
                ilimit  = self.get_argument("limit", default=None)
                ns = Pyro4.locateNS(host=PYRONSADDR, port=PYRONSPORT)
                uri = ns.lookup("user_show_processor")
                usProcessor = Pyro4.Proxy(uri)
                #print dir(usProcessor)
                param = {}
                if ioffset != None :
                    param['offset']= ioffset
                if ilimit != None :
                    param['limit'] = ilimit
                print userid, param
                data = usProcessor.userInContacts(userid,param)
                print data
                print '**********************************'
                jsonData = json.dumps(data, ensure_ascii=False, indent=4, encoding='utf8')
                print jsonData
                print '**********************************'
                #data = simplejson.loads(data)
                return self.render('userfull.json',data = data)

            elif action == "friends":
                """
                /0/show?level={%d|0:basic,1:simple,...}&require={%json|["name","img",...]}
                """
                ioffset = self.get_argument("offset", default=None)
                ilimit  = self.get_argument("limit", default=None)
                ns = Pyro4.locateNS(host=PYRONSADDR, port=PYRONSPORT)
                uri = ns.lookup("user_show_processor")
                usProcessor = Pyro4.Proxy(uri)
                #print dir(usProcessor)
                param = {}
                if ioffset != None :
                    param['offset']= ioffset
                if ilimit != None :
                    param['limit'] = ilimit
                print userid, param
                data = usProcessor.userFriends(userid,param)
                print data
                print '**********************************'
                jsonData = json.dumps(data, ensure_ascii=False, indent=4, encoding='utf8')
                print jsonData
                print '**********************************'
                #data = simplejson.loads(data)
                return self.render('userfull.json',data = data)

            elif action == "apps":
                ioffset = self.get_argument("offset", default=None)
                ilimit = self.get_argument("limit", default=None)
                ns = Pyro4.locateNS(host=PYRONSADDR, port=PYRONSPORT)
                uri = ns.lookup("user_show_processor")
                usProcessor = Pyro4.Proxy(uri)
                param = {}
                if ioffset != None :
                    param['offset']= ioffset
                if ilimit != None :
                    param['limit'] = ilimit
                print userid, param
                data = usProcessor.userApps(userid,param)
                print data
                print '**********************************'
                jsonData = json.dumps(data, ensure_ascii=False, indent=4, encoding='utf8')
                print jsonData
                print '**********************************'
                #data = simplejson.loads(data)
                return self.render('userfull.json',data = data)

            elif action == "testing":
                tel = self.get_argument("tel", default='')
                t_start = time.time()
                #engine = create_engine('mysql://%s:%s@%s:%s/user_profile_m?charset=utf8'%('root', 'idea', 'localhost', '3306'))
                #conn = engine.connect()
                #rs = conn.execute('select * from users limit 0,40000')
                conn = MySQLdb.connect(host="localhost",user="root",passwd="idea",db="user_profile_m",charset='utf8',cursorclass=MySQLdb.cursors.DictCursor)
                cur = conn.cursor()
                cur.execute('select * from users limit 0,40000')
                rs = cur.fetchall()
                for row in rs:
                    s = str(row['user_id']) + str(row['phone'])
                t_end = time.time()
                data = [t_start,t_end,t_end-t_start]
                print '**********************************'
                jsonData = json.dumps(data, ensure_ascii=False, indent=4, encoding='utf8')
                print jsonData
                print '**********************************'
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
        return self.render('usershow.json',data = [])
        #        print data
        # for d in data:
            # return d
        # return self.write('----')
        #return self.write(simplejson.dumps(data))         
        # users = []
        #         for i in range(10):
        #             user = {'id':12345,'name':'maven','range_id':'%d' % i,'endfix':'end_string'}
        #             users.append(user)
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

