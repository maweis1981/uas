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
            self.__engine = create_engine('mysql://%s:%s@%s:%s/user_profile_m?charset=utf8'%(MYSQLUSER, MYSQLPWD, MYSQLADDR, MYSQLPORT),pool_size=10)
        return self.__engine
        
    def conn_begin(self):
        if (self.__conn == None) or (self.__conn.closed):
            self.__conn = self.engine().connect()
            self.__connused = False
        if self.__connused:
            conn = self.engine().connect()
        else:
            conn = self.__conn
            self.__connused = True
        return conn
    
    def conn_end(self, conn):
        if conn != None:
            if conn == self.__conn:
                #if conn.closed :
                #    self.__conn = engine().connect()
                #else:
                #    conn.execute('commit;')
                self.__connused = False
            else:
                conn.close()
        return
    
    def execute(self, object, *multiparams, **params):
        conn = self.conn_begin()
        try:
            rs = conn.execute(object, *multiparams, **params)
        finally:
            self.conn_end(conn)
        return rs
