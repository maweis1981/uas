#!/usr/bin/env python
# encoding: utf-8
# author: maven
# datetime: 23 May 2012


from baseProcessor import BaseProcessor

class UserProcessor(BaseProcessor):

    def getUserDataById(self,id):
        da = self.instanceByName('database_handler')
        return da.userData(id)
