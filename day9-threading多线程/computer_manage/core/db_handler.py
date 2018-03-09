'''有关数据库的操作'''
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from conf import settings
import os
import json



if settings.DATABASE['engine'] == 'file_storage':
    '''数据库为文件系统类型'''
    dbFilePath = settings.DATABASE['path']# + '/' + setting.DATABASE['name']
    # /home/shunzi/person/老男孩pratice/day9/computer_manage/database

    class DB(object):
        '''有关数据库操作的类.'''
        def __init__(self):
            self.basePath = dbFilePath

        def get_fileNamesList(self, fileName):
            '''取出某个文件下的全部文件名'''
            filePath = self.basePath + '/' + fileName
            # try:
            file_name_list = os.listdir(filePath)
            return file_name_list
            # except FileNotFoundError as e:
                # print(e)
                # return False
                # raise e

        def get_fileDate(self, fileName):
            '''取出指定文件的数据'''
            filepath = self.basePath + '/' + fileName
            # try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            return data
            # except Exception as e:
            #     print(e)
            #     return False

        def store_data(self, fileName, data):
            '''存储数据到文件中'''
            # try:
            filePath = self.basePath + '/' + fileName
            with open(filePath, 'w') as f:
                json.dump(data, f)
            # except Exception as e:
            #     print(e)
            #     return False

        def makedir(self, directoryName):
            '''创建文件夹'''
            # try:
            filePath = self.basePath + '/' + directoryName
            os.mkdir(filePath)
            # except Exception as e:
            #     print(e)
            #     return False