#The tables to the system of managing student
from sqlalchemy import Integer, ForeignKey, String, Column, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

student_MTM_class = Table('student_MTM_class', Base.metadata,
                    Column('class_id', Integer, ForeignKey('classes.id')),
                    Column('student_id', Integer, ForeignKey('students.id')),
                    )

class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer,primary_key=True)
    name = Column(String(64), nullable=False)
    qq = Column(String(64), nullable=False)
    password = Column(String(64), nullable=False)

class Class(Base):
    __tablename__ = 'classes'
    id = Column(Integer, primary_key=True)
    courseName = Column(String(64), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    # ...
    students = relationship('Student', secondary=student_MTM_class, backref='classes')
    teachers = relationship('Teacher', backref='classes')

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    qq = Column(String(64), primary_key=True)
    password = Column(String(64), nullable=False)

class Class_Record(Base):
    __tablename__ = 'class_record'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    class_id = Column(Integer, ForeignKey('classes.id'), nullable=False)
    process = Column(Integer, nullable=False)
    status = Column(String(64), default='no')
    point = Column(Integer, default=-1)

