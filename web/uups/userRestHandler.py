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
        data = self.instanceByName('user_show_processor').userData(id)
        
        return self.write(data)
    
    def post(self,id):
        data = self.instanceByName('user_show_processor').userData(id)
        return self.write(data)
    
    def put(self,id):
        print id
        data = self.instanceByName('user_put_processor').greeting()
        return self.write(data)

    def delete(self,id):
        return self.write('get delete request')
