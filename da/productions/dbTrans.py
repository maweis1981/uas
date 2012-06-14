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

		udf = extractUserDataFields(userData)
		for uf in udf:
			if user_id == None: 
				do_insert = True #==None 直接新增

			else:
				sqlt = userFieldDataToExistsSql(user_id,app_id,uf)
				rs = conn.execute(sqlt[0],sqlt[1])
				if rs.rowcount>0:
					info_id = rs['info_id']
					sqlt = userFieldDataToUpdateSql(user_id,app_id,info_id,uf)
					conn.execute(sqlt[0],sqlt[1])
					do_insert = False
			if do_insert :
				sqlt = userFieldDataToInsertSql(user_id,app_id,uf)
				rs = conn.execute(sqlt[0],sqlt[1])
				if rs.rowcount>0:
					info_id = rs[0]
		# 5. todo
		conn.execute('update userinfo set selected=1 where info_id=%s',info_id)
		return


	def ttcontactTrans(dbname='ttcontactdb'):
		engine = create_engine('mysql://%s:%s@%s:%s/%s?charset=utf8'%(MYSQLUSER, MYSQLPWD, MYSQLADDR, MYSQLPORT, dbname))
		conn = engine.connect()
		rs = conn.execute("select * from tt_user where registered_phone_number=mobile_phone")
		for row in rs:
			ud={'versign_phone':row['registered_phone_number'],
				'name':{'FN':row['display_name']},
				'telephones':[	{'tel_type':'mobile','tel_number':row['mobile_phone']},
								{'tel_type':'work','tel_number':row['work_phone']}],
				'emails':[{'email_type':'home','email':row['email']}],
				'organizations':[{'org_name':row['company'],'org_unit':row['department'],'role':row['position']}],
				'educations':[{'school_name':row['school']}],
				'addresses':[{'adr_type':'home','post_office_address':row['location']}],
				'im':{'QQ':row['qq'],'MSN':row['msn']},
				'url':{'homepage':row['website']},
				'source_name':'user',
				'source_id':row['card_id']
				}
			self.userPut(ud,2)
		return

if __name__ == '__main__':
	d = DatabaseWorker()
	print d.userShow(123874646464646)
