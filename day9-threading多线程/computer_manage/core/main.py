'''主逻辑交互的主程序.'''
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import logging
from computer_manage.core.groups_operator import *
from computer_manage.core.db_handler import *
from computer_manage.core.logger import *
from computer_manage.conf.settings import *

#创建logger对象
loggerName = 'manage computer'
logger = Logger(loggerName)
logger.create_logger(LOG_LEVEL)
# logger.create_console_handler(logging.DEBUG)
logger.create_file_handler(LOG_LEVEL)

#创建DB对象
db_obj = DB()

#创建Group对象
group = Group(db_obj=db_obj, logger_dbj=logger.logger)

while True:
    print('*******************')
    print('      功能列表      ')
    print('1.添加主机')
    print('2.显示分组')
    print('0.退出')
    print('*******************')
    fun_index = int(input("请输入你要进行的操作的索引:"))

    if fun_index == 0:
        logger.logger.info('退出系统')
        break

    elif fun_index == 1:
        #添加主机
        hostname = input('请输入ip地址:')
        port = int(input('请输入端口:'))
        username = input('请输入主机名:')
        password = input('请输入主机密码:')

        ssh = group.add_computer(hostname, port, username, password)
        if ssh != False:
            print('添加成功')
        else:
            print('添加失败')
    elif fun_index == 2:
        #显示分组
        try:
            group.show_group()
            groupId = input('请指定分组:')
            group.show_computers_for_group(groupId=groupId)
        except FileNotFoundError as e:
            print(e)

        while True:
            #显示功能
            print('*******************')
            print('      功能列表      ')
            print('1.执行命令')
            print('2.传输文件')
            print('0.退出')
            print('*******************')

            operator_index = int(input("请输入你要进行的操作的索引:"))
            try:
                if operator_index == 0:
                    break
                elif operator_index == 1:
                    group.batch_execution_command(groupId)
                elif operator_index == 2:
                    group.batch_transport_file(groupId)
            except FileNotFoundError as e:
                print(e)
