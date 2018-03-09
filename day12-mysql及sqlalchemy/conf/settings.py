'''学校管理系统'''
import os
import sys
import logging
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATABASE = {
    'engine': 'mysql',
    'name': 'schoolSystem',
    'user': 'root',
    'password': 'z960520@',
    'address': 'localhost'
}

LOG_LEVEL = logging.INFO
LOG_TYPES = {
    'operator': BASE_DIR + '/log/log'
}