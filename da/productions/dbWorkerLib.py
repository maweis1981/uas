#!/usr/bin/env python
# encoding: utf-8
"""
dbworkerlib.py
"""

import sys
import os
import copy
import json

from types import *
from datetime import *
import time
import uuid

def printJsonData(v):
    print json.dumps(v, ensure_ascii=False, indent=4, encoding='utf8')

#### consts

userFieldDefine = { 
'_sys':{
'fields':['basic','nick'],
'class-mutiline':['telephones','emails','addresses','organizations','photos','sounds','educations','geoes'],
'class-oneline':['name','ident','account'],
'class-list':['im','url'],
'mutiline-key':{
    'telephones':'tel_number',
    'emails':'email',
    'photos':'photo_url',
    'sounds':'sound_url',
    'im':'im_name',
    'url':'url_name',
    'educations':'',
    'addresses':'',
    'organizations':'',
    'account':'',
    'geoes':''
    },
'userinfo':['versign','last_update','source_name','source_id','order','serial','row_serial'],
'readonly':['versign_phone','guid','versign_email','user_id','source_ident', 'application_account'],
'realname':{
    'order':'row_serial',
    'source_name':'origin',
    'source_id':'origin_id'
    }
},

'basic':['birthday','gender','blood','marry'],
'nick':['nick','avatar','sign'],

'name':['FN','family_name','given_name','additional_names','name_prefix','name_suffix'],
'ident':['idcard','key'],

'telephones':['tel_type','tel_number'],
'emails':['email_type','email'],
'addresses':['address_type','post_office_address','extended_address','street','locality','region','postal_code','country'],
'geoes':['geo_type','record_date','tz','geo_lat','geo_lng'],
'organizations':['org_name','org_unit','org_subunit','title','role','work_field','org_logo','org_into_date','org_leave_date'],
'photos':['photo_class','photo_caption','photo_url'],
'educations':['school_name','school_city','education','school_into_date','school_leave_date'],
'sounds':['sound_class','sound_caption','sound_url'],
'account':['user_id','app_id','app_account','app_nick','app_sign','app_avatar','app_last_status','app_last_date'],

'im':['im_name','im'],
'url':['url_name','url']
}


userFieldNotEmpty = [key for key in userFieldDefine['_sys']['class-mutiline'] if userFieldDefine['_sys']['mutiline-key'].get(key,'')!='' ]

def fieldEncode(field):
    tp = type(field)
    if tp is NoneType :
        return ''
    elif (tp is str) or (tp is unicode) :
        return field.encode('utf8')
    elif (tp is date) or (tp is datetime) :
        return str(field)
    else :
        return field
 
def trim(s):
    if s == None:
        return s
    elif type(s) in [str,unicode]:
        return s.lstrip()
    else:
        return str(s)

def trimEmpty(s):
    if s == None:
        return ''
    elif type(s) in [str,unicode]:
        return s.lstrip()
    else:
        return str(s)

def userDataToSql(userData, user_id, app_id):
    d = extractUserData(userData, userDataFields['basic'])
    sql = userFieldDataToSql(d, 'basic', appid)

