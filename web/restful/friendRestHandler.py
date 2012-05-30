#!/usr/bin/env python
# coding: utf-8

"""
friendRestHandler.py

"""

import os, sys, re
from RESTHandler import *
import Pyro4
import logging
import simplejson



class FriendRestHandler(RESTHandler):
    def get(self,id):
        up = self.instanceByName('user_processor')
        param = {}
        friends = up.getFriends(id,param)
        friendsObject = simplejson.dumps(friends)
        code = 200
        message = 'Friend Rest Handler Get Successful'
        return self.render('friend_get.json',code = code, message = message, data = friendsObject)
    
    def post(self,id):
        data = self.instanceByName('user_show_processor').userData(id)
        return self.write(data)
    
    def put(self,id):
        print id
        data = self.instanceByName('user_put_processor').greeting()
        return self.write(data)

    def delete(self,id):
        return self.write('get delete request')
