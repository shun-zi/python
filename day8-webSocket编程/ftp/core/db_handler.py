'''数据库基本操作程序'''
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from conf import setting
import os
import json



if setting.DATABASE['engine'] == 'file_storage':
    '''数据库为文件系统类型'''
    dbFilePath = setting.DATABASE['path'] + '/' + setting.DATABASE['name']

class DB(object):
    '''有关数据库操作的类.'''
    def __init__(self):
        self.basePath = dbFilePath

    def get_fileNamesList(self, fileName):
        '''取出某个文件下的全部文件名'''
        filePath = self.basePath + '/' + fileName
        file_name_list = os.listdir(filePath)
        return file_name_list

    def get_fileDate(self, fileName):
        '''取出指定文件的数据'''
        filepath = self.basePath + '/' + fileName
        with open(filepath, 'r') as f:
            data = json.load(f)
        return data

    def store_data(self, fileName, data):
        '''存储数据到文件中'''
        filePath = self.basePath + '/' + fileName
        with open(filePath, 'w') as f:
            json.dump(data, f)

    def makedir(self, directoryName):
        '''创建文件夹'''
        filePath = self.basePath + '/' + directoryName
        os.mkdir(filePath)