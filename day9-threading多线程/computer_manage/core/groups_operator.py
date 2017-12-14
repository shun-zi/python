'''有关小组的全部操作.'''
# 添加系统环境变量
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import paramiko
import threading
import time
# import db_handler
from computer_manage.core.db_handler import *
from computer_manage.core.server_operator import *

db_obj = DB()
server_obj = Server()

class Group(object):
    def __init__(self, db_obj, logger_dbj=None, memberNumber=2):
        self.db = db_obj
        self.logger = logger_dbj
        self.memberNumber = memberNumber

    def connect_computer(self, hostname, port, username, password):
        '''如果指定主机能连上则返回True'''
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh.connect(hostname=hostname, port=port, username=username, password=password)
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
        try:
            #只检查文件的异常
            if ssh != False:
                groupsRelativePath = 'computers'
                #将全部的分组号取出存储到一个列表中.
                groups_list = self.db.get_fileNamesList(groupsRelativePath)
                if len(groups_list) == 0:
                    #分组列表为空.则新建一个分组文件夹,并将新添加的主机信息存储到该目录下.
                    newGroupRelativePath = groupsRelativePath + '/1'
                    self.db.makedir(newGroupRelativePath)

                    computerRelativePath = newGroupRelativePath + '/' + username
                    data = {'hostname': hostname, 'port': port, 'username': username,
                            'password': password}
                    self.db.store_data(computerRelativePath, data)
                    return True
                else:
                    #出列表中最后一个文件名,判断其目录下的文件个数
                    last_groupId = groups_list[-1]
                    groupRelativePath = groupsRelativePath + '/' + last_groupId
                    computersList = self.db.get_fileNamesList(groupRelativePath)

                    if len(computersList) < self.memberNumber:
                        #添加的主机信息存储到该目录下.
                        computerRelativePath = groupRelativePath + '/' + username
                        data = {'hostname': hostname, 'port': port, 'username': username,
                                'password': password}
                        self.db.store_data(computerRelativePath, data=data)
                        return True
                    else:
                        #分组下的主机数已满,新建一个新的分组文件夹.
                        last_groupId = str(int(last_groupId) + 1)
                        groupRelativePath = groupsRelativePath + '/' + last_groupId
                        self.db.makedir(groupRelativePath)

                        #将新添加的主机信息存储到该目录下
                        computerRelativePath = groupRelativePath + '/' + username
                        data = {'hostname': hostname, 'port': port, 'username': username,
                               'password': password}
                        self.db.store_data(computerRelativePath, data=data)
                        return True
            else:
                return False
        except FileNotFoundError as e:
            print(e)
            return False


    def show_group(self):
        '''显示分组'''
        #将computers的目录下的文件名取出放到一个列表中.
        groupsRelativePath = 'computers'
        groupsList = self.db.get_fileNamesList(groupsRelativePath)
        print('**************************')
        print('         分组列表:         ')
        for groupId in groupsList:
            print(groupId)
        print('**************************')


    def show_computers_for_group(self, groupId):
        '''查看指定小组的主机列表'''
        computersRelativePath = 'computers/' + groupId
        computersList = self.db.get_fileNamesList(computersRelativePath)

        print('**************************')
        print('          主机列表         ')
        for username in computersList:
            print(username)
        print('**************************')

    def batch_execution_command(self, groupId):
        '''批量执行命令'''
        computersRelativePath = 'computers/' + groupId
        computersList = self.db.get_fileNamesList(computersRelativePath)

        if len(computersList) == 0:
            #分组为空
            self.logger.warn('分组为空, 请重新指定分组.')
            return False
        else:
            #连接组里的全部主机
            computersStatus = {}
            for computer in computersList:
                computerRelativePath = computersRelativePath + '/' + computer
                data = self.db.get_fileDate(computerRelativePath)

                #连接主机,并将主机和连接状态放到字典中.
                ssh = self.connect_computer(data['hostname'] , data['port'], data['username'], data['password'])
                computersStatus[computer] = ssh
            exec_command = ''
            while True:
                exec_command = input("请输入批量执行的命令:")
                if exec_command == 'exit':
                    print('退出该功能')
                    break
                #遍历字典,给连接上的主机执行命令.
                for computer, ssh in computersStatus.items():
                    if ssh != False:
                        try:
                            t = threading.Thread(target=server_obj.exec_command, args=[ssh, exec_command,])
                            t.start()
                            result = server_obj.exec_queue.get()
                            # dict = {computer: {'stdout':result['stdout'].read().decode(), 'stderr':result['stderr'].read().decode()}}
                            print(computer + ':')
                            print('stdout:' + result['stdout'].read().decode())
                            print('stderr:' + result['stderr'].read().decode())
                            ssh.close()
                        except:
                            self.logger('该命令执行错误')
                while threading.active_count() != 1:
                    #等待所有子线程进行完成
                    time.sleep(1)


    def batch_transport_file(self, groupId):
        '''批量发送文件.'''
        computersRelativePath = 'computers/' + groupId
        computersList = self.db.get_fileNamesList(computersRelativePath)

        if len(computersList) == 0:
            # 分组为空
            self.logger.warn('分组为空, 请重新指定分组.')
            return False
        else:
            # 连接组里的全部主机
            computersStatus = {}
            for computer in computersList:
                computerRelativePath = computersRelativePath + '/' + computer
                data = self.db.get_fileDate(computerRelativePath)

                # 连接主机,并将主机和连接状态放到字典中.
                transport = self.transport_connect(data['hostname'], data['port'], data['username'], data['password'])
                computersStatus[computer] = transport
                print(computersStatus)
            while True:
                exec_command = input("请输入批量传输的命令:").split()
                if exec_command[0] == 'exit':
                    break
                fileName1 = exec_command[1]
                fileName2 = exec_command[2]
                exec_command = exec_command[0]

                # 遍历字典,给连接上的主机执行命令.
                for computer, transport in computersStatus.items():
                    if transport != False:
                        if exec_command == 'get':
                            list = fileName1.split('/')
                            username = transport.get_username()
                            list[2] = username
                            fileName1 = ''
                            for item in list:
                                fileName1 += item
                                fileName1 += '/'
                            fileName1 = fileName1[:-1]
                            print(fileName1)
                        try:
                            t = threading.Thread(target=server_obj.transport, args=[transport, exec_command, fileName1, fileName2,])
                            t.start()
                            t.join()
                            self.logger.info('成功传输文件')
                            transport.close()
                        except:
                            self.logger.warn('传输文件失败.')
                while threading.active_count() != 1:
                    #等待所有子线程进行完成
                    time.sleep(1)