def extractUserDataFields(userData):
    ud = userData
    if ud==None:
        return None

    r  = []
    ufs = userFieldDefine['_sys']
    sourceIdent = {}
    if 'source_ident' in userData and type(userData['source_ident']) is dict:
        sourceIdent = userData['source_ident']
        
    udfs = {}
    udls = {}
    for k,v in ud.iteritems():
        if type(v) in (list,dict):
            udls[k]=v
        else:
            udfs[k]=v
    for f in ufs['fields']:
        rd = extractUserFieldData(dict(sourceIdent.items()+udfs.items()),userFieldDefine[f],f)
        if len(rd['data'])>0: 
            r.append(rd)
    for f,uf in udls.iteritems():
        if f in ufs['class-mutiline']:
            kn = ufs['mutiline-key'][f]
            #print 'kn:',kn,'f',f
            if type(uf) is list: # 代表多行数据
                i=0
                for uitem in uf:
                    i = i + 1
                    uitem['row_serial']=uitem.get('serial',uitem.get('row_serial',i))
                    if kn!='' and uitem.get(kn,None) in [None,'',u'']: # 应该有关键数据，没有则忽略
                        pass
                    else:
                        r.append(extractUserFieldData(uitem,userFieldDefine[f],f))
            elif type(uf) is dict: # 代表此应用此数据只有一条
                if kn!='' and uf.get(kn,None) in [None,'']:
                    pass
                else:
                    r.append(extractUserFieldData(dict(sourceIdent.items()+uf.items()),userFieldDefine[f],f))
        elif f in ufs['class-oneline']: # 肯定只有一条
            r.append(extractUserFieldData(dict(sourceIdent.items()+uf.items()),userFieldDefine[f],f))
        elif f in ufs['class-list']:
            kn = ufs['mutiline-key'][f]
            kf = userFieldDefine[f][1]
            for k,v in uf.iteritems():
                if v != None:
                    ul={kn:k,kf:v}
                    r.append(extractUserFieldData(dict(sourceIdent.items()+ul.items()),[kn,kf],f))
        else:
            if f in ufs['readonly']:
                pass
            elif type(uf) is dict:
                r.append(extractUserFieldData(dict(sourceIdent.items()+uf.items()),['*'],f))
            elif type(uf) is list:
                for uitem in uf:
                    r.append(extractUserFieldData(uitem,['*'],f))
            elif type(uf) in (str,unicode,int,long):
                r.append(extractUserFieldData(dict(sourceIdent.items()+{f:uf}.items()),['*'],''))
    return r



def extractUserFieldData(userDataField, fieldList, fieldClass):
    d = {'data':{},'info':{},'class':''}
    u = userDataField;
    if u==None:
        return d

    realname = userFieldDefine['_sys']['realname']
    if 'data_id' in u:
        d['data_id'] = u['data_id']

    for k in u:
        if k in userFieldDefine['_sys']['userinfo']:
            d['info'][realname.get(k,k)] = u[k]
        elif '*' in fieldList:
            d['data'][k] = u[k]
        elif k in fieldList:
            d['data'][realname.get(k,k)] = u[k]
    d['class']=fieldClass
    return d
    

def userFieldDataToExistsSql(user_id, app_id, userFieldData):
    sql = ''
    param = []
    if userFieldData==None:
        return ('',[])

    ufs = userFieldDefine['_sys']
    ud  = userFieldData['data']
    ui  = userFieldData['info']
    fieldClass = userFieldData['class']
    if 'data_id' in userFieldData: # 已经指定特定数据记录 /同时校验用户和应用的归属的合法性
        sql = "select info_id from userinfo where user_id=%s  and app_id=%s and info_id=%s "
        param = [user_id, app_id, userFieldData['data_id']]
        return (sql,param)
    if fieldClass in userFieldDefine:
        sqlpf = "select u.info_id from userinfo u inner join userinfo_"+fieldClass+" d on u.info_id=d.info_id where u.user_id=%s and u.app_id=%s "
        if 'origin_id' in ui: # 指定和外部数据相匹配的记录/同时校验用户，应用，数据归类，
            sql = sqlpf + " and origin=%s and origin_id=%s "
            param = [user_id, app_id, ui.get('origin',''),ui['origin_id']]
            return (sql,param)
        else: # 按照规则以字段逻辑的唯一性要求尝试匹配
            if (fieldClass in (ufs['fields']+ufs['class-oneline'])) or (
                fieldClass in ufs['class-mutiline'] and 'row_serial' not in ui ): ## 单一记录的，查询之 userid/appid/class/one
                sql = sqlpf + " "
                param = [user_id, app_id]
                return (sql,param)
                #print '****', sql
            elif fieldClass in (ufs['class-mutiline']+ufs['class-list']): #多行情况，再附加检查关键字段，
                k = ufs['mutiline-key'][fieldClass]
                if 'serial' in ui or 'row_serial' in ui: #多行，且没有可用以区别的关键字段，附加检验系列号
                    sql = sqlpf + " and u.row_serial = %s "
                    param = [user_id, app_id, ui['serial']]
                elif (k!='') and (k in ud):
                    sql = sqlpf + " and "+k+"=%s "
                    param = [user_id, app_id, ud[k]]
                    return (sql,param)
                else: #这种情况不允许发生，只能认为是一新行，无法认为是新增还是更新，哪些字段匹配
                    #sql = " and ".join(str(f)+"<=>%s" for f in userFieldDefine[fieldClass])
                    #sql = sqlpf + " and " + sql +''
                    #param = [user_id, app_id] + [ud.get(f,None) for f in userFieldDefine[fieldClass]]
                    sql='select info_id from userinfo where 0'
                    return (sql,[])
    else:  # userinfo_data data
        sqlpf = "select u.info_id from userinfo u inner join userinfo_data d on u.info_id=d.info_id where user_id=%s and app_id=%s and data_class=%s "
        param = [user_id, app_id, fieldClass]
        if 'origin_id' in ui: # 指定和外部数据相匹配的记录/同时校验用户，应用，数据归类，
            sql =  sqlpf + " and origin=%s and origin_id=%s ;"
            param = param + [ui.get('origin',''),ui['origin_id']]
            return (sql,param)
        else: 
            if (fieldClass!=''):
                return (sqlpf+" limit 1 ;", param)
            else:
                if len(ud)==1: 
                    sql   = sqlpf + " and "+ud.keys()[0]+"=%s ;"
                    param = param + [ud.values()[0]]
                    return (sql, param)


    return (sql,param)


