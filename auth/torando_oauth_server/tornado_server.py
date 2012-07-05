#!/usr/bin/python
# encoding: utf-8
# -*- encoding: utf-8 -*-

import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.options
from tornado.options import define,options

import logging
import os
import pymongo
from pymongo import Connection

import oauth.oauth as oauth

CALLBACK_URL = 'http://localhost/request_token_ready'
VERIFIER = 'verifier'

class OAuthDataStore(oauth.OAuthDataStore):
   
    # this is test data, will be updated to use database
    # def __init__(self, consumer_key, consumer_secret, request_key, request_secret, access_key, access_secret):
    def __init__(self):
        # set default empty key
        self.consumer = oauth.OAuthConsumer('a', 'a')
        self.request_token = oauth.OAuthToken('a', 'a')
        self.access_token = oauth.OAuthToken('a', 'a')

        self.nonce = 'nonce'
        self.verifier = VERIFIER
        # initial mongodb connection
        connection = Connection('localhost', 27017)
        self.db = connection['apps']

    def lookup_consumer(self, key):
        consumer = self.db.applications.find_one({'consumer_key': key})
        self.consumer = oauth.OAuthConsumer(consumer['consumer_key'], consumer['consumer_secret'])
        #TODO: need to load request token
        accessToken = self.db.access_tokens.find_one({'consumer_key': self.consumer.key, 'consumer_secret': self.consumer.secret})
        self.access_token = oauth.OAuthToken(accessToken['access_key'], accessToken['access_secret'])
        print 'application [%s] access, developer is [%s]' % (consumer['title'], consumer['developer'])
        return self.consumer

    def lookup_token(self, token_type, token):
        token_attrib = getattr(self, '%s_token' % token_type)
        if token == token_attrib.key:
            token_attrib.set_callback(CALLBACK_URL)
            return token_attrib
        return None

    def lookup_nonce(self, oauth_consumer, oauth_token, nonce):
        if oauth_token and oauth_consumer.key == self.consumer.key and (oauth_token.key == self.request_token.key or oauth_token.key == self.access_token.key) and nonce == self.nonce:
            return self.nonce
        return None

    def fetch_request_token(self, oauth_consumer, oauth_callback):
        if oauth_consumer.key == self.consumer.key:
            if oauth_callback:
                self.request_token.set_callback(oauth_callback)
            return self.request_token
        return None

    def fetch_access_token(self, oauth_consumer, oauth_token, oauth_verifier):
        if oauth_consumer.key == self.consumer.key and oauth_token.key == self.request_token.key and oauth_verifier == self.verifier:
            # want to check here if token is authorized
            # for mock store, we assume it is
            return self.access_token
        return None

    def authorize_request_token(self, oauth_token, user):
        if oauth_token.key == self.request_token.key:
            # authorize the request token in the store
            # for mock store, do nothing
            return oauth_token
        return None


class baseHandler(tornado.web.RequestHandler):

    def prepare(self):
        print '-----------------------------------------'
        print 'uri is %s %s ' % (self.request.uri ,self.request.query)
        print '-----------------------------------------'
        """running some prepare process"""
        try:
            if "X-Http-Method-Override" in self.request.headers:
                self.request.method = self.request.headers["X-Http-Method-Override"]
        except Exception, e:
            raise HttpError(500)


    @property
    def oauth_request(self):
        if  not hasattr(self, '_oauth_request'):
            postdata = self.request.query
            if self.request.method == 'POST':
                try:
                    postdata = self.request.body
                except:
                    pass
            self._oauth_request = oauth.OAuthRequest.from_request(self.request.method, self.request.uri, headers = self.request.headers, query_string=postdata)
        return self._oauth_request

    @property
    def db(self):
        if  not hasattr(self, '_db'):
            self._db = asyncmongo.Client(
                    pool_id='mypool', 
                    host = 'localhost', 
                    port=27017, 
                    maxcached=10, 
                    maxconnections=50, 
                    dbname='apps',
                )
        return self._db

    @property
    def oauth_server(self):
        if  not hasattr(self, '_oauth_server'):
            self._oauth_server = oauth.OAuthServer(OAuthDataStore())
            self._oauth_server.add_signature_method(oauth.OAuthSignatureMethod_PLAINTEXT())
            self._oauth_server.add_signature_method(oauth.OAuthSignatureMethod_HMAC_SHA1())
        return self._oauth_server


# regist a user
class UserHandler(baseHandler):
    
    def get(self):
        pass      

class RequestTokenHandler(baseHandler):

    def post(self):
        print 'post command'

    def get(self):
        token = self.oauth_server.fetch_request_token(self.oauth_request)
        self.write(token.to_string())

class AuthorizationHandler(baseHandler):
    def post(self):
        print 'post'

    def get(self):
        token = self.oauth_server.fetch_request_token(self.oauth_request)
        token = self.oauth_server.authorize_token(token, None)
        token.set_verifier(VERIFIER)
        self.write(token.get_callback_url())


class AccessTokenHandler(baseHandler):
    
    def post(self):
        print 'post in access token handler'
    
    def get(self):
        token = self.oauth_server.fetch_access_token(self.oauth_request)
        self.write(token.to_string())



