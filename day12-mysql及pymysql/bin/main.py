import sqlalchemy
from sqlalchemy import create_engine
from conf import settings
from db.test import tables
from core import studentView, teacherView

database = settings.DATABASE
connect_inf = database['engine'] + '+pymysql://' + database['user'] + ':' + database['password'] + '@' + database['address'] + '/' + database['name'] + '?charset=utf8'
engine = create_engine(connect_inf, encoding='utf-8')

# orm基类
Base = tables.Base

# 向用户询问是否重新建立表结构
rc = input('是否重新建立表格(y/n)?')
if rc == 'no':
    pass
else:
    Base.metadata.create_all(engine)

# 询问用户的身份, 进入相应的视图
view = input('选择身份（student/teacher/exit):')
if view == 'exit':
    print('已经退出学员管理系统！')
elif view == 'student':
    studentView.main(engine)
elif view == 'teacher':
    teacherView.main(engine)
