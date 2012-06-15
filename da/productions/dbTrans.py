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
            #print user_id
            do_insert = True #==None 直接新增
        else:
            do_insert = False

        udf = extractUserDataFields(userData)
        for uf in udf:
            if not do_insert:
                fieldInsert = False
                sqlt = userFieldDataToExistsSql(user_id,app_id,uf)
                #print sqlt[0] % tuple(sqlt[1])
                rs = conn.execute(sqlt[0],sqlt[1])
                if rs.rowcount>0:
                    row = rs.fetchone()
                    info_id = row['info_id']
                    sqlt = userFieldDataToUpdateSql(user_id,app_id,info_id,uf)
                    #print sqlt[0] % tuple(sqlt[1])
                    conn.execute(sqlt[0],sqlt[1])
                    fieldInsert = False
                else:
                    fieldInsert = True
            if do_insert or fieldInsert:
                sqlt = userFieldDataToInsertSql(user_id,app_id,uf)
                #print sqlt[0] % tuple(sqlt[1])
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
        rs = conn.execute("select * from tt_user where registered_phone_number=mobile_phone limit 1")
        for row in rs:
            ud={'versign_phone':row['registered_phone_number'],
                'uid':guidctoa(row['card_id']),
                'name':{'FN':row['display_name']},
                'telephones':[  {'tel_type':'mobile','tel_number':trim(row['mobile_phone'])},
                                {'tel_type':'work','tel_number':row['work_phone']}],
                'emails':{'email_type':'person','email':trim(row['email'])},
                'organizations':{'org_name':trim(row['company']),'org_unit':trim(row['department']),'role':trim(row['position'])},
                'educations':{'school_name':trim(row['school'])},
                'addresses':{'post_office_address':row['location']},
                'im':{'QQ':trim(row['qq']),'MSN':trim(row['msn'])},
                'url':{'homepage':trim(row['website'])},
                'source_ident':{'source_name':'user','source_id':row['card_id']}
                }
            if ud['telephones'][1]['tel_number'] in [None,'',u'']:
                del ud['telephones'][1]
            #清除空数据
            #printJsonData(ud)
            print row['mobile_phone'], row['display_name']
            TrimEmptyDataField(ud)
            #printJsonData(ud)
            self.userPut(ud,2)
        
        rs = conn.execute("select * from tt_relation  limit 10")
        d = DatabaseWorker()
        engine_u = create_engine('mysql://%s:%s@%s:%s/user_profile_m?charset=utf8'%(MYSQLUSER, MYSQLPWD, MYSQLADDR, MYSQLPORT))
        conn_u = engine_u.connect()
        for row in rs:
            phone= str(row['phone'])
            contact= str(row['contact'])

            user_id = d.userLookup(phone, 'id')
            contact_uid = d.userLookup(contact, 'id')

            if contact_uid == None:
                # add user
                sql = 'insert into users (phone,user_state) values (%s,0); select @userid := LAST_INSERT_ID();'
                rsi = conn_u.execute(sql,contact)
                if rsi.rowcount>0:
                    rsi = conn_u.execute('select @userid')
                    contact_uid=rsi.fetchone()[0]

            if user_id == None:
                # add user
                sql = 'insert into users (phone,user_state) values (%s,0); select @userid := LAST_INSERT_ID();'
                rsi = conn_u.execute(sql,contact)
                if rsi.rowcount>0:
                    rsi = conn_u.execute('select @userid')
                    user_id=rsi.fetchone()[0]

            if (contact_uid != None) and (user_id != None):
                sql = 'insert into user_relation (user_id,relation_user_id,app_id) values (%s,%s,2)'
                conn_u.execute(sql, user_id, contact_uid)

            print user_id,contact_uid
        return

if __name__ == '__main__':
    d = DatabaseWorker()
    print d.userShow(123874646464646)
