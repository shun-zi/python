from django.shortcuts import render, redirect, reverse, HttpResponse
from machineManage import models
from utils.pagination import Page
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.forms import Form, fields, widgets
# Create your views here.

class Login(Form):
    username = fields.CharField(label='username',
                                widget=widgets.TextInput(attrs={'placeholder': '请输入用户名或邮箱'}))
    password = fields.CharField(min_length=6, label='password',
                                widget=widgets.PasswordInput(attrs={'placeholder':'请输入密码'}))

class Register(Form):
    username = fields.CharField(label='username',
                                widget=widgets.TextInput(attrs={'placeholder': '请输入用户名'}))
    email = fields.CharField(label='email',
                             widget=widgets.EmailInput(attrs={'placeholder': '请输入邮箱'}))
    password = fields.CharField(min_length=6, label='password',
                                widget=widgets.PasswordInput(attrs={'placeholder': '请输入密码'}))


def home(request):
    return render(request, 'home.html')

def login(request):
    err = {"account": None, "password": None}
    if request.method == "GET":
        obj = Login()
        return render(request, 'login.html', {'form': obj})
    if request.method == "POST":
        obj = Login(request.POST)

        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        account_obj = models.ACCOUNT.objects.filter(username=username)
        if len(account_obj) == 0:
            account_obj = models.ACCOUNT.objects.filter(email=username)

        # 判断用户输入的信息是否正确
        if len(account_obj) == 0:
            err["account"] = "输入的用户名或者邮箱不存在"
            return render(request, "login.html", {'err': err, 'form': obj})
        else:
            if account_obj[0].password != password:
                err["password"] = "密码输入错误"
                return render(request, "login.html", {'err': err, 'form': obj})

        if obj.is_valid():
            # 设置cookie
            res = redirect('/home/machine/')
            request.session["username"] = obj.cleaned_data["username"]
            return res
        else:
            print(1)


def register(request):
    err = {'username': None, 'email': None}
    if request.method == "GET":
        form_obj = Register()
        return render(request, 'register.html', {'form': form_obj})
    elif request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        form_obj = Register(request.POST)

        account_username = models.ACCOUNT.objects.filter(username=username)
        account_email = models.ACCOUNT.objects.filter(email=email)
        if len(account_username) != 0:
            err['username'] = '用户名已经存在'
            return render(request, "register.html", {'err': err, 'form': form_obj})
        else:
            if len(account_email) != 0:
                err['email'] = '该邮箱地址已经存在'
                return render(request, "register.html", {'err': err, 'form': form_obj})

        if form_obj.is_valid():
            models.ACCOUNT.objects.create(**form_obj.cleaned_data)
            return redirect("/home/login")
        else:
            print(1)


def auth(func):
    def inner(request, *args, **kwargs):
        if request.method == "GET":
            cookie = request.session.get("username", 'None')
            if cookie == 'None':
                return redirect('/home/login')
        return func(request, *args, **kwargs)
    return inner


@csrf_exempt
@auth
def machine(request):
    if request.method == "GET":
        cookie = request.session.get("username", None)
        return render(request, "machine.html", {'username': cookie})
    elif request.method == "POST":
        if request.POST.get("operation") == "logout":
            del request.session["username"]
            return HttpResponse('...')


@auth
def host(request):
    if request.method == "GET":
        pass
    elif request.method == "POST":
        id = request.POST.get("id")
        models.Host.objects.filter(id=id).delete()

    cookie = request.session["username"]
    onePage_hosts = int(request.COOKIES.get("show_hosts", 5))
    select_page = int(request.GET.get("page", 1))
    host_objs = models.Host.objects.all()
    host_counts = len(host_objs)
    # 为了方便show_pages只定为奇数
    show_pages = 5
    half_show_pages = int(show_pages / 2)
    # business = models.Business.objects.get(id=1)
    # models.Host.objects.create(hostname="shunzi", ip="127.0.0.1", port=53, business=business)

    page = Page(show_pages)
    page_counts = page.divide_page(host_counts, onePage_hosts)
    page.start_and_end_page(select_page, half_show_pages, page_counts,)
    # 返回给前端的
    start_page = page.start_page
    end_page = page.end_page
    show_host_objs = page.show_hosts(select_page, onePage_hosts, host_counts, host_objs)

    page_dict = {'show_page': range(start_page, end_page+1), 'show_host': show_host_objs}
    return render(request, "host.html", {'username': cookie, 'page': page_dict})


