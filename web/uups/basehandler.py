#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by Peter Ma on 2012-01-11.
Copyright (c) 2012 Maven Studio. All rights reserved.
"""

import init

import tornado.web
import urllib2
import json
import logging

class BaseHandler(tornado.web.RequestHandler):
	"""
	"""
	authAddr = "http://192.168.91.48:8000/auth/validate"
	def prepare(self):
		print '--process authorized info in http header.'
		try:
			f = urllib2.urlopen(BaseHandler.authAddr + "?access_token=%s&endpoint=%s" % (self.get_argument("access_token").encode("utf8"), self.get_argument("endpoint").encode("utf8")))
			res = f.read()
			if res == None:
				logging.error("ip: " + self.request.remote_ip + " receive no data from auth server")
				self.send_error(500)
			jres = json.loads(res)
			if jres["code"] != 200:
				# log
				logging.error("ip: " + self.request.remote_ip + " " + str(res))
				self.send_error(jres["code"], jres)
			logging.info("ip: " + self.request.remote_ip + " access validated")
		except Exception,e:
			self.send_error(500)
			logging.error("ip: " + self.request.remote_ip + " " + str(e))
		
	@property
	def db(self):
		# return self.application.db
		pass


