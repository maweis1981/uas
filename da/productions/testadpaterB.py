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

import time

def printJsonData(v):
    print json.dumps(v, ensure_ascii=False, indent=4, encoding='utf8')


print '*********************************'
tt_start = time.time()
d = DatabaseWorker()
#v = d.userData(12)
#printJsonData(v)


#print '\n--------------------------------'

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
'''
trans = DatabaseTrans()

t1 = time.time()
trans.ttcontactTrans()
t2 = time.time()

print t1,t2, t2-t1



'''

'''
t_start = time.time()
engine = create_engine('mysql://%s:%s@%s:%s/user_profile_m?charset=utf8'%('root', 'idea', 'localhost', '3306'))
conn = engine.connect()
#'delete from users where user_id = 1'
rs = conn.execute('select * from users limit 0,40000')
conn.connection.connection.commit()
print rs.returns_rows
rs = rs.fetchall()
for row in rs:
    #s = str(row['user_id']) + str(row['phone'])
    s = str(row[0]) + str(row[1])
t_end = time.time()
data = [t_start,t_end,t_end-t_start]
print data
'''


'''
import MySQLdb
t_start = time.time()
conn = MySQLdb.connect(host="localhost",user="root",passwd="idea",
    db="user_profile_m",charset='utf8',cursorclass=MySQLdb.cursors.DictCursor)
cur = conn.cursor()
cur.execute('select * from users limit 0,40000')
print conn.set_sql_mode
conn.commit()
print cur.rowcount
conn.close()
print conn.sqlstate()


rs = cur.fetchall()
#cur.execute('delete from users where user_id = 1')
#print cur.rowcount
#rs = cur.fetchall()
#print rs
for row in rs:
    s = str(row['user_id']) + str(row['phone'])
    #s = str(row[0]) + str(row[1])
t_end = time.time()
data = [t_start,t_end,t_end-t_start]
print data
'''


'''
engine = create_engine('mysql://%s:%s@%s:%s/user_profile_m?charset=utf8'%('root', 'idea', 'localhost', '3306'))
conn = engine.connect()
rs = conn.execute('select * from users limit 0,1; set @id = 12 ;select * from users limit 3,2')
print rs.cursor.description
for i in range(0,3):
    print 'rownumber=%s, returns_rows=%s, rowcount=%s' % (rs.cursor.rownumber , rs.returns_rows, rs.cursor.rowcount)
    print 'next',rs.cursor.nextset()

'''

'''
rs = d.dbConns.execute('select * from users limit 0,1; set @id = 12 ;select * from users limit 3,2')
for i in range(0,4):
    print 'rownumber=%s, returns_rows=%s, rowcount=%s' % (rs.cursor.rownumber , rs.returns_rows, rs.cursor.rowcount)
    print 'next',rs.cursor.nextset()
'''

'''
print '\n--------------------------------'

for i in range(23,1000):
    #u = d.userData(i)
    u = d.userFullData(i)
    #printJsonData(u)
print '\n--------------------------------'
print [tt_start,time.time(),time.time()-tt_start]
tt_start = time.time()
'''

sql = ' select @uid := %s; \
select * from users where user_id= @uid; \
select *, u.info_id as data_id from userinfo u inner join userinfo_basic d on u.info_id=d.info_id where user_id= @uid and (selected=1) and (under=0) limit 1; \
select *, u.info_id as data_id from userinfo u inner join userinfo_name d on u.info_id=d.info_id where user_id= @uid and (selected=1) and (under=0) limit 1; \
select *, u.info_id as data_id from userinfo u inner join userinfo_nick d on u.info_id=d.info_id where user_id= @uid and (selected=1) and (under=0) limit 1; \
select *, u.info_id as data_id from userinfo u inner join userinfo_emails d on u.info_id=d.info_id where user_id= @uid and (selected=1) and (under=0) order by row_ord; \
select *, u.info_id as data_id from userinfo u inner join userinfo_telephones d on u.info_id=d.info_id where user_id= @uid and (selected=1) and (under=0) order by row_ord; \
select *, u.info_id as data_id from userinfo u inner join userinfo_im d on u.info_id=d.info_id where user_id= @uid and (selected=1) and (under=0) ; \
select *, u.info_id as data_id from userinfo u inner join userinfo_url d on u.info_id=d.info_id where user_id= @uid and (selected=1) and (under=0) ; \
select *, u.info_id as data_id from userinfo u inner join userinfo_photos d on u.info_id=d.info_id where user_id= @uid and (selected=1) and (under=0) order by row_ord; \
select *, u.info_id as data_id from userinfo u inner join userinfo_addresses d on u.info_id=d.info_id where user_id= @uid and (selected=1) and (under=0) order by row_ord; \
select *, u.info_id as data_id from userinfo u inner join userinfo_organizations d on u.info_id=d.info_id where user_id= @uid and (selected=1) and (under=0) order by row_ord; \
select *, u.info_id as data_id from userinfo u inner join userinfo_educations d on u.info_id=d.info_id where user_id= @uid and (selected=1) and (under=0) order by row_ord; \
select *, u.info_id as data_id from userinfo u inner join userinfo_sounds d on u.info_id=d.info_id where user_id= @uid and (selected=1) and (under=0) order by row_ord; \
select *, u.info_id as data_id from userinfo u inner join userinfo_geoes d on u.info_id=d.info_id where user_id= @uid and (selected=1) and (under=0) order by row_ord; \
select *, userinfo.info_id as infoid from userinfo inner join userinfo_data on userinfo.info_id=userinfo_data.info_id where user_id= @uid and (selected=1) and (under=0) order by user_id, data_class, row_ord, userinfo.info_id; \
select *, apps.app_id as appid from user_account inner join apps on user_account.app_id = apps.app_id where user_id= @uid ; \
select *, userinfo.info_id as infoid from userinfo inner join userinfo_data on userinfo.info_id=userinfo_data.info_id where (user_id= @uid) and (selected=1) and (under=1) and (not isnull(app_id)) order by app_id, user_id, data_class, row_ord, userinfo.info_id; \
'


for i in range(23,1000):
    #print sql % (i)
    rs = d.dbConns.execute(sql % (i))
    for j in range(0,18):
        if rs.cursor.rowcount > 0:
            rs.cursor.fetchall()
        #for row in rs:
        #    print row[0]
        #print 'rownumber=%s, returns_rows=%s, rowcount=%s' % (rs.cursor.rownumber , rs.returns_rows, rs.cursor.rowcount)
        #print 'next',
        rs.context.cursor.nextset()
'''    
'''

print [tt_start,time.time(),time.time()-tt_start]
