from ftp.conf import settings
import logging

# logging.basicConfig(filename=setting.LOG_TYPES['operator'], level=setting.LOG_LEVEL,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
#
# logging.debug('This message should go to the log file')
# logging.info('So should this')
# logging.warning('And this, too')

# create logger
# logger = logging.getLogger('TEST-LOG')
# logger.setLevel(logging.DEBUG)
#
# # create console handler and set level to debug
# ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)
#
# # create file handler and set level to warning
# fh = logging.FileHandler("/home/shunzi/person/老男孩pratice/day8/ftp/log/operator.log")
# fh.setLevel(logging.WARNING)
# # create formatter
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#
# # add formatter to ch and fh
# ch.setFormatter(formatter)
# fh.setFormatter(formatter)
#
# # add ch and fh to logger
# logger.addHandler(ch)
# logger.addHandler(fh)
#
# # 'application' code
# logger.debug('debug message')
# logger.info('info message')
# logger.warn('warn message')
# logger.error('error message')
# logger.critical('critical message')

import hashlib
import os
class FtpClient(object):
    '''ftp客户端'''
    def __init__(self):
        pass
    def help(self):
        '''
        login
        register
        ls
        cd
        get_file
        put_file
        :return:
        '''
    def connect(self):
        '''连接服务端'''
        client = socket.socket()
        client.connect((self.ipAddress, self.port))
        return client

    def login(self):
        '''登录'''
        pass

    def register(self):
        '''注册'''
        pass

    def get_file(self):
        '''下载文件'''
        pass

    def put_file(self):
        '''上传文件'''
        pass

    def cd(self):
        '''切换目录'''
        pass

    def show_progress_bar(self):
        '''显示进度条'''
        pass

    def ls(self):
        '''查看当前目录'''
        pass

    def interrctive_with_server(self):
        '''与服务器的主交互'''
        # 创建日志

        #输入命令
        cmd = input('>>').strip()
        if hasattr(self, cmd):
            print(1)
        # # 选择操作
        # operator = client.recv(1024)
        # print(operator.decode())
        # index = input("请输入数字来选择相对应的操作:")
        # client.send(index.encode())


# a = FtpClient()
# a.interrctive_with_server()
# a = os.popen("cd '/home/shunzi/person/老男孩pratice/day8/ftp/db/accounts/dasds'").read()
# a = '/1/'
# print(a.split('/')[:-2])
# a = 'djasljdlsl'
# print(a)



# os.chdir('/home/shunzi/person/老男孩pratice/day8/ftp/core')
# /home/shunzi/person/老男孩pratice/day8/ftp/db/accounts/homes/shunzi/hhehe