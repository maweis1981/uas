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

class RESTHandler(tornado.web.RequestHandler):

  """
  do prepare operation in 
  @TODO add auth validate
  @TODO add rates limit
  @TODO write to audit log
  @TODO auto enable redis,mq,process naming

  """
  def prepare(self):
    if "X-Http-Method-Override" in self.request.headers:
      self.request.method = self.request.headers["X-Http-Method-Override"]
