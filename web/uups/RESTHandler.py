#!/usr/bin/env python
# encoding: utf-8

"""
RESTHandler.py

Create by Maven on 3 May 2012
Copyright (c) 2012 Maven Studio. All rights reserved
"""

import tornado.web
import json
import logging
import ConfigParser
import urllib2
import Pyro4
from tornado.options import define, options

define("auth_uri", default="http://192.168.91.48:8000/auth/validate", help="auth server uri")
define("pyro4_address", default="192.168.91.48", help="pyro4 server address")
define("pyro4_port", default=9999, help="pyro4 server port", type=int)


class RESTHandler(tornado.web.RequestHandler):

  """
  do prepare operation in 
  @TODO add auth validate
  @TODO add rates limit
  @TODO write to audit log
  @TODO auto enable redis,mq,process naming

  """
  def prepare(self):
    try:
      auth_server_uri = "%s?access_token=%s&endpoint=%s" % (options.auth_uri , self.get_argument("access_token").encode("utf8"), self.get_argument("end_point").encode("utf8"))
      print auth_server_uri
      f = urllib2.urlopen(auth_server_uri,timeout=3)
      res = f.read()
      if res == None:
        logging.error("ip: %s Receive Null Data From Auth Server." % self.request.remote_ip)
        self.finish('401')
      elif json.loads(res)["code"] != 200:
        logging.error("ip: %s %s" % (self.request.remote_ip, json.loads(res)["message"]))
        self.finish(res)

      logging.info("ip: %s access validated" % self.request.remote_ip)
      
      if "X-Http-Method-Override" in self.request.headers:
        self.request.method = self.request.headers["X-Http-Method-Override"]

    except Exception, e:
      self.finish('500')
      logging.error("ip: %s %s" % (self.request.remote_ip, str(e)))
        
  @property
  def application_info(self):
    return "application mocked data"
  
  def instanceByName(self, name):
    ns = Pyro4.locateNS(host=options.pyro4_address, port=options.pyro4_port)
    uri = ns.lookup(name)
    instanceProcessor = Pyro4.Proxy(uri)
    return instanceProcessor

  @property
  def user_show_processor(self):
    ns = Pyro4.locateNS(host=options.pyro4_address, port=options.pyro4_port)
    uri = ns.lookup('user_show_processor')
    userShowProcessor = Pyro4.Proxy(uri)
    return userShowProcessor

  @property
  def user_processor(self):
    ns = Pyro4.locateNS(host=options.pyro4_address, port=options.pyro4_port)
    uri = ns.lookup('user_processor')
    userProcessor = Pyro4.Proxy(uri)
    return userProcessor


  @property
  def redisAdapter(self):
    return "Redis Adapter"

