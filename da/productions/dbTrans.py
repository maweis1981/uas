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
from dbWorker import *


class DatabaseTrans(object):

	def userData(self, userid, param={}):
		print 'userData'

		#debug = True

		engine = create_engine('mysql://%s:%s@%s:%s/user_profile_m?charset=utf8'%(MYSQLUSER, MYSQLPWD, MYSQLADDR, MYSQLPORT))
		conn = engine.connect()
		sql = 'select * from apps where (app_id = %s) ' % (app_id)
		rs = conn.execute(sql)

	# userData必须是符合修改记录标准的数据，否则可能会引起重复记录。
	def userPut(self, userData, app_id): 
		'''
		1. check exists user
		2. check exists fields
		3. exists -> update
		4. not exists -> add new
		5. check selected, z
		'''
		engine = create_engine('mysql://%s:%s@%s:%s/user_profile_m?charset=utf8'%(MYSQLUSER, MYSQLPWD, MYSQLADDR, MYSQLPORT))
		conn = engine.connect()

		user_id = userData.get('user_id', None);
		if user_id == None:
			if 'versign_phone' in userData:
				d = DatabaseWorker()
				user_id = d.userLookup(userData['versign_phone'], 'id')
				if (user_id == None) and 'versign_email' in userData:
					user_id = d.userLookup(userData['versign_email'], 'id')
		if user_id == None:
			# add user
			phone = userData.get('versign_phone','')
			email = userData.get('versign_email','')
			uguid = userData.get('uid','')
			sql = 'insert into users (guid,phone,email,user_state) values (%s,%s,%s,1); select @userid := LAST_INSERT_ID();'
			rs = conn.execute(sql,uguid,phone,email)
			if rs.rowcount>0:
				rs = conn.execute('select @userid')
				user_id=rs.fetchone()[0]
			print user_id
			do_insert = True #==None 直接新增
		else:
			do_insert = False

		udf = extractUserDataFields(userData)
		for uf in udf:
			if not do_insert:
				sqlt = userFieldDataToExistsSql(user_id,app_id,uf)
				print sqlt[0] % tuple(sqlt[1])
				rs = conn.execute(sqlt[0],sqlt[1])
				if rs.rowcount>0:
					row = rs.fetchone()
					info_id = row['info_id']
					sqlt = userFieldDataToUpdateSql(user_id,app_id,info_id,uf)
					print sqlt[0] % tuple(sqlt[1])
					conn.execute(sqlt[0],sqlt[1])
					do_insert = False
				else:
					do_insert = True
			if do_insert :
				sqlt = userFieldDataToInsertSql(user_id,app_id,uf)
				print sqlt[0] % tuple(sqlt[1])
				rs = conn.execute(sqlt[0],sqlt[1])
				if rs.rowcount>0:
					rs = conn.execute('select @dataid')
					info_id = rs.fetchone()[0]
		# 5. todo
			if info_id>0:
				conn.execute('update userinfo set selected=1 where info_id=%s',info_id)
		conn.close()
		return


	def ttcontactTrans(self, dbname='ttcontactdb'):
		connstring = 'mysql://%s:%s@%s:%s/%s?charset=utf8'%(MYSQLUSER, MYSQLPWD, MYSQLADDR, MYSQLPORT, dbname)
		engine = create_engine(connstring)
		conn = engine.connect()
		rs = conn.execute("select * from tt_user where registered_phone_number=mobile_phone")
		for row in rs:
			ud={'versign_phone':row['registered_phone_number'],
				'uid':row['card_id'],
				'name':{'FN':row['display_name']},
				'telephones':[	{'tel_type':'mobile','tel_number':row['mobile_phone']},
								{'tel_type':'work','tel_number':row['work_phone']}],
				'emails':[{'email_type':'home','email':row['email']}],
				'organizations':[{'org_name':row['company'],'org_unit':row['department'],'role':row['position']}],
				'educations':[{'school_name':row['school']}],
				'addresses':[{'adr_type':'home','post_office_address':row['location']}],
				'im':{'QQ':row['qq'],'MSN':row['msn']},
				'url':{'homepage':row['website']},
				'source-ident':{'source_name':'user','source_id':row['card_id']}
				}
			#清除空数据
			self.userPut(ud,2)
			return
		return

if __name__ == '__main__':
	d = DatabaseWorker()
	print d.userShow(123874646464646)
