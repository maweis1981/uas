#!/usr/bin/env python
# encoding: utf-8

"""
author: maven

"""

import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.web

from tornado.options import define, options

import logging

from user_server import MainHandler,RegistHandler,LoginHandler,LogoutHandler,ApplicationHandler,GenAccessTokenHandler,ResourceHandler

from tornado_server import RequestTokenHandler,AccessTokenHandler,AuthorizationHandler
from dobject import DObjectHandler,DObjectManager

define("port", default=80, help="User Auth Server running on port", type=int)

class Application(tornado.web.Application):
  def __init__(self):
    handlers = [
            (r'^/request_token$', RequestTokenHandler),
            (r'^/access_token$', AccessTokenHandler),
            (r'^/authorize$', AuthorizationHandler),
            (r"^/regist$", RegistHandler),
            (r"^/login$", LoginHandler),
            (r"^/logout$", LogoutHandler),
            (r"^/app$", ApplicationHandler),
            (r"^/accessToken$", GenAccessTokenHandler),
            (r'^/photos$', ResourceHandler), 
            (r'^/do/([^/]+)$', DObjectHandler),
            (r'^/do$', DObjectHandler),
            (r'^/admin/do/([^/]+)$', DObjectManager), #custom object rest
            (r'^/admin/do$', DObjectManager), #custom object rest
            (r"^/$", MainHandler),
          ]
    settings = dict(
                cookie_secret='12345',
                login_url='/login',
                template_path=os.path.join(os.path.dirname(__file__), 'templates'),
                static_path   = os.path.join(os.path.dirname(__file__), 'static'),
                debug=True,
              )
    tornado.web.Application.__init__(self, handlers, **settings)


def main():
  tornado.options.parse_command_line()

  http_server = tornado.httpserver.HTTPServer(Application())
  http_server.listen(options.port)

  ioloop = tornado.ioloop.IOLoop.instance()
  ioloop.start()


if __name__ == '__main__':
  logging.basicConfig(
          level = logging.DEBUG,
          filename = 'auth_server.log',
          filemode = 'w',
          )

  logging.info('start oauth server')
  main()
