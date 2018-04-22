import sqlalchemy
from sqlalchemy.orm import sessionmaker
import time
from db.test import tables
from core import schoolMember
from core.log import *


def register(session):
    # 注册
    s = schoolMember.SchoolMember()
    register_inf = s.register()
    # 创建一条新学生数据记录
    try:
        student_obj = tables.Student(qq=register_inf['qq'], name=register_inf['name'],
                                     password=register_inf['password'])
        # 把要创建的数据对象添加到这个session里， 一会统一创建
        session.add(student_obj)
        # 提交数据
        session.commit()
        schoolMember.log.logger.info('%s成功注册' % register_inf['name'])
        print('成功注册')
    except Exception as e:
        print('error:%s' % e)
        print('注册失败,请重新注册.')


def login(session):
    # 登录
    s = schoolMember.SchoolMember()
    while True:
        login_inf = s.login()

        # 根据qq号到数据库寻找相关数据
        student_obj = session.query(tables.Student).filter_by(qq=login_inf['qq']).first()
        if student_obj is None:
            print('该学生不存在.')
        else:
            if student_obj.password == login_inf['password']:
                print('成功登录')
                schoolMember.log.logger.info('%s登录到学校网站' % login_inf['qq'])
                # 创建一个对象保留教师登录信息,方便后面的功能实现.
                s = schoolMember.Student(id=student_obj.id, qq=login_inf['qq'], password=login_inf['password'])
                return s
            else:
                print('该学生不存在.')
        return False


def main(engine):
    # 学生视图的主程序
    # 创建与数据库的会话session class ,注意,这里返回给session的是个class,不是实例
    session_class = sessionmaker(bind=engine)
    # 生成session实例
    session = session_class()

    while True:
        print('\n*********************')
        print('1.exit')
        print('2.注册')
        print('3.登录')
        print('*********************')
        # 选择接下来要进行的操作
        index = int(input('请选择要进行的操作:'))
        if index == 1:
            time.sleep(2)
            print('退出系统!')
            break
        elif index == 2:
            register(session)
        elif index == 3:
            s = login(session)
            if s is not False:
                break
        else:
            continue

    while True:
        print('\n*********************')
        print('1.exit')
        print('2.提交作业')
        print('3.查询成绩')
        print('*********************')

        # 选择接下来要进行的操作
        index = int(input('请选择要进行的操作:'))
        if index == 1:
            time.sleep(2)
            print('退出系统!')
            break
        elif index == 2:
            s.submit_work(session)
        elif index == 3:
            s.look_point(session)
        else:
            continue
