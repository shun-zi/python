import paramiko
# from computer_manage.core.server_operator import *



# ssh = paramiko.SSHClient()
#
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#
# ssh.connect(hostname='192.168.1.103', port=22, username='test2', password='z960520@')
# # 在连接上的服务器执行命令并返回相应内容.
# stdin, stdout, stderr = ssh.exec_command('df')
#
# result = stderr.read()
# print(result.decode())
# print(stderr.read().decode())
# ssh.close()

# try:
#     print('1' + 1)
# except:
#
#     print(2)


# #对远程服务器进行文件传输的动作.
# transport1 = paramiko.Transport(('192.168.1.105', 22))
# transport1.connect(username='fzm', password='w1w2w3w4')
# # server = Server()
# sftp = paramiko.SFTPClient.from_transport(transport1)
# # 将heheh文件上传至服务器/tmp/shunzi.txt
# sftp.put('/home/shunzi/heheh', '/tmp/shunzi.txt')
# # server.transport(sftp, 'get', '/home/shunzi/heheh', '/tmp/shunzi.txt')
# # 将服务器上的shunzi文件下载至本机/home/shunzi/shunzi.txt
# # sftp.get('/home/fzm/shunzi', '/shunzi/shunzi.txt')
# transport1.close()

import time
import threading


# def run(n):
#     print('[%s]------running----\n' % n)
#     time.sleep(2)
#     return 1
#     print('--done--')
#
#
# def main():
#     for i in range(5):
#         t = threading.Thread(target=run, args=[i, ])
#         print(t.get())
#         t.start()
#         t.join(1)
#
#
# main()

class Foo(object):
    def __init__(self):
        self.name = 'wupeiqi'

    def hehe(self,s,a):
        print(a)
        print(s)

    def func(self, a, s):
        self.hehe(s, a)


obj = Foo()

# # #### 检查是否含有成员 ####
# hasattr(obj, 'name')
# hasattr(obj, 'func')

# #### 获取成员 ####
a = getattr(obj, 'name')
b = getattr(obj, 'func')
print(a)
print(b)
