'''认证程序.'''
import os
# from ftp.core.db_handler import *
#
# db_obj = DB()

class Auth(object):
    def __init__(self, db_obj):
        self.db = db_obj

    def auth(self, account, password):
        '''认证用户'''
        fileNameList = self.db.get_fileNamesList('auth')
        if account in fileNameList:
            #用户名存在
            relative = 'auth/' + account
            data = self.db.get_fileDate(relative)
            if password == data['password']:
                #密码正确
                return True
            else:
                #密码不正确
                return False
        else:
            #用户名不存在
            return False

# a = Auth(db_obj)
#
# print(a.auth('46ab452aa4ead12eacb118b92c319241', '91b569e1f83ae10085ec4624bd2a7165'))
