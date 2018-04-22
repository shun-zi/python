__author__ = "Alex Li"
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import datetime
from models import models
from modules import ssh_login
from conf import settings
from modules.utils import print_err,yaml_parser
from modules.db_conn import engine,session
def syncdb(argvs):
    print("Syncing DB....")
    engine = models.create_engine(settings.ConnParams,
                          echo=True )
    models.Base.metadata.create_all(engine) #创建所有表结构



def create_hosts(argvs):
    '''
    create hosts
    :param argvs: command line arguments
    :return:
    '''
    # 输入的命令行参数是否含有'-f'字符串
    if '-f' in argvs:
        # 取出文件名
        hosts_file  = argvs[argvs.index("-f") +1 ]
    else:
        print_err("invalid usage, should be:\ncreate_hosts -f <the new hosts file>",quit=True)
    source = yaml_parser(hosts_file)
    if source:
        print(source)
        for key,val in source.items():
            print(key,val)
            obj = models.Host(hostname=key,ip=val.get('ip'), port=val.get('port') or 22)
            session.add(obj)
        session.commit()


def create_remoteusers(argvs):
    '''
    create remoteusers
    :param argvs:
    :return:
    '''
    if '-f' in argvs:
        remoteusers_file  = argvs[argvs.index("-f") +1 ]
    else:
        print_err("invalid usage, should be:\ncreate_remoteusers -f <the new remoteusers file>",quit=True)
    source = yaml_parser(remoteusers_file)
    if source:
        for key,val in source.items():
            print(key,val)
            obj = models.RemoteUser(username=val.get('username'),auth_type=val.get('auth_type'),password=val.get('password'))
            session.add(obj)
        session.commit()


def create_users(argvs):
    '''
    create little_finger access user
    :param argvs:
    :return:
    '''
    # 输入的命令行参数是否含有'-f'字符串
    if '-f' in argvs:
        # 取出文件名
        user_file  = argvs[argvs.index("-f") +1 ]
    else:
        # 文件不存在时,输出错误信息
        print_err("invalid usage, should be:\ncreateusers -f <the new users file>",quit=True)
    #　得到包含用户信息的字典．
    source = yaml_parser(user_file)
    if source:
        # 一个一个的将用户存入数据库中.
        for key,val in source.items():
            print(key,val)
            obj = models.UserProfile(username=key,password=val.get('password'))
            # if val.get('groups'):
            #     groups = session.query(models.Group).filter(models.Group.name.in_(val.get('groups'))).all()
            #     if not groups:
            #         print_err("none of [%s] exist in group table." % val.get('groups'),quit=True)
            #     obj.groups = groups
            # if val.get('bind_hosts'):
            #     bind_hosts = common_filters.bind_hosts_filter(val)
            #     obj.bind_hosts = bind_hosts
            #print(obj)
            session.add(obj)
        session.commit()

def create_groups(argvs):
    '''
    create groups
    :param argvs:
    :return:
    '''
    if '-f' in argvs:
        group_file  = argvs[argvs.index("-f") +1 ]
    else:
        print_err("invalid usage, should be:\ncreategroups -f <the new groups file>",quit=True)
    source = yaml_parser(group_file)
    if source:
        for key,val in source.items():
            print(key,val)
            obj = models.HostGroup(name=key)
            # if val.get('bind_hosts'):
            #     bind_hosts = common_filters.bind_hosts_filter(val)
            #     obj.bind_hosts = bind_hosts
            #
            # if val.get('user_profiles'):
            #     user_profiles = common_filters.user_profiles_filter(val)
            #     obj.user_profiles = user_profiles
            session.add(obj)
        session.commit()



def create_bindhosts(argvs):
    '''
    create bind hosts
    :param argvs:
    :return:
    '''
    if '-f' in argvs:
        bindhosts_file  = argvs[argvs.index("-f") +1 ]
    else:
        print_err("invalid usage, should be:\ncreate_hosts -f <the new bindhosts file>",quit=True)
    source = yaml_parser(bindhosts_file)
    if source:
        for key,val in source.items():
            #print(key,val)
            # 从数据库中取出相应主机类实例
            host_obj = session.query(models.Host).filter(models.Host.hostname==val.get('hostname')).first()
            # 断言该实例是否存在
            assert host_obj
            for item in val['remote_users']:
                print(item )
                # 断言是否存在断言类型
                assert item.get('auth_type')
                if item.get('auth_type') == 'ssh-password':
                    # 从数据库中取出相应远程用户类实例
                    remoteuser_obj = session.query(models.RemoteUser).filter(
                                                        models.RemoteUser.username==item.get('username'),
                                                        models.RemoteUser.password==item.get('password')
                                                    ).first()
                else:
                    remoteuser_obj = session.query(models.RemoteUser).filter(
                                                        models.RemoteUser.username==item.get('username'),
                                                        models.RemoteUser.auth_type==item.get('auth_type'),
                                                    ).first()
                if not remoteuser_obj:
                    # 远程用户类实例不存在
                    print_err("RemoteUser obj %s does not exist." % item,quit=True )
                # 从数据库中取出相应绑定主机类实例
                bindhost_obj = models.BindHost(host_id=host_obj.id,remoteuser_id=remoteuser_obj.id)
                session.add(bindhost_obj)
                #for groups this host binds to
                if source[key].get('groups'):
                    group_objs = session.query(models.HostGroup).filter(models.HostGroup.name.in_(source[key].get('groups') )).all()
                    assert group_objs
                    print('groups:', group_objs)
                    bindhost_obj.host_groups = group_objs
                #for user_profiles this host binds to
                if source[key].get('user_profiles'):
                    userprofile_objs = session.query(models.UserProfile).filter(models.UserProfile.username.in_(
                        source[key].get('user_profiles')
                    )).all()
                    assert userprofile_objs
                    print("userprofiles:",userprofile_objs)
                    bindhost_obj.user_profiles = userprofile_objs
                #print(bindhost_obj)
        session.commit()

