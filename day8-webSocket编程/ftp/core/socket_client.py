'''客户端程序'''
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import socket
import hashlib
import json
import time

from logger import create_logger
from db_handler import DB


db_obj = DB()
md5 = hashlib.md5()


class FtpClient(object):
    '''ftp客户端'''
    def __init__(self, ipAddress, port):
        self.ipAddress = ipAddress
        self.port = port
        self.client = None

    def show_progress_bar(self, receivedSize, contentSzie):
        '''显示进度条'''
        schedule = receivedSize/ float(contentSzie) * 100
        schedule = round(schedule, 3)
        return schedule

    def logout(self, *args):
        '''退出'''
        cmd = args[0].split()[0]
        infoDict = {
            'action': cmd
        }
        print(json.dumps(infoDict).encode())
        self.client.send(json.dumps(infoDict).encode())
        # self.client.close()
        return True

    def connect(self):
        '''连接服务端'''
        client = socket.socket()
        client.connect((self.ipAddress, self.port))
        return client

    def login(self, *args):
        '''登录'''
        #将命令读取出来
        cmd = args[0].split()[0]
        execution_handler = args[1]
        if execution_handler != '>>':
            #用户已经登录
            infoDict = {
                'action': cmd
            }
            print('你已经登录过了')
            self.client.send(json.dumps(infoDict).encode())

        else:
            while 1:
                account = input('请输入用户名:')
                # md5.update(account.encode())
                # account_lock = md5.hexdigest()
                password = input('请输入密码:')
                # md5.update(password.encode())
                # password_lock = md5.hexdigest()
                infoDict = {
                    'action': cmd,
                    'account': account,
                    'password': password
                }
                print(infoDict)
                self.client.send(json.dumps(infoDict).encode())

                #接受服务端的消息
                new = self.client.recv(1024).decode()
                # print(1)
                if new == 'True':
                    print('成功登录.')
                    self.client.send('1'.encode())
                    break
                else:
                    print(new)

    def register(self, *args):
        '''注册'''
        cmd = args[0].split()[0]

        while 1:
            account = input('请输入用户名:')
            # md5.update(account.encode())
            # account_lock = md5.hexdigest()
            password = input('请输入密码:')
            # md5.update(password.encode())
            # password_lock = md5.hexdigest()
            infoDict = {
                'action': cmd,
                'account': account,
                'password': password
            }
            self.client.send(json.dumps(infoDict).encode())
            new = self.client.recv(1024)
            if new.decode() == 'True':
                print("注册成功")
                self.client.send('1'.encode())
                break
            else:
                print(new.decode())

    def get_file(self, *args):
        '''下载文件'''

        execution_handler = args[1]
        list = args[0].split(' ',1)
        cmd = list[0]
        if execution_handler == ">>":
            # 未登录.
            infoDict = {
                'action': cmd,
                'fileName': None
            }
            self.client.send(json.dumps(infoDict).encode())
            print('未登录,请先进行登录.')

        else:
            if len(list) == 1:
                #文件名为空
                infoDict = {
                    'action': cmd,
                    'fileName': None
                }
                self.client.send(json.dumps(infoDict).encode())
            elif len(list) == 2:
                filename = list[1]
                infoDict = {
                    'action': cmd,
                    'fileName': filename
                }
                self.client.send(json.dumps(infoDict).encode())

            fileSize = int(self.client.recv(1024).decode())

            if fileSize == -1:
                print('输入文件不存在.')

            else:
                self.client.send('开始发送文件...'.encode())

                #接收文件内容并将文件内容放入文件中.
                receivedSize = 0
                f = open(filename, 'wb')

                while receivedSize < fileSize:
                    data = self.client.recv(10240)
                    f.write(data)
                    receivedSize += len(data)
                    schedule = self.show_progress_bar(receivedSize, fileSize)
                    print('process bar:' + str(schedule) + '%')

                else:
                    print('ok')
                    f.close()

                # #将文件内容写入到一个文件中.
                # filePath = '/home/shunzi/person/老男孩pratice/day8/ftp/core/file' + '/' + filename
                # with open(filePath, 'wb') as f:
                #     f.write(receivedContent)

    def put_file(self, *args):
        '''上传文件'''
        execution_handler = args[1]
        list = args[0].split(' ', 1)
        cmd = list[0]
        if execution_handler == ">>":
            # 未登录.
            infoDict = {
                'action': cmd,
                'fileName': None,
                'fileSize': 0
            }
            self.client.send(json.dumps(infoDict).encode())
            print('未登录,请先进行登录.')

        else:
            currentPath = os.path.dirname(os.path.abspath(__file__))
            if len(list) == 1:
                # 文件名为空
                infoDict = {
                    'action': cmd,
                    'fileName': None,
                    'fileSize': 0
                }
                self.client.send(json.dumps(infoDict).encode())
                print('文件不存在.')

            elif len(list) == 2:
                fileName = list[1]
                fileAbsolutePath = currentPath + '/file/' + fileName

                if os.path.isfile(fileAbsolutePath):
                    #文件名存在

                    #将文件内容取出来并计算大小.
                    f = open(fileAbsolutePath, 'rb')
                    # content = f.read()
                    contetnSize = os.stat(fileAbsolutePath).st_size

                    infoDict = {
                        'action': cmd,
                        'fileName': fileName,
                        'fileSize': contetnSize
                    }
                    self.client.send(json.dumps(infoDict).encode())
                    new = int(self.client.recv(1024).decode())
                    if new == -1:
                        print('可用空间不足')
                    else:
                        #接收到服务端的上传请求

                        #将文件内容上传给服务器.
                        for line in f:
                            self.client.send(line)
                            schedule = self.client.recv(1024).decode()
                            print('process bar:' + schedule + '%')

                else:
                    infoDict = {
                        'action': cmd,
                        'fileName': None,
                        'fileSize': 0
                    }
                    self.client.send(json.dumps(infoDict).encode())
                    print('文件名不存在.')

    def cd(self, *args):
        '''切换目录'''
        execution_handler = args[1]
        list = args[0].split()
        cmd = list[0]
        if execution_handler == ">>":
            #未登录.
            infoDict = {
                'action': cmd,
                'path': None
            }
            self.client.send(json.dumps(infoDict).encode())
            print('未登录,请先进行登录.')

        else:
            if len(list) == 1:
                #cd ''
                infoDict = {
                    'action': cmd,
                    'path': None
                }
            else:
                #cd .. 或者 cd 'path'
                path = list[1]
                infoDict = {
                    'action': cmd,
                    'path': path
                }
            self.client.send(json.dumps(infoDict).encode())

            new = self.client.recv(1024).decode()
            if new != '1':
                print(new)

    def ls(self, *args):
        '''查看当前目录'''
        execution_handler = args[1]
        operator = args[0].split()
        cmd = operator[0]

        if execution_handler == '>>':
            infoDict = {
                'action': cmd,
                'content': None
            }
            self.client.send(json.dumps(infoDict).encode())
            print('未登录')
        else:
            # 将执行语句拆分成执行命令和路径两部分,将其编写成json序列化对象,然后传给服务端.
            if len(operator) == 1:
                #ls '':
                infoDict = {
                    'action': cmd,
                    'content': None
                }
                self.client.send(json.dumps(infoDict).encode())
            elif len(operator) == 2:
                # ls 'content':
                content = operator[1]
                infoDict = {
                    'action': cmd,
                    'content': content
                }
                self.client.send(json.dumps(infoDict).encode())

            # 接受到服务端发回来的执行内容字节大小
            contentSize = int(self.client.recv(1024).decode())
            if contentSize == -1:
                new = content + ':该路径不存在'
                print(new)
            else:
                self.client.send('请开始发送内容.'.encode())
                receivedSize = 0
                receivedContent = ''
                while receivedSize < contentSize:
                    data = self.client.recv(1024).decode()
                    receivedSize += len(data)
                    receivedContent += data
                else:
                    print(receivedContent)

    def interrctive_with_server(self):
        '''与服务器的主交互'''
        # 创建日志
        logger = create_logger('ftpClient')

        #连接服务端
        self.client = self.connect()


        #输入命令
        while 1:
            execution_handler = self.client.recv(1024).decode()
            operator = input(execution_handler).strip()
            if len(operator) < 1:
                continue

            cmd = operator.split()[0]
            if hasattr(self, cmd):
                '''self.'cmd'存在,调用就行'''
                func = getattr(self, cmd)
                func(operator, execution_handler)

                if cmd == 'logout':
                    break

            else:
                print("Ftp200")

    def help(self):
        '''
        login
        register
        ls
        cd ..
        get_file filename
        put_file  filename
        :return:

        标准码:Ftp200:方法不存在.
        '''



ftpClinet = FtpClient('localhost', 9998)
ftpClinet.interrctive_with_server()






