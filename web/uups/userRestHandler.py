#!/usr/bin/env python
# coding: utf-8

"""
userRestHandler.py

"""

import os, sys, re
from RESTHandler import *
import Pyro4
import logging
import simplejson

from init import *


class UserRestHandler(RESTHandler):
    def get(self,id):
        ns = Pyro4.locateNS(host=PYRONSADDR, port=PYRONSPORT)
        uri = ns.lookup('user_show_processor')
        userProcessor = Pyro4.Proxy(uri)
        print id
        data = userProcessor.show(id, 2, None)
        print simplejson.loads(data)
        return self.render('usershow.json',data = simplejson.loads(data))
    
    def post(self,id):
        return self.write('get post request')

    def put(self,id):
        return self.write('get put request')

    def delete(self,id):
        return self.write('get delete request')
