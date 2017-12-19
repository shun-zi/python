import os
import sys
import logging
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


DATABASE = {
    'engine': 'file_storage',#support mysql,postgresql in the future
    'name':'accounts',
    'path': "%s/db" % BASE_DIR
}


LOG_LEVEL = logging.INFO
LOG_TYPES = {
    'operator': '/home/shunzi/person/老男孩pratice/day10-异步io-协程-多路复用/ftp/log/operator.log',
}