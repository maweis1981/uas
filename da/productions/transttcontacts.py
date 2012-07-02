from dbTrans import *


import time

trans = DatabaseTrans()
t1 = time.time()
trans.ttcontactTrans()
t2 = time.time()

print t1,t2, t2-t1
