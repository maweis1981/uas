import os,sys,inspect
#from init import *
import logging
import json

curFilePath = os.path.abspath(os.path.dirname(inspect.stack()[1][1]))
sys.path.append(os.path.dirname(curFilePath)+"\\productions")
print curFilePath

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
v = d.userData(12)
#print v ,'\n'
#printvalue(v)
printJsonData(v)




print '\n--------------------------------'

v = d.apiStruct('api-user-baseinfo',True)
printJsonData(v)

print '\n--------------------------------'

v = d.userBaseData(12)
printJsonData(v)

'''
print '\n--------------------------------'

v = d.apiStruct('api-user-fullinfo',True)
printvalue(v)

print '\n--------------------------------'

v = d.userFullData(12)
printvalue(v)
print v
'''


