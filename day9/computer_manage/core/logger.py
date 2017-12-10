'''创建logger类'''
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import logging
from conf import setting

class Logger(object):

    def __init__(self, loggerName=None, logger_dbj=None):
        self.name = loggerName
        self.logger = logger_dbj

    def create_logger(self, level=logging.DEBUG):
        '''创建logger对象'''
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(level)

    def set_formatter(self, formatterStr):
        '''设置日志格式'''
        formatter = logging.Formatter(formatterStr)
        return formatter


    def create_console_handler(self, level=logging.DEBUG, formatterStr=None):
        '''创建控制台handler'''
        #创建控制台handler对象
        ch = logging.StreamHandler()
        ch.setLevel(level)

        #设置日志格式
        formatter = self.set_formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)

        #将设置好的handler加入logger
        self.logger.addHandler(ch)

    def create_file_handler(self, level=logging.DEBUG, formatterStr=None):
        '''创建文件handler'''
        #创建文件handler对象
        fh = logging.FileHandler(setting.LOG_TYPES['operator'])
        fh.setLevel(setting.LOG_LEVEL)

        # 设置日志格式
        formatter = self.set_formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)

        # 将设置好的handler加入logger
        self.logger.addHandler(fh)
