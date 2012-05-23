import Pyro4
from init import *
import sys


if len(sys.argv)>1 : 
    userid=sys.argv[1]
else :
    userid=123
    
if len(sys.argv)>2 : 
    level=sys.argv[2]
else :
    level=2
    
ns = Pyro4.locateNS(host=PYRONSADDR, port=PYRONSPORT)
uri = ns.lookup("database_handler")
dbProcessor = Pyro4.Proxy(uri)
data = dbProcessor.userShow(userid, level, None)

print(data)
 
