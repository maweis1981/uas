#!/usr/bin/env python
# encoding: utf-8
"""
dbConnections.py
"""

import sys
import os

from types import *

from sqlalchemy import *
from init import *

#from DBUtils.PooledDB import PooledDB
#import MySQLdb
import time

import conf
import ConfigParser

class IniConfig(ConfigParser.ConfigParser):
    __inifilename = ''
    def get(self, section, option, default=None, raw=False, vars=None):
        if self.has_section(section) and self.has_option(section, option):
            return ConfigParser.ConfigParser.get(self,section, option, raw, vars)
        else:
            return default

    def read(self, inifilename):
        ls = ConfigParser.ConfigParser.read(self, inifilename)
        if len(ls)>0:
            self.__inifilename = inifilename
            #print self.__inifilename
            return True
        else:
            self.__inifilename = ''
            return False

    def set(self, section, option, value=None):
        if not self.has_section(section):
            self.add_section(section)
        ConfigParser.ConfigParser.set(self, section, option, value)

    def write(self, fp=None):
        if fp == None:
            if self.__inifilename != '':
                ConfigParser.ConfigParser.write(self, open(self.__inifilename,'w'))
        elif type(fp) in [str,unicode]:
            ConfigParser.ConfigParser.write(self, open(fp,'w'))
        elif type(fp) is file:
            ConfigParser.ConfigParser.write(self, fp)

class initdbconfig():
    def __init__(self):
        cf = IniConfig()
        print 'init...',CONFPATH+'/db.conf'
        cf.read(CONFPATH+'/db.conf')
        self.db_addr = cf.get('db','addr','localhost')
        self.db_port = int(cf.get('db','port','3306'))
        self.db_user = cf.get('db','user','root')
        self.db_pass = cf.get('db','pass','idea')

        self.pool_mincached = int(cf.get('pool','mincached',0))
        self.pool_maxcached = int(cf.get('pool','mincached',0))
        self.pool_maxshared = int(cf.get('pool','maxshared',0))
        self.pool_maxconnections = int (cf.get('pool','maxconnections',5))
        self.pool_blocking  = int(cf.get('pool','blocking',0))
        self.pool_maxusage  = int(cf.get('pool','maxusage',0))


'''
#数据库连接池句柄
class DBPool:
    pool = {};
    @staticmethod
    def getInstance(db_name):
        try:
            if isinstance(db_name, unicode):
                db_name = db_name.encode("utf8")
            if DBPool.pool.get(db_name):
                return DBPool.pool.get(db_name)
            else:
                dbconf = initdbconfig()
                print dbconf.db_addr, dbconf.db_port, dbconf.db_user, dbconf.db_pass
                tmp_pool = PooledDB(MySQLdb, \
                                    int(dbconf.pool_mincached),\
                                    int(dbconf.pool_maxcached),\
                                    int(dbconf.pool_maxshared),\
                                    int(dbconf.pool_maxconnections),\
                                    int(dbconf.pool_blocking),\
                                    int(dbconf.pool_maxusage),\
                                    ["SET NAMES utf8","SET CHARACTER SET utf8"],\
                                    host = dbconf.db_addr, \
                                    user = dbconf.db_user, \
                                    passwd = dbconf.db_pass, \
                                    db = db_name,\
                                    charset = "utf8",\
                                    port = int(dbconf.db_port))
                tmp_pool.charset = "utf8"
                DBPool.pool[db_name] = tmp_pool
                return DBPool.pool[db_name]
        except Exception,e:
            #func_ext.error_log(e)
            time.sleep(5)
            return DBPool.getInstance(db_name)
'''

class DatabaseConnections(object):
    __engine = None
    __conn = None
    __connused = False

    def __init__(self):
        # 创建默认定义的数据库
        # 创建一个默认连接，以便效率更高
        conn = self.conn_begin()
        self.conn_end(conn)
    
    def engine(self):
        if (self.__engine == None) :
            dbconf = initdbconfig()
            connstring = 'mysql://%s:%s@%s:%s/user_profile_m?charset=utf8'%(dbconf.db_user, dbconf.db_pass, dbconf.db_addr, dbconf.db_port)
            print connstring
            self.__engine = create_engine(connstring, pool_size=dbconf.pool_maxconnections)
            #self.__engine = DBPool.getInstance('user_profile_m')
        return self.__engine
        
    def conn_begin(self):
        if (self.__conn == None) or (self.__conn.closed):
            self.__conn = self.engine().connect()
            self.__connused = False
        if self.__connused:
            #print 'conn open'
            conn = self.engine().connect()
        else:
            conn = self.__conn
            self.__connused = True
        return conn
    
    def conn_end(self, conn, commit=False):
        if conn != None:
            if conn == self.__conn:
                if conn.closed:
                    self.__conn = engine().connect()
                else:
                    if commit:
                        conn.execute('commit;')
                self.__connused = False
                #print ' __conn end'
            else:
                if not conn.closed:
                    #print 'conn close'
                    if commit:
                        conn.execute('commit;')
                    conn.close()
        return

    def conn_commit(self, conn):
        if not conn.closed:
            conn.execute('commit;')
    
    def execute(self, object, *multiparams, **params):
        try:
            conn = self.conn_begin()
            rs = conn.execute(object, *multiparams, **params)
        finally:
            self.conn_end(conn)
        return rs
