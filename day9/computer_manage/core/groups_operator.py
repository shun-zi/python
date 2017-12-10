'''有关小组的全部操作.'''
# 添加系统环境变量
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import paramiko
import db_handler


db_obj = DB()

class Group(object):
    def __init__(self, db_obj):
        self.db = db_obj

    def connect_computer(self, hostname, port, username, password):
        '''如果指定主机能连上则返回True'''
        ssh = paramiko.SSHClient()

        try:
            ssh.connect(hostname=hostname, port=port, username=username, password=paramiko)
            return True
        except:
            print('out log info')
            return False



    def add_computer(self):
        '''添加主机到分组中'''
        pass

    def show_group(self):
        '''显示分组'''
        pass

    def show_computers_for_group(self):
        '''查看指定小组的主机列表'''
        pass