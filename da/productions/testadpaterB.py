import os,sys,inspect
import logging
import json


from dbWorker import DatabaseWorker


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

'''
print '\n--------------------------------'

v = d.userBaseData(12)
printJsonData(v)
'''

#print '\n--------------------------------'

#v = d.apiStruct('api-user-fullinfo',True)
#printJsonData(v)

#print '\n--------------------------------'

#v = d.userFullData(12)
#printJsonData(v)

#v = d.userLookup('mawei02@snda.com','base')
#v = d.userLookup('energy@sohu.com','base')
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

#v = d.userRelationDatas(userid=12,friend=1)
#printJsonData(v)

v = d.apiData(12,'api-user-friends')
printJsonData(v)



