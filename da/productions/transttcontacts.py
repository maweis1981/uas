from dbTrans import *


import time

if len(sys.argv)>1 : 
    umax=sys.argv[1]
else :
    umax=10
    
if len(sys.argv)>2 : 
    cmax=sys.argv[2]
else :
    cmax=30

trans = DatabaseTrans()
t1 = time.time()
trans.ttcontactTrans(umax,cmax)
t2 = time.time()

print t1,t2, t2-t1
