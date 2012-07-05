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
                'uid':guidctoa(row['card_id']),
                'name':{'FN':row['display_name']},
                'telephones':[  {'tel_type':'mobile','tel_number':trim(row['mobile_phone']),'serial':1},
                                {'tel_type':'work','tel_number':trim(row['work_phone']),'serial':2}],
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
            #Çå³ý¿ÕÊý¾Ý
            #printJsonData(ud)
            print row['mobile_phone'], row['display_name']
            d.userPut(ud,2,2)
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