# 更新必须找到 info_id, 
def userFieldDataToUpdateSql(user_id, app_id, data_id, userFieldData):
    sqld = ''
    sqli = ''
    parami = []
    paramd = []
    if userFieldData==None:
        return ('',[])
    ufs = userFieldDefine['_sys']
    ud  = userFieldData['data']
    ui  = userFieldData['info']
    fieldClass = userFieldData['class']
    # 有字段定义的
    if 'serial' in ui:
        del ui['serial']
    if len(ui) >0:
        #print ui
        uisql = ', '.join(f+"=%s" for f in ui.keys())
        parami = ui.values()
        if 'last_update' in ui:
            sqli = "update userinfo set " + uisql
        else:
            sqli = "update userinfo set last_update=now(), " + uisql
    else:
        sqli = "update userinfo set last_update=now() "
        
    sqli = sqli + " where info_id=%s and user_id=%s and app_id=%s ; set @cnt=row_count();"
    parami = parami + [data_id, user_id, app_id]
    if fieldClass in (ufs['fields']+ufs['class-oneline']+ufs['class-mutiline']+ufs['class-list']):
        if len(ud) >0:
            sqld = "update userinfo_"+fieldClass+" set "
            sqld = sqld + ','.join(f+"=%s" for f in ud.keys())
            paramd = ud.values() 
            sqld = sqld + " where info_id=%s and @cnt=1; commit;"  # 再次保证记录的有效性
            paramd = paramd + [data_id]
    # 无字段定义的
    else :
        sqld = "replace userinfo_data (info_id,data_class,data_field,data_value) values "
        sqld+= ",".join( "(%s,'%s','%s','%s')" % (data_id,fieldClass,sqlstr(k),sqlstr(v)) for k,v in ud.iteritems() ) + "; commit;" 
    return (sqli+sqld, parami+paramd)
    

def userFieldDataToInsertSql(user_id, app_id, userFieldData):
    sqld = ''
    sqli = ''
    parami = []
    paramd = []
    if userFieldData==None:
        return ('',[])
    ufs = userFieldDefine['_sys']
    ud  = userFieldData['data']
    ui  = userFieldData['info']
    fieldClass = userFieldData['class']
    if 'serial' in ui:
        del ui['serial']

    #if len(ui)>0:
    #print ui
    sqli = "insert into userinfo (" +", ".join(f for f in ['user_id', 'app_id']+ ui.keys()) +") values (" \
        + ", ".join('%s' for f in ['','']+ui.keys())+"); set @cnt=row_count();  set @dataid = LAST_INSERT_ID(); "
    parami = [user_id, app_id]+ui.values()
    if fieldClass in (ufs['fields']+ufs['class-oneline']+ufs['class-mutiline']+ufs['class-list']):
        if len(ud) >0:
            sqld = "insert userinfo_"+fieldClass+" (info_id, "+', '.join(f for f in ud.keys()) \
                +") select * from (select @dataid, "+', '.join('%s as '+f for f in ud)+") d where @cnt=1; commit;"
            paramd = ud.values()
    else:
        sqld = "insert userinfo_data (info_id,data_class,data_field,data_value) values "
        sqld+= ",".join( "(@dataid,'%s','%s','%s')" % (fieldClass,sqlstr(k),sqlstr(v)) for k,v in ud.iteritems() ) + "; commit;" 
    return (sqli+sqld, parami+paramd)

