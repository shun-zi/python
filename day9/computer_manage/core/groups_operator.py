'''有关小组的全部操作.'''
# 添加系统环境变量
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import paramiko
# import db_handler
from computer_manage.core.db_handler import *

db_obj = DB()

class Group(object):
    def __init__(self, db_obj, logger_dbj=None, memberNumber=2):
        self.db = db_obj
        self.logger = logger_dbj
        self.memberNumber = memberNumber

    def connect_computer(self, hostname, port, username, password):
        '''如果指定主机能连上则返回True'''
        ssh = paramiko.SSHClient()

        try:
            ssh.connect(hostname=hostname, port=port, username=username, password=paramiko)
            return ssh
        except:
            new = hostname + ':连接失败'
            self.logger.warn(new)
            return False

    def transport_connect(self, hostname, port, username, password):
        '''对主机进行传输连接'''
        try:
            transport = paramiko.Transport((hostname, port))
            transport.connect(username=username, password=password)
            return transport
        except:
            new = hostname + ':连接失败'
            self.logger.warn(new)
            return False

    def add_computer(self, hostname, port, username, password):
        '''添加主机到分组中'''
        ssh = self.connect_computer(hostname, port, username, password)
        if ssh != False:
            groupsRelativePath = 'computers'
            #将全部的分组号取出存储到一个列表中.
            groups_list = db_obj.get_fileNamesList(groupsRelativePath)
            if len(groups_list) == 0:
                #分组列表为空.则新建一个分组文件夹,并将新添加的主机信息存储到该目录下.
                newGroupRelativePath = groupsRelativePath + '/1'
                db_obj.makedir(newGroupRelativePath)

                computerRelativePath = newGroupRelativePath + '/' + username
                data = {'hostname': hostname, 'port': port, 'username': username,
                        'password': password}
                db_obj.store_data(computerRelativePath, data)
            else:
                #出列表中最后一个文件名,判断其目录下的文件个数
                last_groupId = groups_list[-1]
                groupRelativePath = groupsRelativePath + '/' + last_groupId
                computersList = db_obj.get_fileNamesList(groupRelativePath)

                if len(computersList) < self.memberNumber:
                    #添加的主机信息存储到该目录下.
                    computerRelativePath = groupRelativePath + '/' + username
                    data = {'hostname': hostname, 'port': port, 'username': username,
                            'password': password}
                    db_obj.store_data(computerRelativePath, data=data)
                else:
                    #分组下的主机数已满,新建一个新的分组文件夹.
                    last_groupId = str(int(last_groupId) + 1)
                    groupRelativePath = groupsRelativePath + '/' + last_groupId
                    db_obj.makedir(groupRelativePath)

                    #将新添加的主机信息存储到该目录下
                    computerRelativePath = groupRelativePath + '/' + username
                    data = {'hostname': hostname, 'port': port, 'username': username,
                           'password': password}
                    db_obj.store_data(computerRelativePath, data=data)
        else:
            pass


    def show_group(self):
        '''显示分组'''
        #将computers的目录下的文件名取出放到一个列表中.
        groupsRelativePath = 'computers'
        groupsList = db_obj.get_fileNamesList(groupsRelativePath)

        print('**************************')
        print('         分组列表:         ')
        for groupId in groupsList:
            print(groupId)
        print('**************************')


    def show_computers_for_group(self, groupId):
        '''查看指定小组的主机列表'''
        computersRelativePath = 'computers/' + groupId
        computersList = db_obj.get_fileNamesList(computersRelativePath)

        print('**************************')
        print('          主机列表         ')
        for username in computersList:
            print(username)
        print('**************************')
