#!/usr/bin/env python
# encoding: utf-8

"""
author: maven

"""

import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
from userRestHandler import UserRestHandler
from userLookupRestHandler import UserLookupRestHandler
from contactRestHandler import ContactRestHandler
from inContactRestHandler import InContactRestHandler
from appRestHandler import AppRestHandler

import logging

define("port", default=8888, help="API Server running on port", type=int)

class Application(tornado.web.Application):
  def __init__(self):
    handlers = [
            (r'/api/v1/user/([0-9]+)', UserRestHandler),
            (r'/api/v1/user/([0-9]+)/contacts', ContactRestHandler),
            (r'/api/v1/user/([0-9]+)/in_contacts', InContactRestHandler),
            (r'/api/v1/user/([0-9]+)/apps', AppRestHandler),
            (r'/api/v1/lookup/(.*)', UserLookupRestHandler),
          ]
    settings = dict(
                template_path=os.path.join(os.path.dirname(__file__), 'templates'),
                debug=True
              )
    tornado.web.Application.__init__(self,handlers, **settings)


def main():
  tornado.options.parse_command_line()

  http_server = tornado.httpserver.HTTPServer(Application())
  http_server.listen(options.port)

  ioloop = tornado.ioloop.IOLoop.instance()
  ioloop.start()


if __name__ == '__main__':
  logging.basicConfig(
          level = logging.DEBUG,
          filename = 'api_server.log',
          filemode = 'w',
          )

  logging.info('start api server')
  main()
