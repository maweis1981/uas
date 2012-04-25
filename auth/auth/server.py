#!/usr/bin/env python
# encoding: utf-8
"""
server.py

Created by Peter Ma on 2012-03-20.
Copyright (c) 2012 Maven Studio. All rights reserved.
"""

import sys
import os

import re
import tornado.auth
import tornado.database
import tornado.httpserver
import tornado.ioloop

import tornado.web
import unicodedata
import simplejson

from tornado.options import define, options
import tornado.autoreload

import oauth2 as oauth
import time
from apis import TestAPIHandler

params = {
    'oauth_version': '2.0',
    'oauth_nonce': oauth.generate_nonce(),
    'oauth_timestamp': int(time.time()),
}

define("port", default=8888, help="run the oauth server on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="auth server database host")
define("mysql_database", default="auth", help="auth server database name")
define("mysql_user", default="root", help="auth server database user")
define("mysql_password", default="", help="auth server database password")

class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/apps",AppsHandler),
            (r"/apps/create",CreateAppHandler),
            (r"/apps/([^/]+)",AppHandler),
            (r"/auth/login", AuthLoginHandler),
            (r"/auth/logout", AuthLogoutHandler),
            (r"/oauth2/v1/request_token", TokenHandler),
            (r"/oauth2/v1/authorize", AuthorizeHandler),      
            (r"/oauth2/v1/access_token", AccessTokenHandler),
            (r"/oauth2/v1/refresh_token", RefreshTokenHandler),  
            (r"/apis/v1/test", TestAPIHandler),  
        ]
        settings = dict(
            debug = True,
            app_title = u"SNDA OAuth2",
            template_path = os.path.join(os.path.dirname(__file__), "templates"),
            static_path = os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookie = True,
            cookie_secret = "4Gplr40ITRS4xjZMZV0ZKkzUmlmt60PrkYGDTg6QM+8=",
            login_url ="/auth/login",
        )
        
        self.db = tornado.database.Connection(
            host = options.mysql_host, 
            database = options.mysql_database,
            user = options.mysql_user,
            password = options.mysql_password
        )
        
        tornado.web.Application.__init__(self, handlers, **settings)
        
class BaseHandler(tornado.web.RequestHandler):
    def prepare(self):
        print 'running prepare'
        
    @property    
    def db(self):
        return self.application.db
        
    def get_current_user(self):
        user_id = self.get_secure_cookie("user")
        if not user_id: return None
        return self.db.get("SELECT * FROM USERS WHERE ID = %s", int(user_id))
        
class AppsHandler(BaseHandler):
    def get(self):
        apps = self.db.query("select * from apps order by date_joined desc limit 5")
        if not apps:
            self.redirect("/apps/create")
            return
        self.render("apps.html", apps = apps)

class AppHandler(BaseHandler):
    def get(self,id):
        app = self.db.query("select * from apps where id = %s",id)
        if not app: raise tornado.web.HTTPError(404)
        self.render("app.html", app = app)
        
class CreateAppHandler(BaseHandler):
    def get(self):
        self.render("create_app.html")
        
    def post(self):
        name = self.get_argument("name",None)
        consumer_key = self.get_argument("consumer_key")
        consumer_secret = self.get_argument("consumer_secret")
        description = self.get_argument("description")
        website = self.get_argument("website")
        callback = self.get_argument("callback")
        ip_address = self.get_argument("ip_address")
        
        if  name:
            self.db.execute(
                "insert into apps (name,consumer_key,consumer_secret,description,website,callback,ip_address,date_joined)"
                "values (%s,%s,%s,%s,%s,%s,%s,UTC_TIMESTAMP())",
                name,consumer_key,consumer_secret,description,website,callback,ip_address)
                # generate consumer_key & consumer_secret
                
        else:
            self.render("create_app.html")
        
        self.redirect("/apps")
  
class AuthLoginHandler(BaseHandler, tornado.auth.GoogleMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("openid.mode", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authenticate_redirect()
    
    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Google auth failed")
        author = self.db.get("SELECT * FROM authors WHERE email = %s",
                             user["email"])
        if not author:
            # Auto-create first author
            any_author = self.db.get("SELECT * FROM authors LIMIT 1")
            if not any_author:
                author_id = self.db.execute(
                    "INSERT INTO authors (email,name) VALUES (%s,%s)",
                    user["email"], user["name"])
            else:
                self.redirect("/")
                return
        else:
            author_id = author["id"]
        self.set_secure_cookie("user", str(author_id))
        self.redirect(self.get_argument("next", "/"))


class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))     
        
        
class TokenHandler(BaseHandler):
    def get(self):
        self.write('token')
        
class AuthorizeHandler(BaseHandler):
    def get(self):
        self.write('authorize')
        
class AccessTokenHandler(BaseHandler):
    def get(self):
        self.write('access token')
        
class RefreshTokenHandler(BaseHandler):
    def get(self):
        self.write('refresh token')
        

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()

