#!/usr/bin/env python
# coding: utf-8

"""
contactRestHandler.py

"""

import os, sys, re
from RESTHandler import *
import Pyro4
import logging
import simplejson



class ContactRestHandler(RESTHandler):
    def get(self,id):
        up = self.instanceByName('user_processor')
        param = {}
        contacts = up.getContacts(id,param)
        contactsObject = simplejson.dumps(contacts)
        code = 200
        message = 'Contact Rest Handler Get Successful'
        return self.render('contact_get.json',code = code, message = message, data = contactsObject)
    
    def post(self,id):
        data = self.instanceByName('user_show_processor').userData(id)
        return self.write(data)
    
    def put(self,id):
        print id
        data = self.instanceByName('user_put_processor').greeting()
        return self.write(data)

    def delete(self,id):
        return self.write('get delete request')
