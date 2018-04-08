import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from django.shortcuts import render
from django.db import models
from machine import models as md
from django.views import View


# Create your views here.


# def home(request):
#     group_objs = md.MachineGroup.objects.all()
#     machine_objs = md.Machine.objects.all()
#
#     return render(request, 'home.html', {'groups':group_objs, 'machines': machine_objs})

class Home(View):

    def get(self, request):
        # get请求执行该函数
         group_objs = md.MachineGroup.objects.all()
         machine_objs = md.Machine.objects.all()
         return render(request, 'home.html', {'groups':group_objs, 'machines': machine_objs})

    def post(self, request):
        # post请求执行该函数.
        operation = request.GET.get("operation", None)
        db = request.GET.get("db", None)
        if operation == "add":
            if db=="machineGroup":
                name = request.POST.get("name", None)
                new_obj = md.MachineGroup(name=name)
                new_obj.save()
            elif db=="machine":
                hostname = request.POST.get("hostname", None)
                ip = request.POST.get("ip", None)
                port = int(request.POST.get("port", None))
                power = request.POST.get("power", None)
                group_id = int(request.POST.get("group_id", None))
                if group_id is not None:
                    group_obj = md.MachineGroup.objects.filter(id=group_id).first()
                    new_obj = md.Machine(hostname=hostname, ip=ip, port=port, power=power, machine_group=group_obj)
                    new_obj.save()
        elif operation == "delete":
            if db == "machineGroup":
                id = request.POST.get("id", None)
                del_group = md.MachineGroup.objects.filter(id=id).delete()
            elif db == "machine":
                id = request.POST.get("id", None)
                del_machine = md.Machine.objects.filter(id=id).delete()
        elif operation == "update":
            if db == "machineGroup":
                id = request.GET.get("id", None)
                name = request.POST.get("name", None)
                md.MachineGroup.objects.filter(id=id).update(name=name)
            elif db == "machine":
                id = request.GET.get("id", None)
                hostname = request.POST.get("hostname", None)
                ip = request.POST.get("ip", None)
                port = int(request.POST.get("port", None))
                power = request.POST.get("power", None)
                group_id = request.POST.get("group_id", None)
                group_obj = md.MachineGroup.objects.filter(id=group_id).first()
                md.Machine.objects.filter(id=id).update(hostname=hostname, ip=ip, port=port, power=power, machine_group=group_obj)


        group_objs = md.MachineGroup.objects.all()
        machine_objs = md.Machine.objects.all()
        return render(request, 'home.html', {'groups': group_objs, 'machines': machine_objs})