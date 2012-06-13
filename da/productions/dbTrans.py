#!/usr/bin/env python
# encoding: utf-8
"""
dbTrans.py

Created by Peter Ma on 2012-03-13.
Copyright (c) 2012 Maven Studio. All rights reserved.
"""

import sys
import os
import copy

from sqlalchemy import *
from datetime import *
from init import *
from types import *

from dbWorkerLib import *


class DatabaseTrans(object):

	def userData(self, userid, param={}):
		print 'userData'

		#debug = True

		engine = create_engine('mysql://%s:%s@%s:%s/user_profile_m?charset=utf8'%(MYSQLUSER, MYSQLPWD, MYSQLADDR, MYSQLPORT))
		conn = engine.connect()
		sql = 'select * from apps where (app_id = %s) ' % (app_id)
		rs = conn.execute(sql)

	def userPut(self, userData):
		'''
		1. check exists
		2. exists -> update
		3. not exists -> add new
		4. check selected, z
		'''
		return


if __name__ == '__main__':
	d = DatabaseWorker()
	print d.userShow(123874646464646)
