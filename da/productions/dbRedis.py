#!/usr/bin/env python
# encoding: utf-8
"""
usershowprocessor.py

Copyright (c) 2012 snda inc. All rights reserved.
"""

import sys
import os

import redis
from init import *
import copy


'''
cache data struct

user:
    dauf%id = user full data
    daub%id = user base data
    dacl%id = user contact list
    daci%id = revise user contact list (in contact)
    daaf%id = app info

'''

rd_prefs_UserBase       = 'dauf%s'
rd_prefs_UserFull       = 'daub%s'
rd_prefs_RelationList   = 'dacl%s'
rd_prefs_InRelationList = 'daci%s'
rd_prefs_Applicaton     = 'daaf%s'
rd_prefs_RelationData   = 'dard%s'
rd_const_fieldsindex   = 'da.fieldsindex'

class rdset(object):
    def __init__(self, rd, pref):
        self._dbRedis = rd
        self._pref = pref

    def get(self, id):
        s = self._dbRedis.redis.get(self._pref % id)
        if s != None:
            return self._dbRedis.uncompress(eval(s))
        else:
            return None
    
    def set(self, id, value):
        if id == None:
            return
        v = self._dbRedis.compress(value)
        self._dbRedis.redis.set(self._pref % id, v)

    def delete(self, id):
        self._dbRedis.redis.delete(self._pref % id)


class mapdict(object):
    def __init__(self, origDict):
        if origDict != None and type(origDict) is dict:
            self.dictkey = copy.deepcopy(origDict)
            self.dictidx = {}
            for (k,v) in self.dictkey.iteritems():
                self.dictidx[v]=k
            ks = self.dictidx.keys()
            ks.sort()
            self.index = ks[len(ks)-1]+1
        else:
            self.dictkey = {}
            self.dictidx = {}
            self.index = 0
        self.indexUpdate = False
        #print self.dictkey
        #print self.dictidx
        #print self.index


    def map(self, key):
        if key in self.dictkey:
            return self.dictkey[key]
        else:
            self.dictkey[key] = self.index
            self.dictidx[self.index] = key
            self.index = self.index + 1
            self.indexUpdate = True

    def key(self, idx):
        return self.dictidx.get(idx, None)


class dbRedis(object):
    def __init__(self, host = 'localhost', port=6379):
        self.redis = redis.Redis(host,port)
        self.redis.ping()
        s = self.redis.get(rd_const_fieldsindex)
        if s != None:
            self._fieldsdef = mapdict(eval(s))
        else:
            self._fieldsdef = mapdict(None)

        self.UserBase = rdset(self, rd_prefs_UserBase)
        self.UserFull = rdset(self, rd_prefs_UserFull)
        self.RelationList = rdset(self, rd_prefs_RelationList)
        self.InContactList = rdset(self, rd_prefs_InRelationList)
        self.RelationData = rdset(self, rd_prefs_RelationData)
        self.Applicaton = rdset(self, rd_prefs_Applicaton)

    def compress(self, data):
        if data == None: return None
        dest = type(data)()
        self._compress(data, dest)
        if self._fieldsdef.indexUpdate :
            self.redis.set(rd_const_fieldsindex, repr(self._fieldsdef.dictkey))
            self._fieldsdef.indexUpdate = False
        return dest

    def uncompress(self, data):
        if data == None: return None
        dest = type(data)()
        self._uncompress(data, dest)
        return dest

    def _compress(self, data, dest):
        if type(data) is dict:
            for k,v in data.iteritems():
                idx = self._fieldsdef.map(k)
                if type(v) in [dict,list]:
                    d = type(v)()
                    dest[idx]=d
                    self._compress(v,d)
                else:
                    dest[idx]=v
        elif type(data) is list:
            for v in data:
                d = type(v)()
                dest.append(d)
                self._compress(v,d)

    def _uncompress(self, data, dest):
        if type(data) is dict:
            for k,v in data.iteritems():
                idx = self._fieldsdef.key(k)
                if type(v) in [dict,list]:
                    d = type(v)()
                    dest[idx]=d
                    self._uncompress(v,d)
                else:
                    dest[idx]=v
        elif type(data) is list:
            for v in data:
                d = type(v)()
                dest.append(d)
                self._uncompress(v,d)

        
