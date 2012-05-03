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
from testRestfulHandler import testHandler

define("port", default=8888, help="server running on port", type=int)

class Application(tornado.web.Application):
  def __init__(self):
    handlers = [
            (r'/test/(.*)', testHandler),
          ]
    settings = dict(
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
  main()