def auth():
    '''
    do the user login authentication
    :return:
    '''
    count = 0
    while count <3:
        username = input("\033[32;1mUsername:\033[0m").strip()
        if len(username) ==0:continue
        password = input("\033[32;1mPassword:\033[0m").strip()
        if len(password) ==0:continue
        user_obj = session.query(models.UserProfile).filter(models.UserProfile.username==username,
                                                            models.UserProfile.password==password).first()
        if user_obj:
            return user_obj
        else:
            print("wrong username or password, you have %s more chances." %(3-count-1))
            count +=1
    else:
        print_err("too many attempts.")

def welcome_msg(user):
    WELCOME_MSG = '''\033[32;1m
    ------------- Welcome [%s] login FuckJumpServer -------------
    \033[0m'''%  user.username
    print(WELCOME_MSG)

def store_aduit_log(user_profile_obj, bind_host_obj, cmd):
    '''

    :param user_obj: 登录远程计算机的用户对象
    :param bind_host_obj: 远程计算机对象
    :param cmd: 用户对象执行的命令字符串
    :return:
    '''
    aduitLog_obj = models.AuditLog(user_profile_id=user_profile_obj.id, bind_host_id=bind_host_obj.id, cmd=cmd,
                                   date=datetime.datetime.now())
    session.add(aduitLog_obj)
    session.commit()

def start_session(argvs):
    print('going to start sesssion ')
    # 验证用户
    user = auth()
    if user:
        # 用户登录成功,显示欢迎.
        welcome_msg(user)
        # 显示用户的绑定主机和用户的所属分组
        print(user.bind_hosts)
        print(user.host_groups)
        exit_flag = False
        while not exit_flag:
            if user.bind_hosts:
                # 显示该用户的绑定主机的数量
                print('\033[32;1mz.\tungroupped hosts (%s)\033[0m' %len(user.bind_hosts) )
            # 显示该用户所属分组的名字和每一个分组所绑定的主机数
            for index,group in enumerate(user.host_groups):
                print('\033[32;1m%s.\t%s (%s)\033[0m' %(index, group.name,  len(group.bind_hosts)) )

            choice = input("[%s]:" % user.username).strip()
            if len(choice) == 0:continue
            if choice == 'z':
                print("------ Group: ungroupped hosts ------" )
                for index,bind_host in enumerate(user.bind_hosts):
                    print("  %s.\t%s@%s(%s)"%(index,
                                              bind_host.remote_user.username,
                                              bind_host.host.hostname,
                                              bind_host.host.ip,
                                              ))
                print("----------- END -----------" )
            elif choice.isdigit():
                # 选择一个分组并且显示该分组中的绑定主机信息
                choice = int(choice)
                if choice < len(user.host_groups):
                    print("------ Group: %s ------"  % user.host_groups[choice].name )
                    for index,bind_host in enumerate(user.host_groups[choice].bind_hosts):
                        print("  %s.\t%s@%s(%s)"%(index,
                                                  bind_host.remote_user.username,
                                                  bind_host.host.hostname,
                                                  bind_host.host.ip,
                                                  ))
                    print("----------- END -----------" )

                    #host selection
                    while not exit_flag:
                        # 选择绑定主机
                        user_option = input("[(b)back, (q)quit, select host to login]:").strip()
                        if len(user_option)==0:continue
                        # 退出循环
                        if user_option == 'b':break
                        if user_option == 'q':
                            exit_flag=True
                        if user_option.isdigit():
                            user_option = int(user_option)
                            if user_option < len(user.host_groups[choice].bind_hosts) :
                                print('host:',user.host_groups[choice].bind_hosts[user_option])
                                login_info = {'hostname':user.host_groups[choice].bind_hosts[user_option].host.ip,
                                              'username':user.host_groups[choice].bind_hosts[user_option].remote_user.username,
                                              'password':user.host_groups[choice].bind_hosts[user_option].remote_user.password}
                                ssh_login.main(user, user.host_groups[choice].bind_hosts[user_option], login_info)
                #
                    print("no this option..")