@auth
def add_host(request):
    if request.method == "GET":
        cookie = request.session.get("username", None)
        business = models.Business.objects.all()
        return render(request, "add-host.html", {'username': cookie, "business": business})
    elif request.method == "POST":
        hostname = request.POST.get("hostname")
        ip = request.POST.get("ip")
        port = int(request.POST.get("port"))
        business_id = int(request.POST.get("business_id"))
        business_obj = models.Business.objects.get(id=business_id)
        models.Host.objects.create(hostname=hostname, ip=ip, port=port, business=business_obj)
        return redirect("/home/machine/host/")


@auth
def edit_host(request):
    if request.method == "GET":
        cookie = request.session.get("username", None)
        id = int(request.GET.get("id", 1))
        host_obj = models.Host.objects.get(id=id)
        business = models.Business.objects.all()
        return render(request, "edit-host.html", {'username': cookie, "business": business, 'host': host_obj})
    elif request.method == "POST":
        id = request.GET.get("id")
        hostname = request.POST.get("hostname")
        ip = request.POST.get("ip")
        port = int(request.POST.get("port"))
        business_id = int(request.POST.get("business_id"))
        business_obj = models.Business.objects.get(id=business_id)
        models.Host.objects.filter(id=id).update(hostname=hostname, ip=ip, port=port, business=business_obj)
        return redirect("/home/machine/host/")


@auth
def app(request):
    if request.method == "GET":
        pass
    elif request.method == "POST":
        id = request.POST.get("id")
        models.Application.objects.filter(id=id).delete()

    cookie = request.session.get("username", None)
    onePage_hosts = int(request.COOKIES.get("show_hosts", 5))
    select_page = int(request.GET.get("page", 1))
    app_objs = models.Application.objects.all()
    app_counts = len(app_objs)
    host_objs = models.Host.objects.all()
    # 为了方便show_pages只定为奇数
    show_pages = 5
    half_show_pages = int(show_pages / 2)
    # business = models.Business.objects.get(id=1)
    # models.Host.objects.create(hostname="shunzi", ip="127.0.0.1", port=53, business=business)

    page = Page(show_pages)
    page_counts = page.divide_page(app_counts, onePage_hosts)
    page.start_and_end_page(select_page, half_show_pages, page_counts,)
    # 返回给前端的
    start_page = page.start_page
    end_page = page.end_page
    show_app_objs = page.show_hosts(select_page, onePage_hosts, app_counts, app_objs)

    page_dict = {'show_page': range(start_page, end_page+1), 'show_apps': show_app_objs, 'host': host_objs}
    return render(request, "app.html", {'username': cookie, 'page': page_dict})


@auth
def add_app(request):
    if request.method == "GET":
        cookie = request.session.get("username", None)
        host_objs = models.Host.objects.all()
        return render(request, "add-app.html", {'username': cookie, "hosts": host_objs})
    elif request.method == "POST":
        appname = request.POST.get("name")
        print(appname)
        hostList = request.POST.getlist("host_id")
        app_obj = models.Application.objects.create(name=appname)
        app_obj.r.set(hostList)
        return redirect("/home/machine/app/")


@auth
def edit_app(request):
    if request.method == "GET":
        cookie = request.session.get("username", None)
        id = int(request.GET.get("id", 1))
        app_obj = models.Application.objects.get(id=id)
        host_objs = models.Host.objects.all()
        return render(request, "edit-app.html", {'username': cookie, 'app': app_obj, 'hosts': host_objs})
    elif request.method == "POST":
        id = int(request.GET.get("id"))
        appname = request.POST.get("name")
        hostList = request.POST.getlist("host_id")
        models.Application.objects.filter(id=id).update(name=appname)
        app_obj = models.Application.objects.get(id=id)
        app_obj.r.set(hostList)
        return redirect("/home/machine/app/")