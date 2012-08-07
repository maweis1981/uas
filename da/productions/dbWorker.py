#!/usr/bin/env python
# encoding: utf-8
"""
dbworker.py
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
from dbConnections import *

'''
数据库及数据结构中关于NULL值的说明和约定

关键字段 必须有值
一般字段 值分两义 1、有值   2、无值 -> null
改写时候 值为null,'',... 均属于明确值，不给出的取默认
null值在输出时字段会被清除，有值的才会被输出，空串为有值，会被输出
'''

strip_mode_no = -1
strip_mode_null = 0
strip_mode_nullandempty = 1
strip_mode_invalid = 2

contact_style_phone_1_1 = 1
contact_style_phone_1_n = 2
contact_style_email_1_1 = 3
contact_style_email_1_n = 4
contact_style_ident_1_1 = 5
contact_style_ident_1_n = 6
contact_style_user_id_1_1 = 7
contact_style_user_id_1_n = 8
contact_style_mix   = 9

class DatabaseWorker(object):

    dbConns = None
    apiStructs = {}

    def __init__(self, dbConns=None):
        if dbConns == None:
            dbConns = DatabaseConnections()
        self.dbConns = dbConns
        self.apiStructsFromDB()
    
    def create_table(self):
        pass
    
    def generate_data(self):
        pass

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
        #print 'userData'

        #debug = True
     
        ## 1 cache 2 db //todo cache /base

        ## for user data
        ## user basic data
        user_data = {}
        userid = long(userid)

        sql = 'select * from users where user_id= %s'
        #if debug : print sql
        
        rs = self.dbConns.execute(sql,userid)
        if rs.rowcount==1:
            row = rs.fetchone()
            user_data['user_id'] = fieldEncode(row['user_id'])
            user_data['guid']    = fieldEncode(row['guid'])
            user_data['versign_phone'] = fieldEncode(row['phone'])
            user_data['versign_email'] = fieldEncode(row['email'])
            rs.close()
        else:
            return None
         

        sqlprf = 'select *, u.info_id as data_id from userinfo u inner join userinfo_%s d on u.info_id=d.info_id \
where user_id= %u and (selected=1) and (under=0) %s' % ('%s', userid, '%s')
        #print sqlprf

        sql = sqlprf % ('basic', 'limit 1')
        rs = self.dbConns.execute(sql)
        for row in rs:
            user_data['birthday'] = fieldEncode(row['birthday'])
            user_data['gender']= fieldEncode(row['gender'])
            user_data['blood'] = fieldEncode(row['blood'])
            user_data['marry'] = fieldEncode(row['marry'])

        ## user name data
        sql = sqlprf % ('name', 'limit 1')
        rs = self.dbConns.execute(sql)
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
        rs = self.dbConns.execute(sql)
        for row in rs:
            user_data['nick']  = fieldEncode(row['nick'])
            user_data['avatar']= fieldEncode(row['avatar'])
            user_data['sign']  = fieldEncode(row['sign'])

        ## user email data / mutiline
        sql = sqlprf % ('emails', 'order by row_serial')
        rs = self.dbConns.execute(sql)
        rows = []
        for row in rs:
            row_data = {}
            rows.append(row_data)
            row_data['row_serial'] = fieldEncode(row['row_serial'])
            row_data['email_type'] = fieldEncode(row['email_type'])
            row_data['email']  = fieldEncode(row['email'])
            row_data['versign']  = fieldEncode(row['versign'])
        if len(rows)>0 : user_data['emails'] = rows

        ## user tel data / mutiline
        sql = sqlprf % ('telephones', 'order by row_serial')
        rs = self.dbConns.execute(sql)
        rows = []
        for row in rs:
            row_data = {}
            rows.append(row_data)
            row_data['row_serial'] = fieldEncode(row['row_serial'])
            row_data['tel_type'] = fieldEncode(row['tel_type'])
            row_data['tel_number']  = fieldEncode(row['tel_number'])
            row_data['versign']  = fieldEncode(row['versign'])
            #row_data['tel_city'] = fieldEncode(row['tel_city'])
            #row_data['tel_region']  = fieldEncode(row['tel_region'])
        if len(rows)>0 : user_data['telephones'] = rows

        ## user im list data / muti property / dict 
        sql = sqlprf % ('im', '')
        rs = self.dbConns.execute(sql)
        row_data = {}
        for row in rs:
            row_data[fieldEncode(row['im_name'])] = fieldEncode(row['im'])
        if len(row_data)>0 : user_data['im'] = row_data

        ## user url list data / muti property / dict
        sql = sqlprf % ('url', '')
        rs = self.dbConns.execute(sql)
        row_data = {}
        for row in rs:
            row_data[fieldEncode(row['url_name'])] = fieldEncode(row['url'])
        if len(row_data)>0 : user_data['url'] = row_data

        ## user photos data / mutiline
        sql = sqlprf % ('photos', 'order by row_serial')
        rs = self.dbConns.execute(sql)
        rows = []
        for row in rs:
            row_data = {}
            rows.append(row_data)
            row_data['row_serial'] = fieldEncode(row['row_serial'])
            row_data['photo_class'] = fieldEncode(row['photo_class'])
            row_data['photo_caption']  = fieldEncode(row['photo_caption'])
            row_data['photo_url']  = fieldEncode(row['photo_url'])
        if len(rows)>0 : user_data['photos'] = rows

        ## user adrress data / mutiline
        sql = sqlprf % ('addresses', 'order by row_serial')
        rs = self.dbConns.execute(sql)
        rows = []
        for row in rs:
            row_data = {}
            rows.append(row_data)
            row_data['row_serial'] = fieldEncode(row['row_serial'])
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
        sql = sqlprf % ('organizations', 'order by row_serial')
        rs = self.dbConns.execute(sql)
        rows = []
        for row in rs:
            row_data = {}
            rows.append(row_data)
            row_data['row_serial'] = fieldEncode(row['row_serial'])
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
        sql = sqlprf % ('educations', 'order by row_serial')
        rs = self.dbConns.execute(sql)
        rows = []
        for row in rs:
            row_data = {}
            rows.append(row_data)
            row_data['row_serial'] = fieldEncode(row['row_serial'])
            row_data['education']  = fieldEncode(row['education'])
            row_data['school_name'] = fieldEncode(row['school_name'])
            row_data['school_city']  = fieldEncode(row['school_city'])
            row_data['school_into_date']  = fieldEncode(row['school_into_date'])
            row_data['school_leave_date']  = fieldEncode(row['school_leave_date'])
        if len(rows)>0 : user_data['educations'] = rows
        
        ## user sound data / mutiline
        sql = sqlprf % ('sounds', 'order by row_serial')
        rs = self.dbConns.execute(sql)
        rows = []
        for row in rs:
            row_data = {}
            rows.append(row_data)
            row_data['row_serial'] = fieldEncode(row['row_serial'])
            row_data['sound_class'] = fieldEncode(row['sound_class'])
            row_data['sound_caption'] = fieldEncode(row['sound_caption'])
            row_data['sound_url']  = fieldEncode(row['sound_url'])
            rows.append(row_data)
        if len(rows)>0 : user_data['sounds'] = rows

        ## user geo data / mutiline
        sql = sqlprf % ('geoes', 'order by row_serial')
        rs = self.dbConns.execute(sql)
        rows = []
        for row in rs:
            row_data = {}
            rows.append(row_data)
            row_data['row_serial'] = fieldEncode(row['row_serial'])
            row_data['geo_type'] = fieldEncode(row['geo_type'])
            row_data['tz']  = fieldEncode(row['tz'])
            row_data['geo_lat']  = fieldEncode(row['geo_lat'])
            row_data['geo_lng']  = fieldEncode(row['geo_lng'])
            row_data['record_date']  = fieldEncode(row['record_date'])
        if len(rows)>0 : user_data['geoes'] = rows


        # user addition field and common data , 可兼容上面的格式
        '''
        data_class 1->n row_serial 1->1 info_id 
        {                                                 data_class    row_serial -- info_id
            data_field:data_value,                     <- null          null
            data_class:{data_field:data_value,...},    <- not null      null
            data_class:[{data_field:data_value,...}    <- not null      not null
                       ,{data_field:data_value,...}],  
            invalid                                    <- null          not null
        }
        '''
        ### todo: addition data re 
        sql = 'select *, userinfo.info_id as infoid from userinfo inner join userinfo_data on userinfo.info_id=userinfo_data.info_id \
where user_id= %s and (selected=1) and (under=0) \
order by row_serial, data_class' % (userid)
        rs = self.dbConns.execute(sql)
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
        sql = 'select *,d.info_id as infoid, a.app_id as appid from userinfo_account d inner join apps a on d.app_id = a.app_id \
where user_id= %s ' % (userid)
        rs = self.dbConns.execute(sql)
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
        data_class 1->n row_serial 1->1 info_id 
        {
            app_id:n
            app_account:abcd
                                                          data_class    row_serial -- info_id
            data_field:data_value,                     <- null          null
            data_class:{data_field:data_value,...},    <- not null      null
            data_class:[{data_field:data_value,...}    <- not null      not null
                       ,{data_field:data_value,...}],  
            invalid                                    <- null          not null
        }
        '''

        sql = 'select *, userinfo.info_id as infoid from userinfo inner join userinfo_data on userinfo.info_id=userinfo_data.info_id \
where (user_id= %s) and (selected=1) and (under=1) and (not isnull(app_id)) \
order by app_id, row_serial, data_class' % (userid)
        rs = self.dbConns.execute(sql)
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
        #    return None


        if friend == 0:
            sql = 'select * from user_relation where (%s = %s) and (deleted=0) order by contact_alias  %s' % (f,i,limit)
        elif userid != 0 :
            if  friend == 1 : #    marge app, 忽略应用归属计算双向好友
                sql = 'SELECT distinct user_relation.* FROM user_relation inner join  user_relation  ur \
on user_relation.relation_user_id = ur.user_id  \
where user_relation.user_id = %s and ur.relation_user_id = %s order by contact_alias %s' % (i,i,limit)
            elif friend == 2: # relation with app check, 不忽略应用归属计算好友
                sql = 'SELECT distinct user_relation.* FROM user_relation inner join  user_relation  ur \
on user_relation.relation_user_id = ur.user_id  and user_relation.app_id= ur.app_id \
where user_relation.user_id = %s and ur.relation_user_id = %s order by contact_alias  %s' % (i,i,limit)


        idlist = []
        rs = self.dbConns.execute(sql)
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
order by rel_id, data_class, row_serial, userinfo.info_id' % (idliststr)
        rs = self.dbConns.execute(sql)
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
            rs = self.dbConns.execute(sql)
            r = []
            for row in rs:
                r.append(row['rel_id'])
            return r

    
    def appInfoData(self, app_id, param = {}):
        engine = create_engine('mysql://%s:%s@%s:%s/user_profile_m?charset=utf8'%(MYSQLUSER, MYSQLPWD, MYSQLADDR, MYSQLPORT))
        conn   = engine.connect()

        sql = 'select * from apps where (app_id = %s) ' % (app_id)
        rs = self.dbConns.execute(sql)
        appInfo = {}
        for row in rs:
            appInfo['app_id'] = fieldEncode(row['app_id'])
            appInfo['app_name'] = fieldEncode(row['app_name'])
            appInfo['app_type'] = fieldEncode(row['app_type'])
        return appInfo


    def appInfoDataList(self, param = {}):
        engine = create_engine('mysql://%s:%s@%s:%s/user_profile_m?charset=utf8'%(MYSQLUSER, MYSQLPWD, MYSQLADDR, MYSQLPORT))
        conn   = engine.connect()

        limit = self.toLimitString(param)

        sql = 'select * from apps ' + limit
        rs = self.dbConns.execute(sql)
        apps = []
        for row in rs:
            appInfo = {}
            appInfo['app_id'] = fieldEncode(row['app_id'])
            appInfo['app_name'] = fieldEncode(row['app_name'])
            appInfo['app_type'] = fieldEncode(row['app_type'])
            apps.append(appinfo)
        return apps

    '''
    # struct name : user.full,base,ext ; contact.base
    '''
    '''
    # get api data struct define
    #.. api data struct ..
    # api name
    #    struct
    #        struct  <- user define
    #        class row    <- data logic 
    #            row name:filed    <- user define
    #            row field    <- user define
    #        field    <- user define
    #..                 ..
    #    field_type    field_source        param
    #------------------------------------------------------------------------------
    #    list        users,contacts        idlist        data mutiline record
    #    record        user,app,relation    id            data record (exp: userinfo)
    #    classlist    class name            Inherit        data record class  muti line
    #    class        class name            Inherit        data record class  one line
    #    field        data field name        Inherit        field name
    #    classfield    field in class        Inherit        class and field name
    #    param        param name
    #    relfield    rel record field                rel_id_field, rel_rec_name    
    #
    # 获取api返回结构定义
    '''
    #    todo: struct list and first struct
    #
    '''
    def apiStruct(self, dataStructName, root=True):
        apiDefine = []
        if root :
            sql = "select * from apis_struct where struct_name = '%s' and field_ord = 0 " % (dataStructName)
        else :
            sql = "select * from apis_struct where struct_name = '%s' order by field_ord " % (dataStructName)
        rs = self.dbConns.execute(sql)
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
        rs.close()
        if root :
            if len(apiDefine)>0 :
                return apiDefine[0]
            else :
                return None
        else :
            return apiDefine
    '''
    def apiStruct(self, dataStructName, root=True):
        if dataStructName in self.apiStructs:
            if root:
                return self.apiStructs[dataStructName][0]
            else:
                return self.apiStructs[dataStructName]

    def apiStructsFromDB(self):
        self.apiStructs = {}
        sql = 'select * from apis_struct order by struct_name, field_ord'
        rs = self.dbConns.execute(sql)
        for row in rs:
            structname = row['struct_name']
            if structname not in self.apiStructs:
                self.apiStructs[structname] = []
            field = {}
            self.apiStructs[structname].append(field)
            field['caption']= fieldEncode(row['field_caption'])
            field['type']   = fieldEncode(row['field_type'])
            field['source'] = fieldEncode(row['field_source'])
            field['rel_id_field'] = fieldEncode(row['rel_id_field'])
            field['rel_rec_name'] = fieldEncode(row['rel_rec_name'])
            field['struct'] = fieldEncode(row['field_struct'])
        for structname, structvalue in self.apiStructs.iteritems():
            for structdata in structvalue:
                if structdata['type'] in ('list','record','class','classlist'):
                    field_struct = structdata['struct']
                    if field_struct in self.apiStructs:
                        structdata['struct'] = self.apiStructs[field_struct]
                    else:
                        structdata['struct'] = None
        return self.apiStructs

    
    # 解析api返回结构定义
    '''
        返回数据的结构
        api:[
            caption:[                        <- record list
                [                            <- record
                    (caption,value)            <- field 
                    caption:[                <- data class
                        (caption,value)        <- field for class
                    ]
                    caption:[                <- data class list
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
        if field['type']=='field':
            if type(record) is dict:
                if (field['struct'] in record):
                    c = record[field['struct']]
                    if (type(c) is list) and (len(c)>0) :
                        c = c[0]
                else:
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
        #    if (type(record) is dict) and (field['struct'] in record):
        #        c = record[field['struct']]
        #        if (type(c) is list) and (len(c)>0) :
        #            c = c[0]
        #        if (type(c) is dict) and (field['source'] in c) :
        #            parentData[caption]=c[field['source']]
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
                    elif (field['source'] == '*') :
                        r = record
                    elif field['source'][:2] == '- ':
                        if caption in parentData:
                            del parentData[caption]
                        elif field['source'][2:] in record:
                            del record[field['source'][2:]]
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

    def userLookup(self, TelOrEmail='', retType='full', guid=''):
        #format tel
        #format email
        if (TelOrEmail in ['',u'',None]) and (guid in ['',u'',None]) : return None
        if TelOrEmail!='':
            if self.isEMail(TelOrEmail):
                sqlu = 'select user_id from users where email like %s'
                sql = "select user_id from userinfo u inner join userinfo_emails e on u.info_id=e.info_id where email like %s order by versign desc limit 1" 
                param = TelOrEmail
            elif self.isTel(TelOrEmail):
                sqlu = 'select user_id from users where phone like %s'
                sql = "select user_id from userinfo u inner join userinfo_telephones t on u.info_id=t.info_id where tel_number like %s order by versign desc limit 1"
                param = TelOrEmail
        elif guid!='':
            sqlu = 'select user_id from users where guid like %s'
            param = guid

        #print sql
       
        user_id = None
        rs = self.dbConns.execute(sqlu,param)
        if rs.rowcount>0:
            user_id = rs.fetchone()[0]
        else:
            if TelOrEmail != '':
                rs2 = self.dbConns.execute(sql,param)
                if rs2.rowcount>0:
                    user_id = rs2.fetchone()[0]
                rs2.close()
        rs.close()

        result = None
        if user_id != None:
            if retType=='full':
                result = self.userFullData(user_id)
            elif retType=='base':
                result = self.userBaseData(user_id)
            elif retType=='id':
                result = user_id

        return result

    ## user contacts info
    # return contacts with user base data
    def userContacts(self, user_id, param={}):
        return self.apiData(user_id,'api-user-contacts', param)

    # return contacts relation id list
    def userRelationsIdList(self, user_id, param={}):
        return self.userRelationList(user_id,0,param)

    # return relation data for relation id
    def    userRelationData(self, rel_id):
        return self.userRelationDatas(relid = rel_id)
    
    # return Contact data for relation id (with user base)
    def    userContactData(self, rel_id):
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
    def userExists(self, user_id):
        rs = self.dbConns.execute('select user_id from users where user_id=%s',user_id)
        cnt = rs.cursor.rowcount
        rs.close
        if cnt == 1:
            return user_id
        else:
            return None
    
    ###

    def userBatchPut(self, user_id, value):
        if userid == None:
            return

    def userPatch(self, userid, userData):
        return

    ## user addsl,
    def userPost(self, app_id, user_id, userData):
        if type(userData) is dict:
            userData.clone()

        return


    def userIdForIdent(self, userData, app_id):                         
        idenTypes = []
        user_id = None
        sql = []
        if 'versign_phone' in userData:
            sql.append( "(ident_type='tel' and ident='%s')" % userData['versign_phone'] )
        if 'versign_email' in userData:
            sql.append( "(ident_type='email' and ident='%s')" % userData['versign_email'] )
        if 'guid' in userData:
            sql.append( "(ident_type='guid' and ident='%s')" % userData['guid'])
        if 'account' in userData or 'application_account' in userData:
            sql.append( "(ident_type='a%s' and ident='%s')" % (app_id, 
                        userData.get('application_account',userData['account']['app_account'])) )
        if len(sql)>0:
            sql = 'select user_id, ident_type from user_ident where ' + ' or '.join(sql)   
            rs = self.dbConns.execute(sql)
            if rs.rowcount>0:
                rows = rs.fetchall()
                idenTypes = [row['ident_type'] for row in rows]
                user_id = rows[0]['user_id']
            rs.close()
        return (user_id, idenTypes)


    # userData必须是符合修改记录标准的数据，否则可能会引起重复记录。
    # userData结构和输出结构相同，增加若干指示字段
    # 每块记录里可以加入以下字段
    # versign, last_update, source_name, source_id, order, data_class, serial
    #
    #
    def userPut(self, userPutData, app_id, stripMode=strip_mode_nullandempty, checkValid=False, user_state=1): 
        '''
        1. check exists user
        2. check exists fields
        3. exists -> update
        4. not exists -> add new
        5. check selected, z
        '''
        #需要改变传递过来的数据，拷贝一份
        userData = copy.deepcopy(userPutData)
        #清理数据时的规则，
        #保留所有数据，不清除，认可空数据
        #f stripMode == strip_mode_no: 
        emptys=[]
        #数据为空时清除（数据库内为NULL，json为null)
        if stripMode == strip_mode_null: 
            emptys=[None]
        #数据为空或空串时清除
        elif stripMode == strip_mode_nullandempty:
            emptys=[None, '', u'']
        #清理数据，不存储不需要存储的数据
        debugShowData = False
        debugShowData and printJsonData(userData)
        TrimEmptyDataField(userData,emptys)
        #清理数据，剔除无效数据， todo
        if checkValid:
            TrimInvalidData(userData)
        debugShowData and printJsonData(userData)

        #putMode = None # insert, update, replace, ? 放参数里准备批量更新

#        #存在用户则获取user_id,。
#        #是否传递了系统中的用户编号
#        #有认证的phone就取phone
#        #有认证的email就取email
#        #没有有认证的phone,email就取guid，并检查是否已经有这个用户了
#        #这个是为外部使用者添加用户时方便标识用户设置的。可以由对方设置标识，而不是我们返回。

        user_id = userData.get('user_id', None);
        if user_id != None:
            user_id = self.userExists(user_id)
            
        apps = userData.get("applications",None)
        #如果这个传递的数据为单一对象，则转换成列表，和列表形式一起处理。
        if type(apps) is dict:
            apps = [apps]
        app_data = None
        #如果取到了列表，则取出和appid相应的记录
        if type(apps) is list:
            for app in apps:
                if str(app.get('app_id',-1)) == str(app_id):
                    app_data=app
                    break
        if 'applications' in userData:
            del userData['applications']
        if app_data != None:
            app_data['user_id'] = user_id
            app_data['app_id'] = app_id
            userData['account'] = app_data
 
        (user_id,idenTypes) = self.userIdForIdent(userData, app_id)

        #获取连接，成串传送sql。
        conn = self.dbConns.conn_begin()
        #conn = self.dbConns
            

        #新用户
        if user_id == None:
            # add user
            phone = userData.get('versign_phone',None)
            email = userData.get('versign_email',None)
            uguid = guidHex(userData.get('guid',genGUID()))
            sql = 'insert into users (guid,phone,email,user_state) values (%s,%s,%s,%s)'
            rs = conn.execute(sql,uguid,phone,email,user_state)
            #print rs.rowcount, rs.lastrowid
            if rs.rowcount>0:
                user_id = rs.lastrowid
                do_insert = True #==None 直接新增
                userData['guid'] = uguid
            else:
                return None
            rs.close()
        else:
            do_insert = False

        if app_data != None:
             app_data['user_id'] = user_id
            
        
        idents = []
        if 'versign_phone' in userData and 'phone' not in idenTypes:
            idents.append( ('tel', userData['versign_phone']) )
        if 'versign_email' in userData and 'email' not in idenTypes:
            idents.append( ('email', userData['versign_email']) )
        if 'guid' in userData and 'guid' not in idenTypes:
            idents.append( ('guid', userData['guid']) )
        if app_data != None and 'a%s'%(app_id) not in idenTypes:
            idents.append( ('a%s'%(app_id), app_data['app_account']) )
        if len(idents)>0 :
            sql = 'replace user_ident values ' + ','.join("(%s,'%s','%s')" % (user_id,k[0],k[1]) for k in idents)
            rs = conn.execute(sql)
            rs.close()

       
        # 分解用户数据为可更新数据结构
        udf = extractUserDataFields(userData)
        debugShowData and printJsonData(udf)
        for uf in udf:
            #如果不是新增，则先查找记录
            if not do_insert:
                fieldInsert = False
                #print uf
                sqlt = userFieldDataToExistsSql(user_id,app_id,uf)
                #print sqlt[0] % tuple(sqlt[1]) , user_id, app_id, uf
                rs = conn.execute(sqlt[0],sqlt[1])
                if rs.rowcount>0:
                    row = rs.fetchone()
                    rs.close()
                    info_id = row['info_id']
                    sqlt = userFieldDataToUpdateSql(user_id,app_id,info_id,uf)
                    #print sqlt[0] % tuple(sqlt[1])
                    rsu = conn.execute(sqlt[0],sqlt[1])
                    rsu.close()
                    fieldInsert = False
                else:
                    rs.close()
                    fieldInsert = True
            if do_insert or fieldInsert:
                sqlt = userFieldDataToInsertSql(user_id,app_id,uf)
                #print sqlt[0],sqlt[1], sqlt[0] % tuple(sqlt[1])
                rs = conn.execute(sqlt[0],sqlt[1])
                rs.close()
                rs2 = conn.execute('select @dataid')
                info_id = rs2.fetchone()[0]
                rs2.close()
        # 5. todo: select role
            if info_id>0:
                conn.execute('update userinfo set selected=1 where info_id=%s',info_id)
        self.dbConns.conn_end(conn)
        return user_id

    def userAddBlank(self, userData, user_state=0):
        # add user
        sql = 'insert into users (phone, email, guid, user_state) values (%s,%s,%s,%s);'
        rsi = self.dbConns.execute(sql,(
                    userData.get('phone',None),
                    userData.get('email',None),
                    userData.get('guid' ,None), 0))
        if rsi.context.cursor.rowcount >0:
            user_id = rsi.context.cursor.lastrowid
        rsi.close()
        return user_id

    def _contactAdd(self, app_id, contactData):
        user = contactData[0]
        contact = contactData[1]
        relationData = contactData[2]
        
        def getid(user):
            user_id = user.get('user_id',None)
            if user_id == None:
                (user_id, idenTypes) = self.userIdForIdent(user, app_id)
            if user_id == None:
                if user.has_key('phone'):
                    user['versign_phone']=user['phone']
                    if not user.has_key('telephones'):
                        user['telephones']={'tel_type':'mobile','tel_number':trim(user['phone'])}
                if user.has_key('email'):
                    user['versign_email']=user['email']
                    if not user.has_key('emails'):
                        user['emails']={'email_type':'person','email':trim(user['email'])}
                user_id = self.userPut(user, app_id, user_state=0)

            return user_id

        user_id = getid(user)
        contact_id = getid(contact)
        print 'user_id, contact_id',user_id, contact_id
        if (contact_id != None) and (user_id != None):
            if type(relationData) is not dict:
                relationData = {}
            relationData['relation_type']=relationData.get('relation_type','contact')
            vl = []
            ks = ''
            vs = ''
            for r in relationData:
                if r in ['relation_type','contact_alias','contact_group','contact_note','contact_lastdate']:
                    ks = ks + ', ' + r
                    vs = vs + ',%s '
                    vl.append(relationData[r]) 
            sql = 'set @user_id = %s; set @contact_uid = %s; set @app_id = %s; ' 
            sql = sql+'insert into user_relation (user_id,relation_user_id,app_id'+ks+') ' \
+' select * from (select @user_id, @contact_uid, @app_id '+vs+') d where (select count(*) from user_relation '  \
+" where user_id = @user_id and relation_user_id = @contact_uid and app_id=@app_id and relation_type=%s)=0; COMMIT; "
            rs = self.dbConns.execute(sql, [user_id, contact_id, app_id]+vl+[relationData['relation_type']])
            rs.close()
        return [user_id, contact_id] 

    '''
    contactData
    style 1:
        [[user phone, contact phone, relation data],[user phone, contact phone, relation data],...]
    style 2:
        [[user phone, [[contact phone, relation data], [contact phone, relation data], ...]]...]
    style 3:
        [[user email, contact email, relation data],[user email, contact email, relation data],...]
    style 4:
        [[user email, [[contact email, relation data], [contact email, relation data], ...]]...]
    style 5:
        [[user account, contact account, relation data],[user account, contact account, relation data],...]
    style 6:
        [[user account, [[contact account, relation data], [contact account, relation data], ...]]...]
    style 7:
        [[user user_id, contact user_id, relation data],[user user_id, contact user_id, relation data],...]
    style 8:
        [[user user_id, [[contact user_id, relation data], [contact user_id, relation data], ...]]...]
    style 9 [{user object},{user object},{relation data}],[{},{}],...
        [[userdata{email|phone|user_id|user ident: value,...},{email|phone|user_id|user ident: value,...},relation data],[{},{},{}],...]
    '''
    def contactPut(self, app_id, contactDataList, dataStyle=contact_style_phone_1_1):
        def extractData_1_1(data, key):
            if type(data) is list and len(data)>=2:# 对结构容错
                if type(data[0]) in (int,str,unicode,float) and type(data[1]) in (int,str,unicode,float):
                    r = [{key:str(data[0])},{key:str(data[1])}]
                    if len(data)==3 and type(data[2]) is dict:
                        r.append(data[2])
                    else:
                        r.append({})
                    return r

        def add_contract_list_1(data, name):
            r = []
            for item in data:
                contactData = extractData_1_1(item, name)
                if contactData != None:
                    r.append(self._contactAdd(app_id, contactData))
            return r
        
        def add_contract_list_n(data, name):
            r = []
            for item in data:
                user = str(item[0])
                if type(item[1]) is list:
                    for contact in item[1]:
                        if type(contact) is list:
                            contactData = extractData_1_1([user] + copy.deepcopy(contact), name)
                            if contactData != None:
                                r.append(self._contactAdd(app_id, contactData))
            return r

        if type(contactDataList) is not list or len(contactDataList) == 0:
            return
        if dataStyle == contact_style_phone_1_1:
            r = add_contract_list_1(contactDataList, 'phone')
        elif dataStyle == contact_style_phone_1_n:
            r = add_contract_list_n(contactDataList, 'phone')
        elif dataStyle == contact_style_email_1_1:
            r = add_contract_list_1(contactDataList, 'email')
        elif dataStyle == contact_style_email_1_n:
            r = add_contract_list_n(contactDataList, 'email')
        elif dataStyle == contact_style_ident_1_1:
            r = add_contract_list_1(contactDataList, 'account')
        elif dataStyle == contact_style_ident_1_n:
            r = add_contract_list_n(contactDataList, 'account')
        elif dataStyle == contact_style_user_id_1_1:
            r = add_contract_list_1(contactDataList, 'user_id')
        elif dataStyle == contact_style_user_id_1_n:
            r = add_contract_list_n(contactDataList, 'user_id')
        elif dataStyle == contact_style_mix:
            r = []
            for contactData in contactDataList:
                r.append(self._contactAdd(app_id, contactData))
        return r
