from sqlalchemy.orm import sessionmaker
import time
import sqlalchemy
from db.test import tables
from core import schoolMember
from core.log import *

log = Logger('teacher')
log.create_logger()
log.create_file_handler()


def show_class(session, t):
    # 显示老师所教班级
    # 到数据库中找出该教师所教的班级记录
    class_objs = session.query(tables.Class).filter_by(teacher_id=t.id).all()
    if class_objs == []:
        print('你还没指导任何班级.')
    else:
        print('你所管理的班级:')
        for class_obj in class_objs:
            print(str(class_obj.id) + ':' + class_obj.courseName)


def select_class(session, t):
    # 选择班级
    while True:
        classID = t.select_class()
        class_obj = session.query(tables.Class).filter_by(id=classID).first()
        # 取出属于该班级的同学信息
        student_objs = class_obj.students
        if student_objs == []:
            print('该班级还未添加任何一个同学.')
        elif student_objs == None:
            print('所选择的班级不存在,请重新选择.')
        else:
            print('************************')
            for student_obj in student_objs:
                print(student_obj.qq, student_obj.name)
            print('************************')
        return class_obj


def register(session):
    # 注册
    s = schoolMember.SchoolMember()
    registerInf = s.register()
    # 创建一条新老师数据记录
    try:
        student_obj = tables.Teacher(qq=registerInf['qq'], name=registerInf['name'], password=registerInf['password'])
        # 把要创建的数据对象添加到这个session里， 一会统一创建
        session.add(student_obj)
        # 提交数据
        session.commit()
        log.logger.info('%s成功注册'%registerInf['name'])
        print('成功注册')
    except Exception as e:
        print('error:%s'%e)
        print('注册失败,请重新注册.')


def login(session):
    # 登录
    s = schoolMember.SchoolMember()
    while True:
        loginInf = s.login()

        # 根据qq号到数据库寻找相关数据
        teacher_obj = session.query(tables.Teacher).filter_by(qq=loginInf['qq']).first()
        if teacher_obj == None:
            print('该老师不存在.')
        else:
            if teacher_obj.password == loginInf['password']:
                print('成功登录')
                log.logger.info('%s登录到学校网站'%loginInf['qq'])
                # 创建一个对象保留教师登录信息,方便后面的功能实现.
                t = schoolMember.Teacher(id=teacher_obj.id, qq=loginInf['qq'], password=loginInf['password'])
                return t
            else:
                print('该老师不存在.')
        return False


def create_class(session, t):
    # 创建一个新班级
    s_t = schoolMember.Teacher()
    while True:
        again = False
        courseName = s_t.create_class()
        class_objs = session.query(tables.Class).filter_by(teacher_id=t.id).all()
        for class_obj in class_objs:
            if courseName == class_obj.courseName:
                # 对于该老师, 该课程已经创建了.
                again = True
                break
        if again == True:
            # 重新输入课程
            print('课程已经存在,请重新输入')
            break
        try:
            class_obj = tables.Class(courseName=courseName, teacher_id=t.id)
            session.add(class_obj)
            session.commit()
            log.logger.info('teacher%d创建了%s课程'%(t.id, courseName))
            print('成功创建课程.')
            show_class(session, t)
            break
        except Exception as e:
            print('error:%s'%e)
            print('请重新创建班级.')

def add_student(session, t):
    # 根据学生的qq号添加学生到指定班级
    class_obj = select_class(session, t)
    student_objs = class_obj.students
    while True:
        exist = False
        studentQQ = input('请输入学生的qq:')
        for student_obj in student_objs:
            if student_obj.qq == studentQQ:
                print('该同学已经存在于班级中,请重新输入.\n')
                exist = True
                break
        if exist == True:
            continue
        else:
            new_student_obj = session.query(tables.Student).filter_by(qq=studentQQ).first()
            class_obj.students.append(new_student_obj)
            print('添加学生成功')
            log.logger.info('添加学生%s到%s班级'%(new_student_obj.name, class_obj.courseName))
            session.commit()
            break

