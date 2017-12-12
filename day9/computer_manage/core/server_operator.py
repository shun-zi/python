'''有关服务器的全部操作.'''

class Server(object):
    def __init__(self):
        pass

    def exec_command(self, ssh, command):
        '''执行命令'''
        stdin, stdout, stderr = ssh.exec_command(command)
        exe_dict = {'stdin': stdin, 'stdout': stdout, 'stderr': stderr}
        return exe_dict

    def transport(self, transport, exec_operator, fileName1, fileName2):
        '''在本地和主机之间执行传输请求'''
        operator = getattr(transport, exec_operator)
        operator(fileName1, fileName2)

