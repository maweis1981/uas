#!/usr/bin/env python
# coding: utf8
# author: Maven
# datetime: 15 May 2012

from userProcessor import UserProcessor
from userPutProcessor import UserPutProcessor
import threading
import Pyro4
from tornado.options import define, options

define("running_pyro4_host", default="192.168.91.48", help="Pyro4 nameserver running host")
define("running_pyro4_port", default=9999, help="Pyro4 nameserver running port", type=int)

define("running_service_host", default="192.168.248.37", help="Service Running host")

#start processor server
if __name__ == "__main__":
  print 'processor server will be start...'

  Pyro4.config.HOST = options.running_service_host
  Pyro4.config.NS_HOST = options.running_pyro4_host
  Pyro4.config.NS_PORT = options.running_pyro4_port

  Pyro4.Daemon.serveSimple(
      {
        UserProcessor(): "user_processor",
        UserPutProcessor(): "user_put_processor",
      },
    ns=True, verbose=True)

