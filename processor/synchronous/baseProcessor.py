#!/usr/bin/env python
# coding: utf8
# Copyright 2012 SNDA
# Author: Maven
# DateTime: 15 May 2012

"""
Base Processor
Extract common attributes into Base Processor.

"""
import json
import Pyro4
import redis
from tornado.options import define, options

define("pyro4_host", default="192.168.91.48", help="Pyro4 nameserver running host")
define("pyro4_port", default=9999, help="Pyro4 nameserver running port", type=int)
define("service_host", default="192.168.248.37", help="Service Running host")


class BaseProcessor(object):
  
  def __init__(self, **kwargs):
    for key in kwargs:
      f = getattr(self, 'set_' + key)
      f(kwargs[key])

  def set_id(self, id = None):
    print id
    pass

  def set_name(self, name = None):
    print name
    pass

  def instanceByName(self, name):
    ns = Pyro4.locateNS(host = options.pyro4_host, port = options.pyro4_port)
    uri = ns.lookup(name)
    instanceProcessor = Pyro4.Proxy(uri)
    if instanceProcessor:
      return instanceProcessor
    else:
      raise Exception('Not Found %s instance in name server' % name)

  def registIntoNameServer(self, name):
    daemon = Pyro4.Daemon(host = options.service_host)
    server_uri = daemon.register(self)

    ns = Pyro4.locateNS(host = options.pyro4_host, port = options.pyro4_port)
    uri = ns.register(name, server_uri)

    daemon.requestLoop()
