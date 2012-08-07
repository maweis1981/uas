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

import MySQLdb

tt_start = time.time()
engine = create_engine('mysql://%s:%s@%s:%s/user_profile_m?charset=utf8'%('root', 'idea', '192.168.91.48', '3306'))
conn = engine.connect()

s = [
"select * from users limit 10"
]
for sql in s:
    cur = conn.connection.connection.cursor(MySQLdb.cursors.SSCursor)
    print '--', cur.execute(sql)
    print cur.messages
    print cur.fetchone()
    print cur.fetchone()
    print cur.fetchone()
    print '-----'
    for rec in cur:
        print rec
    cur.close()
'''
'''
tt_start = time.time()
engine = create_engine('mysql://%s:%s@%s:%s/user_profile_m?charset=utf8'%('root', 'idea', '192.168.91.48', '3306'))
conn = engine.connect() # commit; select @id := LAST_INSERT_ID();

cnn = conn.connection
cur = cnn.cursor()
cur.execute('select * from users')
print cur.fetchall()
cur.execute("""
    insert into data_dict (data_name) values (111);
    select @a:=1;
    update data_dict set data_name='aaaa' where data_id = 20;
    select * from data_dict limit 2;
    set @dataid = LAST_INSERT_ID();
    commit;
    """)
cur.close()
cur = cnn.cursor()
cur.execute('select * from users tttt ')


for j in range(0,5):
    #rs = conn.execute("select @c:=1; set @a=1; select @b:=2; insert into data_dict (data_name) values (111); commit;")
    #rs = conn.execute("SELECT * FROM  `data_dict` LIMIT 0 , 1")
    rs = conn.execute("""
    select @a:=1;
    update data_dict set data_name='aaaa' where data_id = 20;
    insert into data_dict (data_name) values (111);
    select * from data_dict limit 2;
    set @dataid = LAST_INSERT_ID();
    commit;
    """)
    cursor = rs.context.cursor
    #rs.close()
    for i in range(0,1):
        #cursor = rs.cursor
        print dict(rownumber=cursor.rownumber,
                   lastrowid=rs.lastrowid,
                   returns_rows=rs.returns_rows,
                   #rowcount=cursor.rowcount,
                   #description=cursor.description,
    ##               rslastrowid=rs.lastrowid,
    ##               is_crud  =rs.context.is_crud,
    ##               isddl    =rs.context.isddl,
    ##               isdelete =rs.context.isdelete,
    ##               isupdate =rs.context.isupdate,
    ##               isinsert =rs.context.isinsert,
    ##               lastrow_has_defaults =rs.context.lastrow_has_defaults()
                   #description_flags= cursor.description_flags
                   arraysize=cursor.arraysize
                   )
        #if rs.returns_rows:
        #data = cursor.fetchall()
        #print data
        print 'next',cursor.nextset()
    rs.close()
    conn.execute("select@a:=1; select * from data_dict limit 1;")
'''

'''

#conn.execute('update userinfo_emails set  userinfo_emails.hashs = 0')
tt_start = time.time()
rs = conn.execute("SELECT * FROM  userinfo_emails limit 0,100000")
data = rs.cursor.fetchall()

tt_start = time.time()
for i in range(0,len(data)):
    h = hash(data[i][2])
    conn.execute("update userinfo_emails set hashs=%s where info_id=%s",h,data[i][0])
print [tt_start,time.time(),time.time()-tt_start]

#conn.execute('update userinfo_emails set  userinfo_emails.hashs = 0')
tt_start = time.time()
v = ', '.join( '(%s, %s)' % (f[0],hash(f[2])) for f in data)
#print v
sql = "select @a=1; CREATE TEMPORARY TABLE tmp(id BIGINT,n INT,KEY id( id )); \
INSERT INTO tmp VALUES %s ;\
UPDATE userinfo_emails u,tmp SET u.hashs = tmp.n WHERE u.info_id = tmp.id; \
commit;" % v
#print sql
rs = conn.execute(sql)
for i in range(0,5):
    rs.context.cursor.nextset()
    print rs.context.cursor.description
print [tt_start,time.time(),time.time()-tt_start]


'''

'''
rs = d.dbConns.execute('SELECT hex(uid) FROM  user_ident')
uid = rs.fetchone()[0]
print type(uid), uid,
d.dbConns.execute('UPDATE user_ident SET uid = 0x123456789ABCDEF0123456789ABCDEF2 where uid =unhex(%s)',long(uid,16))

print hex(long(uid,16))

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

'''
for i in range(23,24):
    #print sql % (i)
    rs = d.dbConns.execute(sql % (i))
    for j in range(0,18):
        #print rs.cursor.description
        if rs.cursor.rowcount > 0:
            rs.cursor.fetchall()
        #for row in rs:
        #    print row[0]
        #print 'rownumber=%s, returns_rows=%s, rowcount=%s' % (rs.cursor.rownumber , rs.returns_rows, rs.cursor.rowcount)
        #print 'next',
        rs.context.cursor.nextset()

'''

'''
def t1():
    print 't1'
    return {1:2}

class foo(object):
    f = t1()
    def t2(self):
        print self.f

ff = foo()
f2 = foo()
print ff.f
print f2.f
f2.f[1]=3
print ff.f
print f2.f
print f2.t2()
'''

'''
import redis


tt_start = time.time()
for i in range(0,10):
    d.userFullData(12)
    d.userFullData(15)
    d.userFullData(16)
print [tt_start,time.time(),time.time()-tt_start]

import dbRedis
rd = dbRedis.dbRedis('192.168.91.48')
rd.UserFull.set(12,d.userFullData(12))
rd.UserFull.set(16,d.userFullData(15))
rd.UserFull.set(16,d.userFullData(16))
printJsonData(d.userFullData(24))
rd.UserFull.set(24,d.userFullData(24))

printJsonData((rd.UserFull.get(12)))

tt_start = time.time()
for i in range(0,10):
    (rd.UserFull.get(12))
    (rd.UserFull.get(15))
    (rd.UserFull.get(16))

print [tt_start,time.time(),time.time()-tt_start]
'''


