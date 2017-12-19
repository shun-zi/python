'''服务端程序'''
from ftp.core.logger import Logger
from creat_role import CreateRole
from db_handler import DB
from auth import Auth
import socketserver
import hashlib
import time
import json
import os

db_obj = DB()
md5 = hashlib.md5()
login = False

#创建日志
logger = Logger('ftpServer')
logger.create_logger()
logger.create_file_handler()
logger.create_console_handler()
logger = logger.logger

class FtpHandler(socketserver.BaseRequestHandler):
    '''ftp服务端'''

    def show_progress_bar(self, receivedSize, contentSzie):
        '''显示进度条'''
        schedule = receivedSize/float(contentSzie) * 100
        return schedule

    def receive_oversize_content(self, contentSize):
        '''一次性接受完服务端发送过来的内容.'''
        receivedContent = ''
        receivedContentBytes = b''
        print(contentSize)
        while len(receivedContent) < contentSize and len(receivedContentBytes) < contentSize:
            minus = contentSize- len(receivedContentBytes)
            if minus >= 10240:
                content = self.request.recv(10240)
            else:
                content = self.request.recv(minus)
            try:
                data = content.decode()
                receivedContent += data
                schedule = self.show_progress_bar(len(receivedContent), contentSize)
            except UnicodeDecodeError:
                data = content
                receivedContentBytes += data
                schedule = self.show_progress_bar(len(receivedContentBytes), contentSize)
            print('schedule:' + str(schedule) + '%')
        else:
            #接收完服务端发送来的内容
            return receivedContent

    def register(self, *args):
        """用户注册"""
        execution_handler = args[1]
        account_client = args[0]['account']
        password_client = args[0]['password']

        # 创建用户
        create_role = CreateRole(db_obj)
        if create_role.create_account(account_client, password_client):
            logger.info('成功创建用户!')
            new = 'True'
            self.request.send(new.encode())
            #防止粘包
            a = self.request.recv(1024)
            execution_handler = '/' + account_client + '>>'
            return execution_handler
        else:
            new = "用户名已经被使用,请重新输用户名和密码."
            self.request.send(new.encode())
            time.sleep(0.5)
            return False


    def login(self, *args):
        '''用户登录'''
        execution_handler = args[1]
        if execution_handler != '>>':
            return execution_handler

        else:
            account_client = args[0]['account']
            password_client = args[0]['password']
            #进行认证
            auth = Auth(db_obj)
            if auth.auth(account_client, password_client):
                new = "True"
                logger.info(account_client + '用户接入')
                self.request.send(new.encode())
                #防止粘包
                a = self.request.recv(1024)
                execution_handler = '/' + account_client + '>>'
                return execution_handler
            else:
                new = "用户名或者密码错误,请重新输入"
                self.request.send(new.encode())
                time.sleep(0.5)
            return False

    def get_file(self, *args):
        '''下载文件'''
        execution_handler = args[1]
        infoDict = args[0]
        if execution_handler == '>>':
            #未登录
            return execution_handler
        else:
            print(1)
            basePath = '/home/shunzi/person/老男孩pratice/day10-异步io-协程-多路复用/ftp/db/accounts/homes'
            currentPath = execution_handler[:-2]
            fileName = infoDict['fileName']

            #得到文件的绝对路径
            accountName = currentPath.split('/')[1]
            absolutePath = basePath + '/' + accountName + '/' + fileName

            if os.path.isfile(absolutePath):
                #文件存在
                fileSize = os.stat(absolutePath).st_size
                self.request.send(str(fileSize).encode())
                new = self.request.recv(1024)
                f = open(absolutePath, 'rb')
                for line in f:
                    self.request.send(line)

                logNew = accountName + '下载了' + fileName
                logger.info(logNew)
                return execution_handler
            else:
                self.request.send('-1'.encode())
                return execution_handler

    def put_file(self, *args):
        '''上传文件'''
        execution_handler = args[1]
        infoDict = args[0]
        if execution_handler == '>>':
            # 未登录
            return execution_handler
        else:
            if infoDict['fileName'] == None:
                #上传文件不存在
                return execution_handler
            else:
                #将文件大小取出来.
                fileSize = infoDict['fileSize']

                #取出用户的磁盘使用情况
                basePath = '/home/shunzi/person/老男孩pratice/day10-异步io-协程-多路复用/ftp/db/accounts/homes'
                currentPath = execution_handler[:-2]
                accountName = currentPath.split('/')[1]
                filePath = 'homes/' + accountName + '/' + accountName
                diskInfo = db_obj.get_fileDate(filePath)

                availableSize = diskInfo['availableSize'] * 1024 * 1024

                if availableSize >= fileSize:
                    self.request.send('1'.encode())

                    #接受上传文件内容,并将文件内容写入文件中.
                    storePath = basePath + '/' + accountName + '/' + infoDict['fileName']
                    receivedSize = 0
                    f = open(storePath, 'wb')

                    while receivedSize < fileSize:
                        data = self.request.recv(10240)
                        f.write(data)
                        receivedSize += len(data)
                        #读取进度并将进度返回给用户
                        schedule = self.show_progress_bar(receivedSize, fileSize)
                        schedule = round(schedule, 3)
                        self.request.send(str(schedule).encode())

                    else:
                        f.close()
                    logNew = accountName + '上传了' + infoDict['fileName']
                    logger.info(logNew)
                    return execution_handler

                else:
                    #可用空间不足
                    self.request.send('-1'.encode())
                    return execution_handler

    def cd(self, *args):
        '''切换目录'''
        infoDict = args[0]
        execution_handler = args[1]

        if execution_handler == '>>':
            #未登录
            return execution_handler
        else:
            #设置路径
            basePath = '/home/shunzi/person/老男孩pratice/day10-异步io-协程-多路复用/ftp/db/accounts/homes'
            currentPath = execution_handler[:-2]
            if infoDict['path'] != None:
                #含有执行内容

                if infoDict['path'] != '..':
                    #cd 'path'
                    #检查执行路径是否存在
                    absolutePath = basePath + infoDict['path']
                    a = os.path.isdir(absolutePath)
                    if a:
                        if infoDict['path'][-1] == '/':
                            infoDict['path'] = infoDict['path'].rstrip('/')
                        os.chdir(absolutePath)
                        #返回执行句柄
                        execution_handler = infoDict['path'] + '>>'
                        self.request.send('1'.encode())
                        return execution_handler

                    else:
                        absolutePath = basePath + currentPath + '/' + infoDict['path']
                        a = os.path.isdir(absolutePath)
                        if a:
                            os.chdir(absolutePath)
                            #返回执行句柄
                            execution_handler = currentPath + '/' + infoDict['path'] + '>>'
                            self.request.send('1'.encode())
                            return execution_handler

                        else:
                            new = infoDict['path'] + ':该路径不存在'
                            logger.error(new)
                            self.request.send(new.encode())
                            return execution_handler
                else:
                    #cd ..
                    pathList = currentPath.split('/')
                    if len(pathList) == 2:
                        #当前路径是主目录
                        self.request.send('1'.encode())
                        return  execution_handler

                    else:
                        #当前路径不是主目录
                        pathList = pathList[:-2]
                        currentPath = ''
                        for item in pathList:
                            if item == '':
                                item = '/'
                            currentPath += item
                        execution_handler = currentPath + '>>'
                        self.request.send('1'.encode())
                        return execution_handler

            else:
                #cd ''
                pathList = currentPath.split('/')
                execution_handler = '/' + pathList[1] + '>>'
                self.request.send('1'.encode())
                return execution_handler

    def ls(self, *args):
        '''查看当前目录'''
        execution_handler = args[1]

        if execution_handler == '>>':
            #未登录
            return execution_handler
        else:
            infoDict = args[0]
            basePath = '/home/shunzi/person/老男孩pratice/day10-异步io-协程-多路复用/ftp/db/accounts/homes'
            currentPath = execution_handler[:-2]
            #字典参数进行分类处理
            if infoDict['content'] == None:
                #ls ''

                #执行"ls '完整路径'"命令
                absolutePath = basePath + currentPath
                cmd = infoDict['action'] + ' ' + absolutePath
                cmd_content = os.popen(cmd).read()

                #计算得到内容的大小,告知客户端.
                self.request.send(str(len(cmd_content)).encode())

                #等待到客户端的发送请求,然后一次性发送得到的内容.
                self.request.recv(1024)
                logger.info('开始发送...')
                self.request.sendall(cmd_content.encode())
                return execution_handler

            else:
                #ls 'content'

                #将基本路径和相对路径拼接成一个完整的路径,然后检查该路径是否存在.
                absolutePath = basePath + infoDict['content']
                if os.path.isdir(absolutePath):
                    cmd = infoDict['action'] + ' ' + absolutePath
                    cmd_content = os.popen(cmd).read()

                    # 计算得到内容的大小,告知客户端.
                    self.request.send(str(len(cmd_content)).encode())

                    # 等待到客户端的发送请求,然后一次性发送得到的内容.
                    self.request.recv(1024)
                    logger.info('开始发送...')
                    self.request.sendall(cmd_content.encode())
                    return execution_handler
                else:
                    #路径不存在
                    self.request.send('-1'.encode())
                    return execution_handler


    def handle(self):
        '''与客户端的主交互程序'''
        logger.info("新用户接入")
        #设置执行句柄
        execution_handler = '>>'
        #接受客户端的操作,并对其进行解析,调用对应的方法
        while True:
            if execution_handler != False:
                #执行相应操作成功
                time.sleep(0.5)
                self.request.send(execution_handler.encode())
                infoDict = json.loads(self.request.recv(1024).decode())
            else:
                time.sleep(0.5)
                execution_handler = '>>'
                infoDict = json.loads(self.request.recv(1024).decode())

            cmd = infoDict['action']
            if cmd == 'logout':
                logger.info('用户关闭连接')
                break
            else:
                func = getattr(self, cmd)
                execution_handler = func(infoDict, execution_handler)







if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9999
    server = socketserver.ThreadingTCPServer((HOST, PORT), FtpHandler)
    server.serve_forever(poll_interval=10)

