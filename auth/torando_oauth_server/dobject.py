#!/usr/bin/python
# encoding: utf-8
# -*- encoding: utf-8 -*-

'''
File: dobject.py
Author: Maven v@maweis.com
Description:  Dragonfly Object Handler
'''

# from baseHandler import baseHandler
# from local_baseHandler import baseHandler
from user_server import BaseHandler

import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.options
from tornado import gen
from tornado.options import define,options

import simplejson
from bson.objectid import ObjectId

from shortcuts import handle_mongo_result
import oauth.oauth as oauth
from tornado_server import OAuthDataStore

from bson.json_util import default

class DObjectHandler(BaseHandler):

    @property
    def oauth_server(self):
        if  not hasattr(self, '_oauth_server'):
            self._oauth_server = oauth.OAuthServer(OAuthDataStore())
            self._oauth_server.add_signature_method(oauth.OAuthSignatureMethod_PLAINTEXT())
            self._oauth_server.add_signature_method(oauth.OAuthSignatureMethod_HMAC_SHA1())
        return self._oauth_server


    def prepare(self):
        print self.request.uri
        print self.request.method
        v_oauth_request = oauth.OAuthRequest.from_request(self.request.method, self.request.uri ,headers = self.request.headers, query_string=self.request.body)
        consumer, token, params = self.oauth_server.verify_request(v_oauth_request)
        self.params = params
        

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self, objectName=None):
        response = handle_mongo_result((yield gen.Task(
            self.db.connection(collectionname=objectName).find)))
        print response
        response = simplejson.dumps(response, default=default)
        print response
        self.finish(response)


    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self, objectName=None):
        vo = {}
        vo['object_name'] = objectName
        records = yield gen.Task(self.db.stores.find, vo)
        if len(records[0][0]) == 0:
            response = yield gen.Task(self.db.stores.insert,vo)
        app = self.params
        response = handle_mongo_result((yield gen.Task(
            self.db.connection(collectionname=objectName).insert,
                    app)))
        self.finish('{"code": 200, "message": "object saved!"}')

    def put(self, _objectId):
        self.write('put')
        
    def delete(self, _objectId):
        self.write('delete')
