#!/usr/bin/env python
# coding: utf-8

"""
appRestHandler.py

"""

import os, sys, re
from RESTHandler import *
import Pyro4
import logging
import simplejson



class AppRestHandler(RESTHandler):
    def get(self,id):
        up = self.instanceByName('user_processor')
        param = {}
        apps = up.getUserApps(id,param)
        appsObject = simplejson.dumps(apps)
        code = 200
        message = 'Application Rest Handler Get Successful'
        return self.render('app_get.json',code = code, message = message, data = apps)
    
    def post(self,id):
        data = self.instanceByName('user_show_processor').userData(id)
        return self.write(data)
    
    def put(self,id):
        print id
        data = self.instanceByName('user_put_processor').greeting()
        return self.write(data)

    def delete(self,id):
        return self.write('get delete request')
