# 创建学校成员类.
import hashlib
from db.test import tables
from core.log import *

log = Logger('student')
log.create_logger()
log.create_file_handler()

class SchoolMember(object):

    def __init__(self, qq=None, name=None, password=None):
        self.qq = qq
        self.name = name
        self.__password = password

    def register(self):
        '''注册'''
        m = hashlib.md5()
        self.qq = input('请输入你的QQ账号:')
        self.name = input('请输入你的真实姓名:')
        m.update(input('请输入你的密码:').encode())
        self.__password = m.hexdigest()
        dict = {'qq': self.qq, 'name': self.name, 'password': self.__password}
        return dict

    def login(self):
        '''登录'''
        m = hashlib.md5()
        qq = input('请输入你的QQ账号:')
        m.update(input('请输入你的密码:').encode())
        password = m.hexdigest()
        dict = {'qq': qq, 'password': password}
        return dict

class Student(SchoolMember):
    '''学生类'''
    def __init__(self, id=None, qq=None, name=None, password=None):
        super(Student, self).__init__(qq, name, password)
        self.id = id

    def select_class(self, session):
        # 选择班级
        while True:
            selectClassID = input('请输入你所选择的班级id:')
            class_obj = session.query(tables.Class).filter_by(id=selectClassID).first()
            # 判断班级存不存在
            if class_obj is None:
                print('你所选择班级不存在,请重新输入.')
                continue
            else:
                return class_obj

    def select_process(self, session, class_obj):
        # 选择具体上课节数
        while True:
            process = input('请输入你所选择的具体上课节数:')
            class_record_obj = session.query(tables.Class_Record).filter_by(student_id=self.id,
                                                                            class_id=class_obj.id,
                                                                            process=process).first()
            if class_record_obj is None:
                print('你所选择的课期不存在,请重新输入.')
                continue
            else:
                return class_record_obj

    def submit_work(self, session):
        # 提交作业
        class_obj = self.select_class(session)
        class_record_obj = self.select_process(session, class_obj)
        if class_record_obj.status == 'yes':
            print('你已经提交过作业了.')
        else:
            status = input('请确认是否提交作业?(yes/no)')
            if status == 'yes':
                class_record_obj.status = 'yes'
                print('成功提交作业.')
                log.logger.info('%d学生成功提交了%d班级的第%s次作业' % (self.id, class_obj.id, class_record_obj.process))
                session.commit()


    def look_point(self, session):
        '''查询成绩'''
        while True:
            class_id = int(input('请输入班级号:(输入-1即停止查询)'))
            if class_id != -1:
                process = int(input('请输入课期:'))
                class_record_obj = session.query(tables.Class_Record).filter_by(student_id=self.id, process=process,
                                                                                class_id=class_id).first()
                if class_record_obj is None:
                    print('查询不到成绩,请重新输入班级和课期.')
                    continue
                else:
                    print('你的成绩:%d' % class_record_obj.point)
            else:
                break

class Teacher(SchoolMember):
    '''教师类'''
    def __init__(self, id=None, qq=None, name=None, password=None):
        super(Teacher, self).__init__(qq, name, password)
        self.id = id

    def create_class(self):
        '''创建班级'''
        courseName = input('你所创建的班级名称:')
        return courseName

    def select_class(self):
        '''选择班级'''
        selectClass = input('请输入你所选择的班级id:')
        return selectClass

    def create_record(self):
        '''创建指定班级的上课记录'''
        process = input('输入要创建的上课节数:')
        return process
    def correct_point(self):
        '''批改成绩'''
        point = input('输入该同学获得的成绩:')
        return point

    def add_record(self):
        '''添加学生上课记录'''
        student_id = input('请输入学生的id号:')
        class_id = input('请输入学生所属班级:')
        process = input('请输入第几节课:')
        student_dict = {'id': student_id, 'class': class_id, 'process': process}
        return student_dict