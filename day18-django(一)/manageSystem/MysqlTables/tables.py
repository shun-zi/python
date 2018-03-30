import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from manageSystem.settings import DATABASES

inf =  DATABASES['Mysql']
str = "mysql+pymysql://" + inf['username'] + ":" + inf['password'] + "@" + inf["address"] + "/" + inf["dbName"] + '?charset=utf8'
engine = create_engine(str,encoding='utf-8', echo=True)

Base = declarative_base()  # 生成orm基类


class User(Base):
    __tablename__ = 'user'  # 表名
    id = Column(Integer, primary_key=True)
    username = Column(String(32))
    password = Column(String(64))

class Machine(Base):
    __tablename__= 'machine'
    id = Column(Integer, primary_key=True)
    hostname = Column(String(32))
    ip = Column(String(64))
    port = Column(Integer)
    power = Column(String(32))
    a = Column(String(32))
    b = Column(String(32))
    c = Column(String(32))
    d = Column(String(32))

# Base.metadata.create_all(engine)  # 创建表结构
