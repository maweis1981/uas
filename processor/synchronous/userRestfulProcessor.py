#!/usr/bin/env python
# encoding: utf-8
# author: maven
# datetime: 23 May 2012


from baseProcessor import BaseProcessor

class UserProcessor(BaseProcessor):

    def __init__(self):
        self.da = self.instanceByName('database_handler')

    # load user data
    def getUserDataById(self,id):
        return self.da.userBaseData(id)

    def getUserFullDataById(self,id):
        return da.userFullData(id)

    # lookup user
    def searchUserData(self,attribute):
        return da.userLookup(attribute)

    # load user's contacts
    def getContacts(self,id,param):
        return self.da.userContacts(id,param)

    def getInContacts(self,id,param):
        return self.da.userInContacts(id, param)

    def getUserApps(self,id,param):
        return self.da.userApps(id,param)
