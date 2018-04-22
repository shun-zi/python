'''创建logger程序'''
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import logging
from conf import setting

def create_logger(loggerName):
    '''创建一个完整的logger'''
    #创建logger
    logger = logging.getLogger(loggerName)
    logger.setLevel(logging.DEBUG)

    #创建控制台handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    #创建文件handler
    fh = logging.FileHandler(setting.LOG_TYPES['operator'])
    fh.setLevel(setting.LOG_LEVEL)

    #设置输出格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    #将设置好的格式加入handler中
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    #将设置好的handler加入到logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger

