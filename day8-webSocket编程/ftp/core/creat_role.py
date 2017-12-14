'''创建相关角色程序'''
# from ftp.core.db_handler import *
#
# db_obj = DB()

class CreateRole(object):
    def __init__(self, db_obj):
        self.db = db_obj

    def create_account(self, account, password):
        '''创建用户'''
        #匹配文件名,检查用户是否存在.
        accountFileList = self.db.get_fileNamesList('auth')
        if account in accountFileList:
            # 用户名已经存在
            return False
        else:
            # 用户名还未创建,将该用户的数据放进文件系统的一个文件中.
            relativePath = 'auth/' + account
            data = {'account': account, 'password': password}
            self.db.store_data(relativePath, data)

            #为用户创建主目录
            relativePath = 'homes/' + account
            self.db.makedir(relativePath)


            #为用户分配可用空间.
            relativePath += '/' + account
            data = {'diskSize': 5000, 'unit': 'MB', 'usedSize': 0}
            data['availableSize'] = data['diskSize'] - data['usedSize']
            self.db.store_data(relativePath, data)
            return True

# a = CreateRole(db_obj)
#
# a.create_account('shunzi', '960520')
