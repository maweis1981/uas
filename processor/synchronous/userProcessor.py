#!/usr/bin/env python
# coding: utf8
# author: Maven
# datetime: 15 May 2012
import json
from baseProcessor import BaseProcessor

class UserProcessor(BaseProcessor):
  
  def objectByPK(self, id, **kwargs):
    dbAdapter = self.instanceByName('database_handler')
    data = dbAdapter.userShow(id, 2, None)
    return json.dumps(data,ensure_ascii = True, encoding='utf8')

