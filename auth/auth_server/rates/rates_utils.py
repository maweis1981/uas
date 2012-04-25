from logging import Logger
import datetime
from auth_server import settings

__author__ = 'peter'

import redis

"""
###Check Request Rates Strategy

endpoint: uri
client: access_token
user:access_token
ip:access_token
scope:scope

"""

def checkRates(access_token, endpoint, ip):
    #TODO here will be replace with redis connection pool or redis adapter
    #check is exceed rates limited first.
    r = redis.StrictRedis(host=settings.REDIS_HOST, port=6379, db=0)
    key = '%s_%s_%s_key' % (access_token, endpoint, ip)
    print key
    value = r.get(key)
    print value
    if value is None:
        value = 0
    value = int(value)
    print value
    print value > 500
    print 1 > 500
    if value > 500:
        print 'value exceed 500 limits'
        return True

    value = value + 1
    r.set(key, value)
    return False
