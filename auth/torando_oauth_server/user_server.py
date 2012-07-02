#!/usr/bin/python
# encoding: utf-8
# -*- encoding: utf-8 -*-

import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.options
from tornado import gen
from tornado.options import define,options

import os
import asyncmongo
import hashlib

import oauth.oauth as oauth
from tornado_server import OAuthDataStore

class BaseHandler(tornado.web.RequestHandler):
    
    def prepare(self):
        """running some prepare process"""
        try:
            if "X-Http-Method-Override" in self.request.headers:
                self.request.method = self.request.headers["X-Http-Method-Override"]
        except Exception, e:
            raise HttpError(500)
        
    
    @property
    def db(self):
        if not hasattr(self, '_db'):
            self._db = asyncmongo.Client(
                    pool_id='mypool',
                    host='localhost',
                    port=27017,
                    maxcached=10,
                    maxconnections=50,
                    dbname='apps',
                    )
        return self._db

    def get_current_user(self):
        return self.get_secure_cookie("user")

class MainHandler(BaseHandler):
    
    @tornado.web.authenticated
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        name = tornado.escape.xhtml_escape(self.current_user)
        vo = {}
        vo['developer'] = name
        response = yield gen.Task(self.db.applications.find, vo)
        data = response[0][0]
        print data
        self.render('main.html', name=name, applications = data, user = name)


class GenAccessTokenHandler(BaseHandler):
    
    @tornado.web.authenticated
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        vo = {}
        vo['consumer_key'] = self.get_argument('consumer_key')
        vo['consumer_secret'] = self.get_argument('consumer_secret')

        response = yield gen.Task(self.db.applications.find, vo)
        data = response[0][0]
        if len(data) == 1:
            accessTokenVO = {}
            accessTokenVO['consumer_key'] = data[0]['consumer_key']
            accessTokenVO['consumer_secret'] = data[0]['consumer_secret']
            records = yield gen.Task(self.db.access_tokens.find, accessTokenVO)
            if len(records[0][0]) == 0:
                accessTokenVO['access_key'] = hashlib.sha256(data[0]['title']+'key').hexdigest()
                accessTokenVO['access_secret'] = hashlib.sha256(data[0]['title'] +'secret').hexdigest()
                response = yield gen.Task(self.db.access_tokens.save,accessTokenVO)
                self.render('apps/accessToken.html', data = accessTokenVO, app=data[0], name=tornado.escape.xhtml_escape(self.current_user))
            elif len(records[0][0]) == 1:
                self.render('apps/accessToken.html', data = records[0][0][0], app=data[0], name=tornado.escape.xhtml_escape(self.current_user))
            else:
                self.render('apps/accessToken.html', data = records[0][0][0], app=data[0], name=tornado.escape.xhtml_escape(self.current_user))


class ApplicationHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        name = tornado.escape.xhtml_escape(self.current_user)
        self.render('apps/add.html',name=name)

    @tornado.web.authenticated
    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        vo = {}
        title = self.get_argument('title')
        description = self.get_argument('description')
        developer = tornado.escape.xhtml_escape(self.current_user)
        vo['title'] = title
        vo['description'] = description
        vo['developer'] = developer
        secret_str = '%s-%s' % (title, developer)
        vo['consumer_key'] = hashlib.sha224(title).hexdigest()
        vo['consumer_secret'] = hashlib.sha224(secret_str).hexdigest()
        response = yield gen.Task(self.db.applications.insert, vo)
        self.redirect('/')

class RegistHandler(BaseHandler):
    def get(self):
        self.render("regist.html")
    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        vo = {}
        name = self.get_argument('name')
        password = self.get_argument('password')
        password_verify = self.get_argument('password_verify')
        email = self.get_argument('email')
        if password == password_verify:
            vo['name'] = name
            vo['password'] = hashlib.md5(password).hexdigest()
            vo['email'] = email
            response = yield gen.Task(self.db.developers.insert, vo)
            self.render('profile.html', data = response[0][0])


class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html")

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        name = self.get_argument('name')
        password = self.get_argument('password')
        vo = {}
        vo['name'] = name
        response = yield gen.Task(self.db.developers.find, vo)
        users = response[0][0]
        print users
        print len(users)
        print users[0]
        if len(users) == 1:
            if hashlib.md5(password).hexdigest() == users[0]['password']:
                self.set_secure_cookie('user', self.get_argument('name'))
                self.redirect('/')
            else:
                self.finish('password error')
        else:
            self.finish('found multi user')



class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie('user')
        self.redirect('/login')



class ResourceHandler(tornado.web.RequestHandler):

    @property
    def oauth_server(self):
        if  not hasattr(self, '_oauth_server'):
            self._oauth_server = oauth.OAuthServer(OAuthDataStore())
            self._oauth_server.add_signature_method(oauth.OAuthSignatureMethod_PLAINTEXT())
            self._oauth_server.add_signature_method(oauth.OAuthSignatureMethod_HMAC_SHA1())
        return self._oauth_server


    def prepare(self):
        v_oauth_request = oauth.OAuthRequest.from_request(self.request.method, self.request.uri ,headers = self.request.headers, query_string=self.request.body)
        consumer, token, params = self.oauth_server.verify_request(v_oauth_request)
        # print consumer
        # print token
        # print params
        self.params = params

    def post(self):
        print self.params
        
        self.write('{"code": 200 }')
        


