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
engine = create_engine('mysql://%s:%s@%s:%s/user_profile_m?charset=utf8'%(MYSQLUSER, MYSQLPWD, MYSQLADDR, MYSQLPORT), pool_size=10)
conn   = engine.connect()
sql="select * from users where user_id = %s;"
rs = conn.execute(sql,12)
rs.close()
engine.raw_connection()
print 'pool',engine.pool.size()
#engine.dispose()
conn.close()
print conn.closed

'''
'''
x = 10
for j  in range(0,10):
    engine.dispose()
    ls= []
    for i in range(0,x):
        print i
        ls.append(engine.connect())
    rsls = []
    print
    for i in range(0,x):
        print i ,'\t',
        rsls.append(ls[i].execute(sql,100+i))
        print rsls[i].fetchone()['phone']
    for i in range(0,x):
        rsls[i].close()
        ls[i].close()
engine.dispose()    

'''
'''
print rs.rowcount
print rs.context.cursor.fetchall()
sql="select @userid"
rs = engine.execute(sql)
print rs.rowcount
print rs.fetchall()


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

u = d.userFullData(12)
printJsonData(u)

'''
import time

trans = DatabaseTrans()

t1 = time.time()
trans.ttcontactTrans()
t2 = time.time()

print t1,t2, t2-t1


'''
'''


