'''主逻辑交互的主程序.'''
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import logging
from computer_manage.core.logger import *
from computer_manage.conf.settings import *

#创建logger对象
loggerName = 'manage computer'
logger = Logger(loggerName)
logger.create_logger(LOG_LEVEL)
logger.create_console_handler(logging.DEBUG)
logger.create_file_handler(LOG_LEVEL)


