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
      data = self.user_show_processor.show(id, 2, None)
      return self.render('usershow.json',data = simplejson.loads(data))
    
    def post(self,id):
      data = self.user_processor.objectByPK(id)
      print data
      return self.render('usershow.json', data = simplejson.loads(data))

    def put(self,id):
      return self.write('get put request')

    def delete(self,id):
      return self.write('get delete request')
