#!/usr/bin/env python
# coding: utf8
# author: Maven
# datetime: 15 May 2012

from userProcessor import UserProcessor

def startProcessor():
  #regist user processor
  up = UserProcessor()
  #set name in nameserver
  up.registIntoNameServer('user_processor')
  


#start processor server
if __name__ == "__main__":
  startProcessor()
