#!/usr/bin/env python
# encoding: utf-8
"""
server.py

Created by wenzhenwei on 2012-03-20.
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

from tornado.options import define, options

import Pyro4

import pika
from pika.adapters.tornado_connection import TornadoConnection

import init

from basehandler import BaseHandler
from usershandler import UsersHandler
from friendshandler import FriendsHandler


define("port",default=8888, help="run on the given port", type=int)

# define("mysql_host", default="127.0.0.1:3306", help="blog database host")
# define("mysql_database", default="messages", help="blog database name")
# define("mysql_user", default="root", help="blog database user")
# define("mysql_password", default="", help="blog database password")

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/users/(.*)", UsersHandler),
			(r"/friends/(.*)", FriendsHandler),
			(r"/messages/(.*)/(.*)", MessagesHandler)
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

		# Have one global connection to the blog DB across all handlers
		# self.db = tornado.database.Connection(
		#		   host=options.mysql_host, database=options.mysql_database,
		#		   user=options.mysql_user, password=options.mysql_password)



class MessagesHandler(BaseHandler):
	def get(self, *messages, **extras):
		return self.write(str(messages) + " " + str(extras) + " " + self.get_argument("wuwu"))

def main():
	tornado.options.parse_command_line()
	
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	
	ioloop = tornado.ioloop.IOLoop.instance()
	ioloop.start()


if __name__ == "__main__":
	main()
