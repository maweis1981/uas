import os,sys,inspect
import logging
import json
import copy
from sqlalchemy import *
from datetime import *
from types import *

from init import *
from dbWorker import DatabaseWorker
from dbWorkerLib import *
from dbTrans import *


def printvalue(value,lev=0):

    lev = lev + 1
    if type(value) is list :
        print
        print '['.rjust(lev*4)
        for v in value :
            #print ''.ljust(lev*4+4),
            printvalue(v,lev)
            print ','
        print ']'.rjust(lev*4),
    elif type(value) is dict :
        print
        print '{'.rjust(lev*4)
        for (k,v) in value.iteritems() :
            print ''.ljust(lev*4),
            print k , ':', 
            printvalue(v,lev)
            print ','
        print '}'.rjust(lev*4),
    elif type(value) is tuple :
        #print ''
        print '('.rjust(lev*4),
        #print ''.ljust(lev*4+4),
        for v in value :
            #print ''.ljust(lev*4+4),
            printvalue(v,lev)
            print ',',
        #print ')'.rjust(lev*4),
        print ')',
    else :
       # print ''.rjust(lev*4), value
        #print  type(value),str(value),
        print  value,
        
def printJsonData(v):
    print json.dumps(v, ensure_ascii=False, indent=4, encoding='utf8')




d = DatabaseWorker()
#v = d.userData(12)
#printJsonData(v)


print '\n--------------------------------'

#v = d.apiStruct('api-relation-info',True)
#printJsonData(v)


#print '\n--------------------------------'

#v = d.userBaseData(12)
#printJsonData(v)


#print '\n--------------------------------'

#v = d.apiStruct('api-user-fullinfo',True)
#printJsonData(v)

#print '\n--------------------------------'

#v = d.userFullData(12)
#printJsonData(v)

#v = d.userLookup('mawei02@snda.com','base')
#v = d.userLookup('13916969212','base')
#printJsonData(v)

#v = d.userRelationList(12)
#printJsonData(v)
    
#print '\n--------------------------------'

#v = d.userContacts(12,dict(offset=0,limit=1))
#printJsonData(v)

#print '\n--------------------------------'

#v = d.userInContacts(12,dict(offset=0,limit=1))
#printJsonData(v)

#print '\n--------------------------------'

#v = d.userRelationsIdList("12",dict(offset=0,limit=2))
#printJsonData(v)

#v = d.userInRelationsIdList("12")
#printJsonData(v)

#print '\n--------------------------------'

#v = d.userRelationData(2)
#printJsonData(v)

#print '\n--------------------------------'

#v = d.userContactData(5)
#printJsonData(v)

#print '\n--------------------------------'

#v = d.userInContacts(12,dict(offset=1,limit=1))
#printJsonData(v)

#v = d.userApps(12)
#printJsonData(v)

#print '\n--------------------------------'

#v = d.userRelationDatas(userid=12,friend=1)
#printJsonData(v)

#v = d.apiData(12,'api-user-friends')
#printJsonData(v)

#print '\n--------------------------------'

'''
engine = create_engine('mysql://%s:%s@%s:%s/user_profile_m?charset=utf8'%(MYSQLUSER, MYSQLPWD, MYSQLADDR, MYSQLPORT))
conn   = engine.connect()

sql="insert into users (guid,phone,email,user_state) values ('7c0dd3fa757211e1a5abf04da2086e9d','18618366320','',1); select @userid := LAST_INSERT_ID();"
rs = engine.execute(sql)
print rs.rowcount
print rs.context.cursor.fetchall()
sql="select @userid"
rs = engine.execute(sql)
print rs.rowcount
print rs.fetchall()

'''


'''
print rs.context.statement
#print rs.fetchall()


print '\n--------------------------------'

u = d.userFullData(12)
u['source_ident']={'source_name':'profile','source_id':'12'}
printJsonData(u)

print '\n--------------------------------'

ufs = extractUserDataFields(u)
printJsonData(ufs)

for uf in ufs:
    print '--------------------------------'
    sqlt = userFieldDataToExistsSql(12,2,uf)
    print '~', uf, sqlt[0] , tuple(sqlt[1])
    print sqlt[0] % tuple(sqlt[1])
    print '--------'
    sqlt = userFieldDataToUpdateSql(12,2,6,uf)
    print sqlt[0] % tuple(sqlt[1])
    print '--------'
    sqlt = userFieldDataToInsertSql(12,2,uf)
    print sqlt[0] % tuple(sqlt[1])
'''

trans = DatabaseTrans()
trans.ttcontactTrans()





