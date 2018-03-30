import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from django.shortcuts import render
from django.shortcuts import HttpResponse, redirect
from sqlalchemy.orm import sessionmaker
from MysqlTables.tables import engine, User, Machine
# Create your views here.

session_class = sessionmaker(bind=engine)  # 创建与数据库的会话session class ,注意,这里返回给session的是个class,不是实例
session = session_class()  # 生成session实例

def home(request):
    return render(request, 'home.html')


def login(request):
    if request.method == 'POST':

        # session_class = sessionmaker(bind=engine)  # 创建与数据库的会话session class ,注意,这里返回给session的是个class,不是实例
        # session = session_class()  # 生成session实例
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        my_username = session.query(User).filter_by(username=username).first()
        if my_username is not None:
            if password == my_username.password:
                return redirect('/machine/')
            else:
                print('密码错误')
        else:
            print('用户名错误')

    return render(request, 'login.html')


def manage_machine(request):
    '''
    主机管理视图
    :param request: 客户端请求数据
    :return:
    '''
    id = request.POST.get('id', None)
    if (request.method=='POST' and id is None):
        hostname = request.POST.get('hostname', None)
        ip = request.POST.get('ip', None)
        port = request.POST.get('port', None)
        power = request.POST.get('power', None)
        a = request.POST.get('a', None)
        b = request.POST.get('b', None)
        c = request.POST.get('c', None)
        d = request.POST.get('d', None)
        machine_obj = Machine(hostname=hostname, ip=ip, port=int(port), power=power,
                              a=a, b=b, c=c, d=d)
        session.add(machine_obj)
        session.commit()
    else:
        machine_obj = session.query(Machine).filter_by(id=id).delete()
        session.commit()
    inf_list = []
    # 取出全部主机的信息
    my_machines = session.query(Machine).filter_by().all()
    try:
        for machine in my_machines:
            machine_dict = {'hostname':machine.hostname,
                            'ip': machine.ip,
                            'port': machine.port,
                            'power': machine.power,
                            'a': machine.a,
                            'b': machine.b,
                            'c': machine.c,
                            'd': machine.d,
                            'id': machine.id}
            inf_list.append(machine_dict)
    except Exception as e:
        pass

    return render(request, "machine.html", {'inf_list': inf_list})


def detail(request):
    id = request.GET.get('id', None)
    machine = session.query(Machine).filter_by(id=int(id)).first()
    print(machine)
    if machine is not None:
        machine_dict = {'hostname': machine.hostname,
                        'ip': machine.ip,
                        'port': machine.port,
                        'power': machine.power,
                        'a': machine.a,
                        'b': machine.b,
                        'c': machine.c,
                        'd': machine.d,
                        'id': machine.id}
    return  render(request, "detail.html", {'machine':machine_dict})