def create_classRecord(session, t):
    # 创建指定班级的上课记录
    class_obj = select_class(session, t)
    student_objs = class_obj.students
    while True:
        exist = False
        classRecords = session.query(tables.Class_Record).filter_by(class_id=class_obj.id).all()
        if classRecords == []:
            print('该班级未创建任何记录')
            process = input('请输入第几节课:')
        else:
            process = input('请输入第几节课:')
            for classRecord in  classRecords:
                if classRecord.process == process:
                    print('该班级课记录已经创建过.')
                    exist = True
                    break

        if exist == True:
            continue
        else:
            list = []
            for student_obj in student_objs:
                a = tables.Class_Record(student_id=student_obj.id, class_id=class_obj.id, process=process)
                list.append(a)
            session.add_all(list)
            print('成功创建班级上课记录')
            log.logger.info('教师%d成功创建班级%d第%s次上课记录'%(t.id, class_obj.id, process))
            session.commit()
            break

def add_classRecord(session, t):
    # 添加指定学生的上课记录
    while True:
        # 请求用户输入学生信息
        student_dict = t.add_record()
        # 判断该学生属不属于指定班级
        student_obj = session.query(tables.Student).filter_by(id=student_dict['id']).first()
        class_obj = session.query(tables.Class).filter_by(id=student_dict['class']).first()
        try:
            student_objs = class_obj.students
        except:
            print('班级或者学生不存在,请重新输入.')
            continue
        if student_obj not in student_objs:
            print('该学生不属于该班级.')
        else:
            # 在该班级中,判断该学生是否在指定课期中已有记录
            record_obj = session.query(tables.Class_Record).filter_by(student_id=student_dict['id'],
                                                                      class_id=student_dict['class'],
                                                                      process=student_dict['process']).first()
            if record_obj is not None:
                print('该学生的上课记录已经存在,或者课期记录还未创建.')
            else:
                new_record = tables.Class_Record(student_id=student_dict['id'], class_id=student_dict['class'],
                                                 process=student_dict['process'])
                session.add(new_record)
                print('该学生记录添加成功.')
                log.logger.info('教师%d在%d班级创建了%d学号生第%s次上课记录' % (t.id, class_obj.id, student_obj.id,
                                                               student_dict['process']))
                session.commit()
                break


def show_point(session, class_id, process):
    # 展示该班级同学的成绩
    class_record_objs = session.query(tables.Class_Record).filter_by(class_id=class_id, process=process,
                                                                     status='yes').all()
    if class_record_objs == []:
        print('%d班级的第%d次课期的记录不存在.' % (class_id, process))
        return False
    else:
        print('*********************')
        print('学生ID 成绩')
        for class_record_obj in class_record_objs:
            print('%d     %d' % (class_record_obj.student_id, class_record_obj.point))
        print('*********************')

def correct_point(session, t):
    # 手动为学生批改成绩
    class_id = int(input('请输入班级:'))
    process = int(input('请输入课期:'))
    exist = show_point(session, class_id, process)
    if exist is not False:
        while True:
            student_id = input('请输入批改成绩的学生的ID:(输入exit退出)')
            if student_id == 'exit':
                break
            student_id = int(student_id)
            point = int(input('请输入成绩:'))
            class_record_obj = session.query(tables.Class_Record).filter_by(class_id=class_id, process=process,
                                                                            student_id=student_id).first()
            if class_record_obj is None:
                print('该学生不存在,请重新输入.')
                continue
            else:
                class_record_obj.point = point
                print('批改成功')
                log.logger.info('%d教师给%d班级的%d学生的第%d次作业打上%d分' % (t.id, class_id, student_id, process, point))
                session.commit()


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
            t = login(session)
            if t is not False:
                break
        else:
            continue

    while True:
        # 显示指定教师所教的班级
        show_class(session, t)

        print('\n*********************')
        print('1.exit')
        print('2.创建班级')
        print('3.添加学生')
        print('4.创建班级上课记录')
        print('5.添加学生上课记录')
        print('6.批改成绩')
        print('*********************')

        index = int(input('请选择相应操作的索引:'))
        if index == 1:
            print('退出系统')
            break
        elif index == 2:
            create_class(session, t)
        elif index == 3:
            add_student(session, t)
        elif index == 4:
            create_classRecord(session, t)
        elif index == 5:
            add_classRecord(session, t)
        elif index == 6:
            correct_point(session, t)
