'''配置文件'''
import os
import sys
import logging
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(BASE_DIR)

DATABASE = {
    'engine': 'file_storage',#support mysql,postgresql in the future
    'name':'computers',
    'path': "%s/database" % BASE_DIR
}


LOG_LEVEL = logging.INFO
LOG_TYPES = {
    'operator': '%s/log/info.log' % BASE_DIR,
}