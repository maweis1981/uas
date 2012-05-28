#!/usr/bin/env python
# encoding: utf-8
# author: maven
# datetime: 23 May 2012


from baseProcessor import BaseProcessor

class UserProcessor(BaseProcessor):

    # load user data
    def getUserDataById(self,id):
        da = self.instanceByName('database_handler')
        return da.userFullData(id)
    # lookup user
    def searchUserData(self,attribute):
        da = self.instanceByName('database_handler')
        return da.userLookup(attribute)

    # load user's contacts
    def getContacts(self,id):
        da = self.instanceByName('database_handler')
        return da.***()


