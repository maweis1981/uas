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



class UserLookupRestHandler(RESTHandler):
    def get(self,attribute):
        up = self.instanceByName('user_processor')
        userData = up.searchUserData(attribute)
        if userData != None:
            userObject = simplejson.dumps(userData)
            code = 200
            message = 'User Rest Handler Get Successful'
        else:
            code = 404
            message = 'Not Found User'
            userObject = None
        return self.render('user_get.json',code = code, message = message, data = userObject)
