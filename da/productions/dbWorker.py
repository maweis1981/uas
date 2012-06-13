#!/usr/bin/env python
# encoding: utf-8
"""
dbworker.py

Created by Peter Ma on 2012-03-13.
Copyright (c) 2012 Maven Studio. All rights reserved.
"""

import sys
#reload(sys)
#sys.setdefaultencoding('utf8') 

import os
import copy

from sqlalchemy import *
from datetime import *
from init import *
from types import *

from dbWorkerLib import *


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
		#print sql

		result = conn.execute(sql)
		conn.close()
		row_data = {}
		for row in result:
			row_data[row[0].encode('utf8')]=row[1].encode('utf8')
			#print row[1] , row[1].encode('utf8')
		print ('userid:',userid,'level:',level,'require:',require,'result:',row_data,'\n')
		#print row_data[0]['name']
		return row_data
	

	def userData(self, userid, param={}):
		print 'userData'

		#debug = True

		engine = create_engine('mysql://%s:%s@%s:%s/user_profile_m?charset=utf8'%(MYSQLUSER, MYSQLPWD, MYSQLADDR, MYSQLPORT))
		conn = engine.connect()
		
		## 1 cache 2 db //todo cache /base

		## for user data
		## user basic data
		user_data = {}
		userid = long(userid)

		sql = 'select * from users where user_id= %s' % (userid)
		#if debug : print sql
		
		rs = conn.execute(sql)
		for row in rs:
			user_data['user_id'] = fieldEncode(row['user_id'])
			user_data['uid']    = fieldEncode(row['guid'])
			user_data['versign_phone'] = fieldEncode(row['phone'])
			user_data['versign_email'] = fieldEncode(row['email'])

		sqlprf = 'select *, u.info_id as data_id from userinfo u inner join userinfo_%s d on u.info_id=d.info_id \
where user_id= %u and (selected=1) and (under=0) %s' % ('%s', userid, '%s')
		print sqlprf

		sql = sqlprf % ('basic', 'limit 1')
		rs = conn.execute(sql)
		for row in rs:
			user_data['birthday'] = fieldEncode(row['birthday'])
			user_data['gender']= fieldEncode(row['gender'])
			user_data['blood'] = fieldEncode(row['blood'])
			user_data['marry'] = fieldEncode(row['marry'])

		## user name data
		sql = sqlprf % ('name', 'limit 1')
		rs = conn.execute(sql)
		row_data = {}
		for row in rs:
			row_data['FN'] = fieldEncode(row['FN'])
			row_data['family_name']= fieldEncode(row['family_name'])
			row_data['given_name'] = fieldEncode(row['given_name'])
			row_data['additional_names']= fieldEncode(row['additional_names'])
			row_data['name_prefix']= fieldEncode(row['name_prefix'])
			row_data['name_suffix']= fieldEncode(row['name_suffix'])
		if len(row_data)>0 : user_data['name'] = row_data

		# user nick for user not for app if exist  
		sql = sqlprf % ('nick', 'limit 1')
		rs = conn.execute(sql)
		for row in rs:
			user_data['nick']  = fieldEncode(row['nick'])
			user_data['avatar']= fieldEncode(row['avatar'])
			user_data['sign']  = fieldEncode(row['sign'])

		## user email data / mutiline
		sql = sqlprf % ('emails', 'order by row_ord')
		rs = conn.execute(sql)
		rows = []
		for row in rs:
			row_data = {}
			rows.append(row_data)
			row_data['data_id'] = fieldEncode(row['data_id'])
			row_data['email_type'] = fieldEncode(row['email_type'])
			row_data['email']  = fieldEncode(row['email'])
			row_data['versign']  = fieldEncode(row['versign'])
		if len(rows)>0 : user_data['emails'] = rows

		## user tel data / mutiline
		sql = sqlprf % ('telephones', 'order by row_ord')
		rs = conn.execute(sql)
		rows = []
		for row in rs:
			row_data = {}
			rows.append(row_data)
			row_data['data_id'] = fieldEncode(row['data_id'])
			row_data['tel_type'] = fieldEncode(row['tel_type'])
			row_data['tel_number']  = fieldEncode(row['tel_number'])
			row_data['versign']  = fieldEncode(row['versign'])
			#row_data['tel_city'] = fieldEncode(row['tel_city'])
			#row_data['tel_region']  = fieldEncode(row['tel_region'])
		if len(rows)>0 : user_data['telephones'] = rows

		## user im list data / muti property / dict 
		sql = sqlprf % ('im', '')
		rs = conn.execute(sql)
		row_data = {}
		for row in rs:
			row_data[fieldEncode(row['im_name'])] = fieldEncode(row['im'])
		if len(row_data)>0 : user_data['im'] = row_data

		## user url list data / muti property / dict
		sql = sqlprf % ('url', '')
		rs = conn.execute(sql)
		row_data = {}
		for row in rs:
			row_data[fieldEncode(row['url_name'])] = fieldEncode(row['url'])
		if len(row_data)>0 : user_data['url'] = row_data

		## user photos data / mutiline
		sql = sqlprf % ('photos', 'order by row_ord')
		rs = conn.execute(sql)
		rows = []
		for row in rs:
			row_data = {}
			rows.append(row_data)
			row_data['data_id'] = fieldEncode(row['data_id'])
			row_data['photo_class'] = fieldEncode(row['photo_class'])
			row_data['photo_caption']  = fieldEncode(row['photo_caption'])
			row_data['photo_url']  = fieldEncode(row['photo_url'])
		if len(rows)>0 : user_data['photos'] = rows

		## user adrress data / mutiline
		sql = sqlprf % ('addresses', 'order by row_ord')
		rs = conn.execute(sql)
		rows = []
		for row in rs:
			row_data = {}
			rows.append(row_data)
			row_data['data_id'] = fieldEncode(row['data_id'])
			row_data['address_type'] = fieldEncode(row['address_type'])
			row_data['post_office_address']  = fieldEncode(row['post_office_address'])
			row_data['extended_address']  = fieldEncode(row['extended_address'])
			row_data['street']   = fieldEncode(row['street'])
			row_data['locality'] = fieldEncode(row['locality'])
			row_data['region']   = fieldEncode(row['region'])
			row_data['postal_code']  = fieldEncode(row['postal_code'])
			row_data['country']  = fieldEncode(row['country'])
		if len(rows)>0 : user_data['addresses'] = rows

		## user organization data / mutiline 
		sql = sqlprf % ('organizations', 'order by row_ord')
		rs = conn.execute(sql)
		rows = []
		for row in rs:
			row_data = {}
			rows.append(row_data)
			row_data['data_id'] = fieldEncode(row['data_id'])
			row_data['org_name'] = fieldEncode(row['org_name'])
			row_data['org_unit'] = fieldEncode(row['org_unit'])
			row_data['org_subunit']  = fieldEncode(row['org_subunit'])
			row_data['title'] = fieldEncode(row['title'])
			row_data['role']  = fieldEncode(row['role'])
			row_data['work_field']  = fieldEncode(row['work_field'])
			row_data['org_logo']  = fieldEncode(row['org_logo'])
			row_data['org_into_date']  = fieldEncode(row['org_into_date'])
			row_data['org_leave_date'] = fieldEncode(row['org_leave_date'])
		if len(rows)>0 : user_data['organizations'] = rows

		## user education data / mutiline
		sql = sqlprf % ('educations', 'order by row_ord')
		rs = conn.execute(sql)
		rows = []
		for row in rs:
			row_data = {}
			rows.append(row_data)
			row_data['data_id'] = fieldEncode(row['data_id'])
			row_data['education']  = fieldEncode(row['education'])
			row_data['school_name'] = fieldEncode(row['school_name'])
			row_data['school_city']  = fieldEncode(row['school_city'])
			row_data['school_into_date']  = fieldEncode(row['school_into_date'])
			row_data['school_leave_date']  = fieldEncode(row['school_leave_date'])
		if len(rows)>0 : user_data['educations'] = rows
		
		## user sound data / mutiline
		sql = sqlprf % ('sounds', 'order by row_ord')
		rs = conn.execute(sql)
		rows = []
		for row in rs:
			row_data = {}
			rows.append(row_data)
			row_data['data_id'] = fieldEncode(row['data_id'])
			row_data['sound_class'] = fieldEncode(row['sound_class'])
			row_data['sound_caption'] = fieldEncode(row['sound_caption'])
			row_data['sound_url']  = fieldEncode(row['sound_url'])
			rows.append(row_data)
		if len(rows)>0 : user_data['sounds'] = rows

		## user geo data / mutiline
		sql = sqlprf % ('geoes', 'order by row_ord')
		rs = conn.execute(sql)
		rows = []
		for row in rs:
			row_data = {}
			rows.append(row_data)
			row_data['data_id'] = fieldEncode(row['data_id'])
			row_data['geo_type'] = fieldEncode(row['geo_type'])
			row_data['tz']  = fieldEncode(row['tz'])
			row_data['geo_lat']  = fieldEncode(row['geo_lat'])
			row_data['geo_lng']  = fieldEncode(row['geo_lng'])
			row_data['record_date']  = fieldEncode(row['record_date'])
		if len(rows)>0 : user_data['geoes'] = rows


		# user addition field and common data , 可兼容上面的格式
		'''
		data_class 1->n row_ord 1->1 info_id 
		{                                                 data_class    row_ord -- info_id
			data_field:data_value,                     <- null          null
			data_class:{data_field:data_value,...},    <- not null      null
			data_class:[{data_field:data_value,...}    <- not null      not null
			           ,{data_field:data_value,...}],  
			invalid                                    <- null          not null
		}
		'''
		sql = 'select *, userinfo.info_id as infoid from userinfo inner join userinfo_data on userinfo.info_id=userinfo_data.info_id \
where user_id= %s and (selected=1) and (under=0) \
order by user_id, data_class, row_ord, userinfo.info_id' % (userid)
		rs = conn.execute(sql)
		dataclass = ''
		infoid = 0
		for row in rs:
			if row['data_class'] == None:
				user_data[fieldEncode(row['data_field'])]= fieldEncode(row['data_value'])
			else:
				if dataclass != row['data_class'] :
					dataclass = row['data_class']
					infoid = 0
				if infoid != row['infoid'] :
					infoid = row['infoid']
					row_data = {}
					d = dataclass.encode('utf8')
					row_data['data_id'] = fieldEncode(infoid)
					if d in user_data :
						if type(user_data[d]) is dict:
							prevrow = user_data[d]
							user_data[d] = [prevrow,row_data]
						elif type(user_data[d]) is list :
							user_data[d].append(row_data)
						else :
							user_data[d] = row_data
					else :
						user_data[d] = row_data
				else :
					row_data[fieldEncode(row['data_field'])]= fieldEncode(row['data_value'])


		# for application user data
		# application nick
		appdata = {}
		sql = 'select *,apps.app_id as appid from user_account inner join apps on user_account.app_id = apps.app_id \
where user_id= %s ' % (userid)
		rs = conn.execute(sql)
		for row in rs:
			app_id = row['appid']
			if app_id not in appdata :
				appdata[app_id]={}
			appdata[app_id]['app_id']= fieldEncode(app_id)
			appdata[app_id]['app_name']= fieldEncode(row['app_name'])
			appdata[app_id]['app_account']= fieldEncode(row['app_account'])
			appdata[app_id]['app_nick'  ]= fieldEncode(row['app_nick'])
			appdata[app_id]['app_avatar']= fieldEncode(row['app_avatar'])
			appdata[app_id]['last_status']= fieldEncode(row['app_last_status'])
			appdata[app_id]['account_disabled']= fieldEncode(row['account_disabled'])
			

		# for application comm user data
		'''
		data_class 1->n row_ord 1->1 info_id 
		{
			app_id:n
			app_account:abcd
		                                                  data_class    row_ord -- info_id
			data_field:data_value,                     <- null          null
			data_class:{data_field:data_value,...},    <- not null      null
			data_class:[{data_field:data_value,...}    <- not null      not null
			           ,{data_field:data_value,...}],  
			invalid                                    <- null          not null
		}
		'''

		sql = 'select *, userinfo.info_id as infoid from userinfo inner join userinfo_data on userinfo.info_id=userinfo_data.info_id \
where (user_id= %s) and (selected=1) and (under=1) and (not isnull(app_id)) \
order by app_id, user_id, data_class, row_ord, userinfo.info_id' % (userid)
		rs = conn.execute(sql)
		dataclass = ''
		infoid = 0
		appid  = None
		approw = {}
		for row in rs:
			if appid != row['app_id'] :
				appid = row['app_id']
				if appid in appdata :
					approw = appdata[appid]
				else:
					approw = {}
					appdata[appid] = approw

			if row['data_class'] == None:
				approw[fieldEncode(row['data_field'])]= fieldEncode(row['data_value'])
			else:
				if dataclass != row['data_class'] :
					dataclass = row['data_class']
					infoid = 0
				if infoid != row['infoid'] :
					infoid = row['infoid']
					row_data = {}
					row_data[fieldEncode(row['data_field'])]= fieldEncode(row['data_value'])
					d = fieldEncode(dataclass)
					if d in approw :
						if type(approw[d]) is dict:
							prevrow = approw[d]
							approw[d] = [prevrow,row_data]
						elif type(approw[d]) is list :
							approw[d].append(row_data)
						else :
							approw[d] = row_data
					else :
						approw[d] = row_data
				else :
					row_data[fieldEncode(row['data_field'])]= fieldEncode(row['data_value'])

		if len(appdata)>0 :
			appdatas = []
			for (k,v) in appdata.iteritems():
				appdatas.append(v)
			user_data['applications']=appdatas
		
		
		conn.close()
		return user_data

	def toLimitString(self,param):
		limit = ''
		if type(param) is dict:
			if ('offset' in param ) and (str(param['offset']).isdigit()):
				limit = ' limit %s' % (param['offset'])
			if ('limit' in param) and (str(param['limit']).isdigit()):
				if limit == '':
					limit = ' limit %s ' % (param['limit'])
				else :
					limit = ' %s,%s '%(limit,param['limit'])
			else :
				if limit != '' :
					limit = ' %s,%s '%(limit,'18446744073709551615')
		return limit

	def userInfoData(self, rs_info, dict_info, group_id_name=''):
		dataclass = ''
		infoid = 0
		groupid  = None
		inforow = {}
		for row in rs_info:
			if group_id_name != '' :
				if groupid != row[group_id_name] :
					groupid = row[group_id_name]
					if groupid in dict_info :
						inforow = dict_info[groupid]
					else :
						inforow = {}
						dict_info[groupid] = inforow
			else :
				inforow = dict_info

			if row['data_class'] == None:
				inforow[fieldEncode(row['data_field'])]= fieldEncode(row['data_value'])
			else:
				if dataclass != row['data_class'] :
					dataclass = row['data_class']
					infoid = 0
				if infoid != row['infoid'] :
					infoid = row['infoid']
					row_data = {}
					row_data[fieldEncode(row['data_field'])]= fieldEncode(row['data_value'])
					d= fieldEncode(dataclass)
					if d in inforow :
						if type(inforow[d]) is dict:
							prevrow = inforow[d]
							inforow[d] = [prevrow,row_data]
						elif type(inforow[d]) is list :
							inforow[d].append(row_data)
						else :
							inforow[d] = row_data
					else :
						inforow[d] = row_data
				else :
					row_data[fieldEncode(row['data_field'])]= fieldEncode(row['data_value'])
		return 


	def userRelationDatas(self, userid=0, relUserid=0, relid=0, param={}, friend=0):
		engine = create_engine('mysql://%s:%s@%s:%s/user_profile_m?charset=utf8'%(MYSQLUSER, MYSQLPWD, MYSQLADDR, MYSQLPORT))
		conn   = engine.connect()
		
		## 1 cache 2 db

		## for user data
		## user basic data
		rel_data = {}
		limit = ''

		#try :
		if userid != 0 :
			f = 'user_id'
			userid = long(userid)
			i = userid
			limit = self.toLimitString(param)
			print userid
			friend = long(friend)
		elif relUserid != 0 :
			f = 'relation_user_id'
			relUserid = long(relUserid)
			i = relUserid
			limit = self.toLimitString(param)
		else :
			f = 'rel_id'
			relid = long(relid)
			i = relid
		#except :
		#	return None


		if friend == 0:
			sql = 'select * from user_relation where (%s = %s) and (deleted=0) order by contact_alias  %s' % (f,i,limit)
		elif userid != 0 :
			if  friend == 1 : #	marge app, 忽略应用归属计算双向好友
				sql = 'SELECT distinct user_relation.* FROM user_relation inner join  user_relation  ur \
on user_relation.relation_user_id = ur.user_id  \
where user_relation.user_id = %s and ur.relation_user_id = %s order by contact_alias %s' % (i,i,limit)
			elif friend == 2: # relation with app check, 不忽略应用归属计算好友
				sql = 'SELECT distinct user_relation.* FROM user_relation inner join  user_relation  ur \
on user_relation.relation_user_id = ur.user_id  and user_relation.app_id= ur.app_id \
where user_relation.user_id = %s and ur.relation_user_id = %s order by contact_alias  %s' % (i,i,limit)


		idlist = []
		rs = conn.execute(sql)
		for row in rs:
			relrow = {}
			idlist.append(str(row['rel_id']))
			rel_data[row['rel_id']]= relrow
			relrow['app_id']= fieldEncode(row['app_id'])
			relrow['contact_user_id'] = fieldEncode(row['relation_user_id'])
			relrow['contact_type']  = fieldEncode(row['relation_type'])
			relrow['contact_alias']= fieldEncode(row['contact_alias'])
			relrow['contact_group']= fieldEncode(row['contact_group'])
			relrow['contact_note'] = fieldEncode(row['contact_note'])
			relrow['contact_lastdate']= fieldEncode(row['contact_lastdate'])
			relrow['@user_id']= fieldEncode(row['user_id'])
			userid = row['user_id']

		idliststr = ','.join(idlist)
		print idliststr
		
		if len(rel_data)<=0 :
			if (f == 'rel_id') :
				return {}
			else:
				return []

		sql = 'select * from userinfo inner join userinfo_data on userinfo.info_id=userinfo_data.info_id \
where (selected=1) and (under=2) and (rel_id in (%s)) \
order by rel_id, data_class, row_ord, userinfo.info_id' % (idliststr)
		rs = conn.execute(sql)
		conn.close()
		dataclass = ''
		infoid = 0
		rel_id = 0
		relrow = {}
		for row in rs:
			if rel_id != row['rel_id'] :
				rel_id = row['rel_id']
				if rel_id in rel_data :
					relrow = rel_data[rel_id]
				else:
					relrow = None

			if relrow != None :
				if row['data_class'] == None:
					relrow[fieldEncode(row['data_field'])]= fieldEncode(row['data_value'])
				else:
					if dataclass != row['data_class'] :
						dataclass = row['data_class']
						infoid = 0
					if infoid != row['info_id'] :
						infoid = row['info_id']
						row_data = {}
						row_data[fieldEncode(row['data_field'])]= fieldEncode(row['data_value'])
						if dataclass.encode('utf8') in relrow :
							if type(relrow[dataclass.encode('utf8')]) is dict:
								prevrow = relrow[dataclass.encode('utf8')]
								relrow[dataclass.encode('utf8')] = [prevrow,row_data]
							elif type(relrow[dataclass.encode('utf8')]) is list :
								relrow[dataclass.encode('utf8')].append(row_data)
							else :
								relrow[dataclass.encode('utf8')] = row_data
						else :
							relrow[dataclass.encode('utf8')] = row_data
					else :
						row_data[fieldEncode(row['data_field'])]= fieldEncode(row['data_value'])
		if (f == 'rel_id') and (relid in rel_data):
			return rel_data[relid]
		else :
			result = []
			for v in rel_data.itervalues() :
				result.append(v)
			return result


	def userRelationList(self, userid=0, relUserid=0, param = {}):
		print dict(userid=userid,param=param)
		engine = create_engine('mysql://%s:%s@%s:%s/user_profile_m?charset=utf8'%(MYSQLUSER, MYSQLPWD, MYSQLADDR, MYSQLPORT))
		conn   = engine.connect()

		limit = self.toLimitString(param)

		rel_data = {}
	
		f = ''
		if userid != 0 :
			f = 'user_id'
			i = userid
		elif relUserid != 0 :
			f = 'relation_user_id'
			i = relUserid
		
		if f == '' : 
			return []
		else :
			print 'userRelationList,',param
			sql = 'select * from user_relation where (%s = %s) and (deleted=0) order by contact_alias %s' % (f,i,limit)
			print sql
			rs = conn.execute(sql)
			conn.close()
			r = []
			for row in rs:
				r.append(row['rel_id'])
			return r

	
	def appInfoData(self, app_id, param = {}):
		engine = create_engine('mysql://%s:%s@%s:%s/user_profile_m?charset=utf8'%(MYSQLUSER, MYSQLPWD, MYSQLADDR, MYSQLPORT))
		conn   = engine.connect()

		sql = 'select * from apps where (app_id = %s) ' % (app_id)
		rs = conn.execute(sql)
		appInfo = {}
		for row in rs:
			appInfo['app_id'] = fieldEncode(row['app_id'])
			appInfo['app_name'] = fieldEncode(row['app_name'])
			appInfo['app_type'] = fieldEncode(row['app_type'])
		conn.close()
		return appInfo


	def appInfoDataList(self, param = {}):
		engine = create_engine('mysql://%s:%s@%s:%s/user_profile_m?charset=utf8'%(MYSQLUSER, MYSQLPWD, MYSQLADDR, MYSQLPORT))
		conn   = engine.connect()

		limit = self.toLimitString(param)

		sql = 'select * from apps ' + limit
		rs = conn.execute(sql)
		apps = []
		for row in rs:
			appInfo = {}
			appInfo['app_id'] = fieldEncode(row['app_id'])
			appInfo['app_name'] = fieldEncode(row['app_name'])
			appInfo['app_type'] = fieldEncode(row['app_type'])
			apps.append(appinfo)
		conn.close()
		return apps


	'''
	# struct name : user.full,base,ext ; contact.base
	'''
	'''
	# get api data struct define
	#.. api data struct ..
	# api name
	#	struct
	#		struct  <- user define
	#		class row	<- data logic 
	#			row name:filed	<- user define
	#			row field	<- user define
	#		field	<- user define
	#..                 ..
	#	field_type	field_source		param
	#------------------------------------------------------------------------------
	#	list		users,contacts		idlist		data mutiline record
	#	record		user,app,relation	id			data record (exp: userinfo)
	#	classlist	class name			Inherit		data record class  muti line
	#	class		class name			Inherit		data record class  one line
	#	field		data field name		Inherit		field name
	#	classfield	field in class		Inherit		class and field name
	#	param		param name
	#	relfield	rel record field				rel_id_field, rel_rec_name	
	#
	# 获取api返回结构定义
	'''
	#	todo: struct list and first struct
	#
	def apiStruct(self, dataStructName, root=True):
		engine = create_engine('mysql://%s:%s@%s:%s/user_profile_m?charset=utf8'%(MYSQLUSER, MYSQLPWD, MYSQLADDR, MYSQLPORT))
		conn   = engine.connect()
		apiDefine = []
		if root :
			sql = "select * from apis_struct where struct_name = '%s' and field_ord = 0 " % (dataStructName)
		else :
			sql = "select * from apis_struct where struct_name = '%s' order by field_ord " % (dataStructName)
		rs = conn.execute(sql)
		conn.close()
		for row in rs :
			field = {}
			apiDefine.append(field)
			field['caption']= fieldEncode(row['field_caption'])
			field['type']   = fieldEncode(row['field_type'])
			field['source'] = fieldEncode(row['field_source'])
			field['rel_id_field'] = fieldEncode(row['rel_id_field'])
			field['rel_rec_name'] = fieldEncode(row['rel_rec_name'])
			if field['type'] in ('list','record','class','classlist') :
				field['struct'] = self.apiStruct(row['field_struct'],False)
			else :
				field['struct'] = fieldEncode(row['field_struct'])
		conn.close()
		if root :
			if len(apiDefine)>0 :
				return apiDefine[0]
			else :
				return None
		else :
			return apiDefine



	
	# 解析api返回结构定义
	'''
		返回数据的结构
		api:[
			caption:[						<- record list
				[							<- record
					(caption,value)			<- field 
					caption:[				<- data class
						(caption,value)		<- field for class
					]
					caption:[				<- data class list
						[
							(caption,value)
						],[
							(caption,value)
						]
					]
				]，[
					...
				]
			]

		]
	'''
	def apiStructFieldParse(self, record, data_id, dataStructField, parentData, param={}):
		c = None
		field = dataStructField
		result = None
		if type(data_id) in (int, unicode, str, long) :
			data_id = str(data_id)
		caption = field['caption']
		if caption == None : caption = ''
		if caption == '*' : caption = field['source']
		caption = fieldEncode(caption)
		if field['type']=='field' :
			if type(record) is dict:
				if (field['struct'] in record):
					c = record[field['struct']]
					if (type(c) is list) and (len(c)>0) :
						c = c[0]
				else :
					c = record
				if type(c) is dict:
					if field['source'] == '*':
						result = []
						for (k,v) in c.iteritems():
							if (len(k)>0) and (str(k)[0]!='@'):
								if (type(v) not in (list,dict,tuple)): #(int, unicode, str, long)
									parentData[k]=v
					elif (field['source'] in c) :
						parentData[caption]=c[field['source']]
		#elif field['type']=='classfield' :
		#	if (type(record) is dict) and (field['struct'] in record):
		#		c = record[field['struct']]
		#		if (type(c) is list) and (len(c)>0) :
		#			c = c[0]
		#		if (type(c) is dict) and (field['source'] in c) :
		#			parentData[caption]=c[field['source']]
		elif field['type']=='param' :
			if (type(param) is dict) and (field['source'] in record) :
				parentData[caption]=param[field['source']]
		elif field['type']=='relfield' :
			if (field['source'] != '') and (field['rel_id_field']!='') and (field['rel_id_field'] in record) and (field['rel_rec_name'] != '') :
				data_id = record[field['rel_id_field']]
				if field['rel_rec_name'] == 'user' :
					r = self.userData(data_id, param)
				elif field['rel_rec_name'] == 'relation' :
					r = self.userRelationDatas(relid=data_id)
				elif field['rel_rec_name'] == 'app':
					r = self.appInfoData(data_id, param)
				if type(r) is dict :
					if (field['struct'] != '') and (field['struct'] in r):
						r = r[field['struct']]
				if (type(r) is dict) and (field['source'] in r) :
					parentData[caption]=r[field['source']]
		elif (field['type']=='class') or (field['type']=='classlist'):
			if type(field['struct']) is list :
				if (type(record) is dict) :
					r = None
					if (field['source'] in record):
						r = {caption:record[field['source']]}
					if (field['source'] == '*') :
						r = record
					if type(r) is dict:
						for (caption,c) in r.iteritems() :
							if type(c) is list :
								cl = []
								parentData[caption]= cl
								for r in c:
									cl.append(self.apiStructParse(r,field['struct'],param))
							elif type(c) is dict:
								parentData[caption] = self.apiStructParse(c,field['struct'],param)
		elif field['type'] == 'record' :
			if (field['source'] != '') and (type(field['struct']) is list) :
				if (data_id == '') and (type(record) is dict) and (field['rel_id_field']!='') and (field['rel_id_field'] in record):
					data_id = record[field['rel_id_field']]
				if (data_id != '') :
					if field['source'] == 'user' :
						r = self.userData(data_id, param)
						if type(r) is dict :
							parentData[caption] = self.apiStructParse(r,field['struct'],param)
					elif field['source'] == 'relation' :
						r = self.userRelationDatas(relid=data_id)
						if type(r) is dict :
							parentData[caption] = self.apiStructParse(r,field['struct'],param)
					elif field['source'] == 'app':
						r = self.appInfoData(data_id, param)
						if type(r) is dict :
							parentData[caption] = self.apiStructParse(r,field['struct'],param)
					#elif field['source'] == '@a':
		elif field['type'] == 'list' :
			if (field['source'] != '') and (type(field['struct']) is list) :
				idlist = None
				if type(data_id) is list :
					idlist = data_id
				if (data_id == '') and (type(record) is dict) and (field['rel_id_field']!='') and (field['rel_id_field'] in record):
					data_id = record[field['rel_id_field']]
				if field['source'] == 'relation' :
					rellist=[]
					parentData[caption] = rellist
					if (type(data_id) is str) and (data_id != '') :
						idlist = self.userRelationList(data_id,0  , param)
					if type(idlist) is list :
						for rel in idlist :
							rellist.append(self.apiStructParse(self.userRelationDatas(relid=rel),field['struct'],param))
				if field['source'] == 'friend' :
					rellist=[]
					parentData[caption] = rellist
					if (type(data_id) is str) and (data_id != ''):
						friends = self.userRelationDatas(userid=data_id,param=param,friend=1)
						if type(friends) is list :
							for rel in friends :
								rellist.append(self.apiStructParse(rel,field['struct']))
		return result


	def apiStructParse(self, record, dataStruct, param={}):
		datas = {}
		for field in dataStruct :
			self.apiStructFieldParse(record, '', field, datas, param)
		return datas
			

	def apiData(self, data_id, apiDefineName, param={}):
		#print dict(user_id=user_id,param=param)
		apiStru = self.apiStruct(apiDefineName)
		datas = {}
		self.apiStructFieldParse(None, data_id, apiStru, datas, param)
		if apiStru['caption'] in datas:
			return datas[apiStru['caption']]
		else :
			return None

	def isEMail(self, mail): 
		if (mail.find('@') >=0) and (mail.find('.')>=0) :
			return True
		else :
			return False

	def isTel(self, tel): # todo
		if (tel[0]=='+') or ((tel[0]>='0') and (tel[0]<='9')):
			return True
		else :
			return False

	
	'''

	'''
	
	### api list
	## user api
	# user base info
	# return User Base Data Struct
	def userBaseData(self, user_id):
		return self.apiData(user_id,'api-user-baseinfo')

	# user full info
	# return User Full Data Struct
	def userFullData(self, user_id):
		return self.apiData(user_id,'api-user-fullinfo')

	def userLookup(self, TelOrEmail='', retType='full'):
		#format tel
		#format email
		if TelOrEmail == '' : return None
		if self.isEMail(TelOrEmail):
			sql = "select * from userinfo inner join userinfo_email on userinfo.info_id=userinfo_email.info_id where email like '%s' order by versign desc limit 1" % (TelOrEmail)
		if self.isTel(TelOrEmail):
			sql = "select * from userinfo inner join userinfo_tel on userinfo.info_id=userinfo_tel.info_id where tel like '%s' order by versign desc limit 1" % (TelOrEmail)
		#print sql
		engine = create_engine('mysql://%s:%s@%s:%s/user_profile_m?charset=utf8'%(MYSQLUSER, MYSQLPWD, MYSQLADDR, MYSQLPORT))
		conn   = engine.connect()
		rs = conn.execute(sql)
		conn.close()
		for row in rs:
			if retType=='full':
				return self.userFullData(row['user_id'])
			elif retType=='base':
				return self.userBaseData(row['user_id'])
			elif retType=='id':
				return row['user_id']
		return None

	## user contacts info
	# return contacts with user base data
	def userContacts(self, user_id, param={}):
		return self.apiData(user_id,'api-user-contacts', param)

	# return contacts relation id list
	def userRelationsIdList(self, user_id, param={}):
		return self.userRelationList(user_id,0,param)

	# return relation data for relation id
	def	userRelationData(self, rel_id):
		return self.userRelationDatas(relid = rel_id)
	
	# return Contact data for relation id (with user base)
	def	userContactData(self, rel_id):
		return self.apiData(rel_id,'api-relation-info')


	## user in contacts info
	# return contacts with user base data
	def userInContacts(self, user_id, param={}):
		idlist = self.userInRelationsIdList(user_id, param)
		print idlist
		return self.apiData(idlist,'api-user-in-contacts', param)

	# return In contacts relation id list
	def userInRelationsIdList(self, user_id, param={}):
		return self.userRelationList(0,user_id, param)

	'''
	def userContactsIdList(self, user_id, param={}):
		return self.userRelationList(user_id, param)

	def userInContactsIdList(self, user_id, param={}):
		return self.userRelationList(0,user_id, param)
	'''

	## user friend list
	def userFriends(self, user_id, param={}):
		return self.apiData(user_id,'api-user-friends',param)

	## apps info
	def userApps(self, user_id, param={}):
		#r = self.apiData(user_id,'user-applications', param)
		r = self.userData(user_id)
		if 'applications' in r:
			return r['applications']
		else :
			return []

	###

	def userBatchPut(self, user_id, value):
		if userid == None:
			return
		engine = create_engine('mysql://%s:%s@%s:%s/user_profile?charset=utf8'%(MYSQLUSER, MYSQLPWD, MYSQLADDR, MYSQLPORT))
		conn = engine.connect()
		conn.close()
		result = conn.execute(sql)

	def userPut(self, userData):
		return

	def userPatch(self, userid, userData):
		return

	## user addsl,
	def userPost(self, app_id, user_id, userData):
		if type(userData) is dict:
			userData.clone()

			for (k,v) in userData.iteritems():
				print k
		return
		
if __name__ == '__main__':
	d = DatabaseWorker()
	print d.userShow(123874646464646)
