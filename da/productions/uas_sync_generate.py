# !/usr/bin/python
# encoding=utf8

import os,sys
import urllib2

if __name__ == "__main__":
    c = """{
"count":5,
"length":1024,
"data":[
{
"id":12345,
"name":"test User 1",
"gender":"female"
},
{
"id":12346,
"name":"test User 2",
"gender":"male"
}
]
}"""
    f = urllib2.urlopen("http://192.168.91.171:8888/users/12235/sync?access_token=1234567&endpoint=users:query",
                        c)
    r = f.read()
    print (r)
    f.close()
