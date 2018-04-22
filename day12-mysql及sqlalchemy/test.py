#
#
#
# from sqlalchemy import Table, Column, Integer,String,DATE, ForeignKey
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
#
#
# Base = declarative_base()
#
# book_m2m_author = Table('book_m2m_author', Base.metadata,
#                         Column('id', Integer, primary_key=True),
#                         Column('book_id',Integer,ForeignKey('books.id')),
#                         Column('author_id',Integer,ForeignKey('authors.id')),
#                         # Column('brower_id', Integer, ForeignKey('browers.id')),
#                         )
# book_m2m_brower = Table('book_m2m_brower', Base.metadata,
#                         Column('book_id',Integer,ForeignKey('book_m2m_author.id')),
#                         Column('author_id',Integer,ForeignKey('browers.id')),)
#
# class Book(Base):
#     __tablename__ = 'books'
#     id = Column(Integer,primary_key=True)
#     name = Column(String(64))
#     # pub_date = Column(DATE)
#     authors = relationship('Author',secondary=book_m2m_author,backref='books')
#     # browers = relationship('Brower',secondary=book_m2m_author,backref='books')
#
#
#     def __repr__(self):
#         return self.name
#
#
# class Author(Base):
#     __tablename__ = 'authors'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(32))
#
#     def __repr__(self):
#         return self.name
#
# engine = create_engine("mysql+pymysql://root:z960520@@localhost/test?charset=utf8",
#                                     encoding='utf-8', echo=True)
#
# # Base.metadata.create_all(engine) #创建表结构
#
#
# Session_class = sessionmaker(bind=engine)  # 创建与数据库的会话session class ,注意,这里返回给session的是个class,不是实例
# s = Session_class()  # 生成session实例
#
# b1 = Book(name="AlexPython")
# b2 = Book(name="Alexlinux")
# b3 = Book(name="Alexphp")
# b4 = Book(name="Alexhehe")
#
# b5 = Brower(name="deshun")
# b6 = Brower(name="deshun1")
# b7 = Brower(name="deshun2")
# print(b5)
#
#
#
# a1 = Author(name="Alex")
# a2 = Author(name="Jack")
# a3 = Author(name="Rain")
# print(a1)
#
# b1.authors = [a1, a2]
# b2.authors = [a1, a2, a3]
# b5.book_m2m_author = []
#
# s.add_all([b1, b2, b3, b4, b5, b6, b7,a1, a2, a3])
#
# s.commit()

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from db.test import tables

engine = create_engine("mysql+pymysql://root:z960520@@localhost/schoolSystem",
                       encoding='utf-8')

Base = declarative_base()  # 生成orm基类


class User(Base):
    __tablename__ = 'user'  # 表名
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    password = Column(String(64))


# Base.metadata.create_all(engine)  # 创建表结构

Session_class = sessionmaker(bind=engine)  # 创建与数据库的会话session class ,注意,这里返回给session的是个class,不是实例
Session = Session_class()  # 生成session实例

# user_obj = User(name="alex", password="123456")  # 生成你要创建的数据对象
# print(user_obj.name, user_obj.id)  # 此时还没创建对象呢，不信你打印一下id发现还是None
#
# Session.add(user_obj)  # 把要创建的数据对象添加到这个session里， 一会统一创建
# print(user_obj.name, user_obj.id)  # 此时也依然还没创建
#
# Session.commit()  # 现此才统一提交，创建数据

my_user = Session.query(User).filter_by(name='fsjajfksaj').all()
print(my_user)



# import hashlib
#
# m = hashlib.md5()
# m.update(b"Hello")
# m.update(b"It's me")
# print(m.digest())
# m.update(b"It's been a long time since last time we ...")
#
# print(m.digest())  # 2进制格式hash
# print(m.hexdigest())  # 16进制格式hash
