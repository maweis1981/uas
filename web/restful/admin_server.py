#!/usr/bin/env python
# encoding: utf-8
"""
server.py

Created by maven on 15 May 2012.
Copyright (c) 2012 snda inc. All rights reserved.
"""

import os.path
import re
import tornado.auth
import tornado.database
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import unicodedata
import simplejson

from tornado.options import define, options

import Pyro4
from Pyro4 import naming


define("port",default=7001, help="admin website run on the given port", type=int)

define("pyro4_host", default="192.168.91.48", help="pyro4 nameserver host")
define("pyro4_port", default=9999, help="pyro4 nameserver port", type=int)

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/servers", ServersHandler),
		]
		settings = dict(
			app_title=u"SNDA Universal User Profile Service",
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			static_path=os.path.join(os.path.dirname(__file__), "static"),
			xsrf_cookies=False,
			cookie_secret="11oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
			debug=True,		
		)
		tornado.web.Application.__init__(self, handlers, **settings)


class ServersHandler(tornado.web.RequestHandler):
	def get(self):
          nameserver = naming.locateNS(options.pyro4_host, options.pyro4_port)
          list = nameserver.list()
          self.write('<h1> Running Services </h1>')
          for name,uri in list.items():
            self.write('<b>')
            self.write('%s --> %s' % (name, uri))
            self.write('</b><br/>')
          self.write('<br/><br/><br/>')
          self.write('@copyright Maven')

def main():
	tornado.options.parse_command_line()
	
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	
	ioloop = tornado.ioloop.IOLoop.instance()
	ioloop.start()


if __name__ == "__main__":
	main()
