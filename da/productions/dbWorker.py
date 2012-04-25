#!/usr/bin/env python
# encoding: utf-8
"""
dbworker.py

Created by Peter Ma on 2012-03-13.
Copyright (c) 2012 Maven Studio. All rights reserved.
"""


import sys
import os

from sqlalchemy import *
from datetime import datetime
from init import *

reload(sys)
sys.setdefaultencoding('utf8') 

class DatabaseWorker(object):

	def create_table(self):
		engine = create_engine('mysql://root:idea@localhost/uas_test')
		conn = engine.connect()
		metadata = MetaData()
		user = Table('t_user', metadata, 
			Column('id', Integer, primary_key=True, autoincrement=True),
			Column('name', String(30)),
			Column('address', String(100)))
		metadata.create_all(engine)
		conn.close()
	
	def generate_data(self):
		engine = create_engine('mysql://root:idea@localhost/uas_test')
		conn = engine.connect()
		metadata = MetaData()
		metadata.bind=engine
		t_user = Table('t_user', metadata, autoload=True)
		ins = t_user.insert().values(name="wenzw", address="shanghai")
		print str(ins)
		result = conn.execute(ins)
		print result

	def userShow(self, userid, level=2, require=None):
		engine = create_engine('mysql://%s:%s@%s:%s/user_profile?charset=utf8'%(MYSQLUSER, MYSQLPWD, MYSQLADDR, MYSQLPORT))
		conn = engine.connect()
		keylist = ""
		if require != None :
			requirelist = require.split(',')
			if  requirelist.count > 0 :
				keylist = "'"+requirelist[0]+"'"
				for i in range(1,len(requirelist)):
					keylist = keylist +  ",'" + requirelist[i] + "'"
			keylist = ' OR key_dict.key_name in (%s) ' % (keylist)

		sql = 'SELECT user_info.key_name, user_info.value \
FROM user_info \
INNER JOIN key_dict ON user_info.key_name = key_dict.key_name \
WHERE (user_id = %s AND key_level <=%s) %s \
ORDER BY key_level, key_order' % (userid,level,keylist)
		print sql

		result = conn.execute(sql)
		conn.close()
		row_data = {}
		for row in result:
			row_data[row[0].encode('utf8')]=row[1].encode('utf8')
			print row[1] , row[1].encode('utf8')
		print ('userid:',userid,'level:',level,'require:',require,'result:',row_data,'\n')
		#print row_data[0]['name']
		return row_data

	def userPut(self, userid, value):
		if userid == None:
			return
		engine = create_engine('mysql://%s:%s@%s:%s/user_profile?charset=utf8'%(MYSQLUSER, MYSQLPWD, MYSQLADDR, MYSQLPORT))
		conn = engine.connect()
		print value
		conn.close()
		result = conn.execute(sql)


	def test_data(self):
		engine = create_engine('mysql://root:idea@localhost/uas_test')
		conn = engine.connect()
		result = conn.execute('select * from t_user')
		conn.close()
		row_data = []
		for row in result:
			# print row
			d = dict(row.items())
			# print d
			row_data.append(d)
		return row_data
		
if __name__ == '__main__':
	d = DatabaseWorker()
	print d.userShow(123874646464646)
