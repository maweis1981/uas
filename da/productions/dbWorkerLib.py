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

from sqlalchemy import *


def printJsonData(v):
    print json.dumps(v, ensure_ascii=False, indent=4, encoding='utf8')

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
    if type(s) in [str,unicode]:
        return s.lstrip()
    else:
        return s

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
'userinfo':['versign','last_update','source_name','source_id','order','data_class','serial'],
'readonly':['versign_phone','guid','versign_email','user_id','source_ident'],
'realname':{
    'order':'row_ord',
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
'account':['user_id','app_id','app_account','app_nick','app_avatar','app_last_status','app_last_date'],

'im':['im_name','im'],
'url':['url_name','url']
}


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
    if 'source_ident' in userData:
        if (type(userData['source_ident']) is dict) and ('source_id' in userData['source_ident']):
            sourceIdent = userData['source_ident']
        
    udfs = {}
    udls = {}
    for k,v in ud.iteritems():
        if type(v) in (list,dict):
            udls[k]=v
        else:
            udfs[k]=v
    for f in ufs['fields']:
        rd = extractUserFieldData(dict(udfs.items()+sourceIdent.items()),userFieldDefine[f],f)
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
                    uitem['row_ord']=uitem.get('serial',uitem.get('row_ord',i))
                    if kn!='' and uitem.get(kn,None) in [None,'',u'']: # 应该有关键数据，没有则忽略
                        pass
                    else:
                        r.append(extractUserFieldData(uitem,userFieldDefine[f],f))
            elif type(uf) is dict: # 代表此应用此数据只有一条
                if kn!='' and uf.get(kn,None) in [None,'']:
                    pass
                else:
                    r.append(extractUserFieldData(dict(uf.items()+sourceIdent.items()),userFieldDefine[f],f))
        elif f in ufs['class-oneline']: # 肯定只有一条
            r.append(extractUserFieldData(dict(uf.items()+sourceIdent.items()),userFieldDefine[f],f))
        elif f in ufs['class-list']:
            kn = ufs['mutiline-key'][f]
            kf = userFieldDefine[f][1]
            for k,v in uf.iteritems():
                if v != None:
                    ul={kn:k,kf:v}
                    r.append(extractUserFieldData(dict(ul.items()+sourceIdent.items()),[kn,kf],f))
        else:
            if f in ufs['readonly']:
                pass
            elif type(uf) is dict:
                r.append(extractUserFieldData(dict(uf.items()+sourceIdent.items()),['*'],f))
            elif type(uf) is list:
                for uitem in uf:
                    r.append(extractUserFieldData(uitem,['*'],f))
            elif type(uf) in (str,unicode,int,long):
                r.append(extractUserFieldData(dict({f:uf}.items()+sourceIdent.items()),['*'],''))
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
        if '*' in fieldList:
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
        sql = "select info_id from userinfo where user_id=%s  and app_id=%s and info_id=%s ;"
        param = [user_id, app_id, userFieldData['data_id']]
        return (sql,param)
    if fieldClass in userFieldDefine:
        sqlpf = "select u.info_id from userinfo u inner join userinfo_"+fieldClass+" d on u.info_id=d.info_id where u.user_id=%s and u.app_id=%s "
        if 'origin_id' in ui: # 指定和外部数据相匹配的记录/同时校验用户，应用，数据归类，
            sql = sqlpf + " and origin=%s and origin_id=%s ;"
            param = [user_id, app_id, ui['origin'],ui['origin_id']]
            return (sql,param)
        else: # 按照规则以字段逻辑的唯一性要求尝试匹配
            if (fieldClass in (ufs['fields']+ufs['class-oneline'])) or (
                fieldClass in ufs['class-mutiline'] and 'row_ord' not in ui ): ## 单一记录的，查询之 userid/appid/class/one
                sql = sqlpf + " ;"
                param = [user_id, app_id]
                return (sql,param)
                print '****', sql
            elif fieldClass in (ufs['class-mutiline']+ufs['class-list']): #多行情况，再附加检查关键字段，
                k = ufs['mutiline-key'][fieldClass]
                if 'serial' in ud: #多行，且没有可用以区别的关键字段，附加检验系列号
                    sql = sqlpf + " and u.row_ord = %s ;"
                    param = [user_id, app_id, ud['serial']]
                elif (k!='') and (k in ud):
                    sql = sqlpf + " and "+k+"=%s ;"
                    param = [user_id, app_id, ud[k]]
                    return (sql,param)
                else: #这种情况会速度很慢，导入因尽一切可能避免
                    sql = " and ".join(str(f)+"<=>%s" for f in userFieldDefine[fieldClass])
                    sql = sqlpf + " and " + sql +';'
                    param = [user_id, app_id] + [ud.get(f,None) for f in userFieldDefine[fieldClass]] 
                    return (sql,param)
    else:  # userinfo_data data
        sqlpf = "select u.info_id from userinfo u inner join userinfo_data d on u.info_id=d.info_id where user_id=%s and app_id=%s and data_class=%s "
        param = [user_id, app_id, fieldClass]
        if 'origin_id' in ui: # 指定和外部数据相匹配的记录/同时校验用户，应用，数据归类，
            sql =  sqlpf + " and origin=%s and origin_id=%s ;"
            param = param + [ui['origin'],ui['origin_id']]
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
    sqli = "update userinfo set last_update=now() "
    if 'serial' in ui:
        del ui['serial']
    if len(ui) >0:
        sqli = sqli +', '+ ', '.join(f+"=%s" for f in ui.keys())
        parami = ui.values()
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
        for f in ud:
            sqld=sqld+ "replace userinfo_data values (%s,%s,%s) where @cnt=1; commit; "
            paramd = paramd + [data_id, f, ud[f]]
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
    sqli = "insert into userinfo (" +", ".join(f for f in ['user_id', 'app_id']+ ui.keys()) +") values (" \
        + ", ".join('%s' for f in ['','']+ui.keys())+"); set @cnt=row_count();  set @dataid = LAST_INSERT_ID(); "
    parami = [user_id, app_id]+ui.values()
    if fieldClass in (ufs['fields']+ufs['class-oneline']+ufs['class-mutiline']+ufs['class-list']):
        if len(ud) >0:
            sqld = "insert userinfo_"+fieldClass+" (info_id, "+', '.join(f for f in ud.keys()) \
                +") select * from (select @dataid, "+', '.join('%s as '+f for f in ud)+") d where @cnt=1; commit;"
            paramd = ud.values()
    else:
        for f in ud:
            sqld=sqld+ "replace userinfo_data select * from (select @dataid,%s,%s) d where @cnt=1; commit;"
            paramd = paramd + [f, ud[f]]
    return (sqli+sqld, parami+paramd)

'''
# 清理数据结构对象，把内容为空的删除掉
'''
def TrimEmptyDataField(d,emptys=[None,'',u'']):
    if type(d) is dict:
        for (f,v) in d.items():
            if v in emptys:
                del d[f]
            elif type(v) in [list,dict]:
                TrimEmptyDataField(v)
                if len(v)==0:
                    del d[f]
    elif type(d) is list:
        for i in range(0,len(d)):
            v=d[i]
            if type(v) in [list,dict]:
                TrimEmptyDataField(v)
                if len(v)==0:
                    del d[i]
    return
     

def guidctoa(guid):
    #8bfe7d904b5711e1a05ff04da2086e9d
    #8BFE7D90-4B57-11E1-A05F-F04DA2086E9D
    if len(guid)==32:
        g = guid.upper()
        g = '-'.join([g[0:8],g[8:12],g[12:16],g[16:20],g[20:32]])
        return g
    else:
        return guid
     
# todo : delete invalid data
def TrimInvalidData(data):
    pass