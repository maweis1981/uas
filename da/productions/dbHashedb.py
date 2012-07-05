#!/usr/bin/env python
# encoding: utf-8
"""
dbworker.py
"""

import sys
import os
import copy

from sqlalchemy import *
from datetime import *
from init import *
from types import *

from dbWorkerLib import *
from dbConnections import *
from dbRedis import *

class HashedDatabase(object):

    dbConns = None
    apiStructs = {}

    def __init__(self, dbConns=None):
        if dbConns == None:
            dbConns = DatabaseConnections()
        self.dbConns = dbConns

    

