import paramiko
from computer_manage.core.server_operator import *



# ssh = paramiko.SSHClient()
#
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#
# ssh.connect(hostname='192.168.31.121', port=22, username='fzm', password='w1w2w3w4')

#在连接上的服务器执行命令并返回相应内容.
# stdin, stdout, stderr = ssh.exec_command('df')
#
# result = stdout.read()
# print(result.decode())
# print(stderr.read().decode())
# ssh.close()


#对远程服务器进行文件传输的动作.
transport = paramiko.Transport(('192.168.31.121', 22))
transport.connect(username='fzm', password='w1w2w3w4')
server = Server()
sftp = paramiko.SFTPClient.from_transport(transport1)
#将heheh文件上传至服务器/tmp/shunzi.txt
# sftp.put('/home/shunzi/heheh', '/tmp/shunzi.txt')
server.transport(sftp, 'get', '/home/shunzi/heheh', '/tmp/shunzi.txt')
#将服务器上的shunzi文件下载至本机/home/shunzi/shunzi.txt
# sftp.get('/home/fzm/shunzi', '/home/shunzi/shunzi.txt')
# transport.close()

# class Foo(object):
#
#
#     def __init__(self):
#         self.name = 'wupeiqi'
#
#
#     def func(self):
#         return 'func'
#
#
# obj = Foo()
#
# # #### 检查是否含有成员 ####
# print(hasattr(obj, 'name'))
# print(hasattr(obj, 'func'))
#
# # #### 获取成员 ####
# print(getattr(obj, 'name'))
# a = getattr(obj, 'func')
# print(a())
# # #### 设置成员 ####
# setattr(obj, 'age', 18)
# setattr(obj, 'show', lambda num: num + 1)

# #### 删除成员 ####
delattr(obj, 'name')
delattr(obj, 'func')