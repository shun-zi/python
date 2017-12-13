'''有关服务器的全部操作.'''
import queue
import paramiko

#创建队列对象,用来存储执行结果
q = queue.Queue()

class Server(object):
    def __init__(self):
        self.exec_queue = q

    def exec_command(self, ssh, command):
        '''执行命令'''
        # try:
        stdin, stdout, stderr = ssh.exec_command(command)
        exe_dict = {'stdout': stdout, 'stderr': stderr}
        q.put(item=exe_dict)
        # except Exception as e:
        #     print(e)

    def transport(self, transport, exec_operator, fileName1, fileName2):
        '''在本地和主机之间执行传输请求'''
        try:
            sftp = paramiko.SFTPClient.from_transport(transport)
            operator = getattr(sftp, exec_operator)
            operator(fileName1, fileName2)
        except Exception as e:
            print(e)



# transport1 = paramiko.Transport(('192.168.1.105', 22))
# transport1.connect(username='fzm', password='w1w2w3w4')
# server = Server()
# # sftp = paramiko.SFTPClient.from_transport(transport1)
# server.transport(transport1, 'put', '/home/shunzi/heheh', '/tmp/shunzi.txt')