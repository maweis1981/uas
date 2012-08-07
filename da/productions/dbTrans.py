#!/usr/bin/env python
# encoding: utf-8
"""
dbTrans.py
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
from dbConnections import *
import MySQLdb

import time


qiekeJob = {
1:u'学生仔',
2:u'教师',
3:u'打工仔',
4:u'老板',
5:u'失业',
6:u'其他',
10:u'互联网',
11:u'计算机技术',
12:u'通信',
13:u'广告设计',
14:u'公关公关',
15:u'媒体与出版',
16:u'文化艺术',
17:u'法律',
18:u'金融',
19:u'咨询',
20:u'酒店及餐饮',
21:u'旅游',
22:u'体育及运动',
23:u'商品贸易',
24:u'制造业制造业',
25:u'医疗及健康护理',
26:u'教育	',
27:u'科研',
28:u'房地产',
29:u'交通与物流',
30:u'农林牧渔业',
31:u'政府及公共事业',
32:u'非盈利组织',
150:u'其他',
}
class DatabaseTrans(object):

    def __init__(self):
        self.dbconns = DatabaseConnections()


    def ttcontactTrans(self, usermax = 0, relmax = 10, dbname='ttcontactdb'):
        d = DatabaseWorker(self.dbconns)

        connstring = 'mysql://%s:%s@%s:%s/%s?charset=utf8'%(MYSQLUSER, MYSQLPWD, '192.168.91.48', MYSQLPORT, dbname)
        engine = create_engine(connstring)
        conn = engine.connect()
        rs = conn.execute("select * from tt_user where registered_phone_number=mobile_phone limit %s", usermax)
        for row in rs:
            ud={'versign_phone':row['registered_phone_number'],
                'guid':guidctoa(row['card_id']),
                'name':{'FN':row['display_name']},
                'telephones':[  {'tel_type':'mobile','tel_number':trim(row['mobile_phone']),'serial':1},
                                {'tel_type':'tel','tel_number':trim(row['work_phone']),'serial':2}],
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
            d.userPut(ud,2)
        rs.close()
        
        rs = conn.execute("select * from tt_relation  limit %s", relmax)
        s = []
        for row in rs:
            phone= str(row['phone'])
            contact= str(row['contact'])
            r = d.contactPut(2,[[phone,contact,{}]],contact_style_phone_1_1)
            s = s + [str(phone),str(contact),'\t']
            if r != None:
                s = s + [str(r[0][0]),str(r[0][1]),'\n']
            if len(s)>=240:
                #print ','.join(s)
                print phone, contact
                s=[]

        rs.close()
        print ','.join(s)
        conn.close()
        return
    
    def qiekeTrans(self, usermax = 10, relmax = 0, dbname='db2_user_0_0'):
        d = DatabaseWorker(self.dbconns)
        connstring = 'mysql://%s:%s@%s:%s/%s?charset=utf8'%(MYSQLUSER, MYSQLPWD, '192.168.91.48', MYSQLPORT, dbname)
        engine = create_engine(connstring)
        conn = engine.connect()
        rs = conn.execute("SHOW TABLES LIKE 't_user___';")
        tables = rs.fetchall()
        rs.close()
        for table in tables:
            tableName = table[0]
            print tableName
            cur = conn.connection.connection.cursor(MySQLdb.cursors.SSDictCursor)
            cur.execute('select * from '+ tableName + ' limit %s' % usermax)
            for row in cur:
                ud={'applications':{'app_id':3,'app_account':trim(row['user_id']),'app_nick':row['nick_name'],
                                    'last_update':secondToTimestamp(row['last_nicktime']),
                                    'app_last_date':secondToTimestamp(row['last_nicktime'])},
                'source_ident':{'last_update':secondToTimestamp(row['update_time'])},
                'emails':{'email_type':'person','email':trim(row['email']),'versign':row['email_flag']},
                'bi':{'reg_type':trim(row['reg_type']),'src_type':row['src_type'],
                    'user_type':row['user_type'],'reg_time':secondToTimestamp(row['record_time']),
                    'banned':row['banned'],'src_name':row['src_name'],'src_name2':row['src_name2'],
                    'src_name3':row['src_name3'],'src_pass':row['src_pass'],'chanel_id':trim(row['chanel_id'])}
                }
                if row['email_flag'] == 1:
                    ud['versign_email']= trim(row['email'])
                print row['user_id'], row['nick_name']
                d.userPut(ud,3)
            cur.close()
            #break

        rs = conn.execute("SHOW TABLES LIKE 't_user_ext___';")
        tables = rs.fetchall()
        rs.close()
        tables = [('t_user_ext_'+str(i),) for i in range(15,20)]
        for table in tables:
            tableName = table[0]
            print tableName
            cur = conn.connection.connection.cursor(MySQLdb.cursors.SSDictCursor)
            cur.execute('select * from '+ tableName + ' limit %s' % relmax)
            for row in cur:
                ud={'application_account':trim(row['user_id']),
                    'applications':{
                        'app_id':3,
                        'app_account':trim(row['user_id']),
                        'app_avatar':'avatar:3/'+trim(row['icon_id']),
                        'app_sign':trim(row['note'])
                        },
                    'addresses':[
                        {'serial':1,'@address_type':'live',  'region':trim(row['poi_name']), 'post_office_address':trim(row['address']),'postal_code':trim(row['zip']) },
                        {'serial':2,'@address_type':'idcard','region':trim(row['home_poi_name'])}
                        ],
                    'name':{'FN':trim(row['realname'])},
                    'basic':{'gender':listIndexOf(['Female','Male'],row['sex']),
                        'birthday':birthday(row['year'],row['month'],row['day']),
                        'blood':listIndexOf(['','A','B','O','AB'],row['blood_type']),
                        'marry':listIndexOf(['',1,2,3,4,5,6],row['marry'])
                         },
                    'educations':{'education':listIndexOf(['',u'初中',u'高中',u'专科',u'本科',u'硕士',u'博士'],row['education']),
                                  'school_name':row['school']},
                    'ident':{'idcard':trim(row['id_card'])},
                    'im':{'qq':trim(row['qq']), 'msn':trim(row['msn'])},
                    'telephones':[
                        {'serial':1,'tel_type':'mobile','tel_number':trim(row['phone'])},
                        {'serial':2,'tel_type':'tel',   'tel_number':trim(row['tel'])},
                        ],
                    'geoes':{'geo_lat':row['last_lat'],'geo_lng':row['last_lng']},
                    'organizations':{'org_name':trim(row['company']), 'work_field':qiekeJob.get(row['job'],'')},
                    'source_ident':{'last_update':secondToTimestamp(row['update_time'])}
                }
                print row['user_id'], row['realname']
                d.userPut(ud,3)
            cur.close()
            #break


    def youniTrans(self, usermax = 10, relmax = 0, dbname='d_user_00'):
        d = DatabaseWorker(self.dbconns)
        connstring = 'mysql://%s:%s@%s:%s/%s?charset=utf8'%(MYSQLUSER, MYSQLPWD, '192.168.91.48', MYSQLPORT, dbname)
        engine = create_engine(connstring)
        conn = engine.connect()
        rs = conn.execute("SHOW TABLES LIKE 't\_user\_0__';")
        tables = rs.fetchall()
        rs.close()
        for table in tables:
            tableName = table[0]
            print tableName
            cur = conn.connection.connection.cursor(MySQLdb.cursors.SSDictCursor)
            cur.execute('select * from '+ tableName + ' limit %s' % usermax)
            for row in cur:
                ud={'source_ident':{'last_update':(row['updatetime'])},
                    'emails':{'email_type':'person','email':trim(row['email'])},
                    'guid':guidctoa(row['uuid']),
                    'applications':{
                        'app_id':4,
                        'app_account':trim(row['sdid']),
                        'app_nick':trim(row['name']),
                        'app_avatar':iif(isEmpty(row['headurl']),'','avatar:4/'+trimEmpty(row['headurl'])),
                        'app_sign':trim(row['sign'])
                        },
                    'telephones':{'tel_type':'mobile','tel_number':trim(row['phone'])}
                    }
                print row['sdid'], row['name']
                d.userPut(ud,4)
            cur.close()
            break

        conn.execute("use d_contact_000")
        rs = conn.execute("SHOW TABLES LIKE 't_contact_0000';")
        tables = rs.fetchall()
        rs.close()
        for table in tables:
            tableName = table[0]
            print tableName
            cur = conn.connection.connection.cursor(MySQLdb.cursors.SSDictCursor)
            cur.execute('select * from '+ tableName + ' limit %s' % usermax)
            for row in cur:
                userData= {
                    'applications':{
                        'app_id':4,
                        'app_account':trim(row['sdid']),
                        }
                    }
                contactData = {
                    'phone':trim(row['phone']),
                    'name':{'FN':trim(row['name'])},
                    'email':trim(row['email'])
                    }
                relationData = {
                    'contact_alias':trim(row['name']),
                    'contact_lastdate':trim(row['updatetime']) 
                    }
                r = d.contactPut(4,[[userData,contactData,relationData]],contact_style_mix)
                print r
            cur.close()
            break



if __name__ == "__main__":
    
    
    if len(sys.argv)>1 :
        umax=long(sys.argv[1])
    else :
        umax=1
        
    if len(sys.argv)>2 : 
        cmax=long(sys.argv[2])
    else :
        cmax=1
    
    trans = DatabaseTrans()
    t1 = time.time()
    trans.youniTrans(umax,cmax)
    t2 = time.time()
    
    print t1,t2, t2-t1
        
    