'''
# 清理数据结构对象，把内容为空的删除掉
'''
def TrimEmptyDataField2(d,emptys=[None,'',u'']):
    if type(d) is dict:
        for (f,v) in d.items():
            if v in emptys:
                del d[f]
            elif type(v) in [list,dict]:
                print v
                if type(v) is dict:
                    mlist = [mitem for mitem in v.items() if mitem[0][0]=='@']
                    print mlist
                    for mitem in mlist:
                        del v[mitem[0]]
                TrimEmptyDataField(v)
                if type(v) is dict and len(v)==1 and f in userFieldNotEmpty:
                    if v.keys[0] != userFieldDefine['_sys']['mutiline-key'][f]:
                        del d[f] 
                if len(v)==0:
                    del d[f]
                elif type(v) is dict and len(mlist)>0:
                    for mitem in mlist:
                        key = mitem[0][1:33]
                        v[key]=mitem[1]
            elif type(v) not in [str,unicode]:
                d[f] = str(v)
    elif type(d) is list:
        for i in range(len(d)-1, -1, -1):
            v=d[i]
            if type(v) in [list,dict]:
                TrimEmptyDataField(v)
                if len(v)==0:
                    del d[i]
    return

def TrimEmptyDataField(d,emptys=[None,'',u'']):
    def TrimDict(k,td):
        mlist = [mitem for mitem in td.items() if (type(mitem[0]) is str and mitem[0][0]=='@') or (k!="source_ident" and mitem[0] in userFieldDefine['_sys']['userinfo'] and mitem[1] not in emptys)]
        for mitem in mlist:
            del td[mitem[0]]
        for (key,v) in td.items():
            if v in emptys:
                del td[key]
            elif type(v) in [list,dict]:
                TrimMain(key,v)
                if len(v)==0:
                    del td[key]
        if k in userFieldNotEmpty and userFieldDefine['_sys']['mutiline-key'][k] not in td.keys():
            td.clear()
        if len(td)>0:
            for mitem in mlist:
                td[mitem[0].replace('@','',1)]=mitem[1]

    def TrimMain(k,v):
        if type(v) is dict:
            TrimDict(k,v)
        elif type(v) is list:
            for i in range(len(v)-1,-1,-1):
                d = v[i]
                if type(d) in [list,dict]:
                    TrimMain(k,d)
                    if len(d) == 0:
                        del v[i]
    TrimMain(None,d)


# todo : delete invalid data
def TrimInvalidData(data):
    pass

def guidctoa(guid):
    #8bfe7d904b5711e1a05ff04da2086e9d
    #8BFE7D90-4B57-11E1-A05F-F04DA2086E9D
    if type(guid) in [str,unicode] and len(guid)==32:
        g = guid.upper()
        g = '-'.join([g[0:8],g[8:12],g[12:16],g[16:20],g[20:32]])
        return g
    else:
        return guid
    
genGUID = lambda : uuid.uuid4().hex

def guidHex(guidStr):
    r = ''.join( c for c in guidStr if c in 'ABCDEFabcdef0123456789')
    if len(r)==32:
        return r
    else:
        return None
    
def guidLong(guidStr):
    s = guidHex(guidStr)
    if s != None:
        return long(s,16)
    
def secondToTimestamp(seconds):
    if seconds==0:
        return ''
    else:
        return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(seconds))
     
def sqlstr(s):
    if type(s) in [str,unicode]:
        return _sqlstr(s)
    else:
        return s

_sqlstr = lambda s : s.replace("'","''").replace("%","%%")


listIndexOf = lambda list,index : dict((i,list[i]) for i in range(0,len(list))).get(index,None)


def birthday(y,m,d):
    try:
        return date(y,m,d).isoformat()
    except:
        return None
    
# def iif(ex, valueTrue, valueFalse):
#     if ex:
#        return valueType
#     else:
#        return valueFalse
  
iif = lambda ex, valueTrue, valueFalse : [valueFalse,valueTrue][int(bool(ex))]

isEmpty = lambda v : v in ['',u'',None] 
