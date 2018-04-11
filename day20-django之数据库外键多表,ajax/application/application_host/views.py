from django.shortcuts import render, HttpResponse
import json

# Create your views here.

import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from application_host import models as md


def host(request):
    if request.method == "GET":
        # 将该工程的数据库表的信息全部取出
        host_objs = md.Host.objects.all()
        application_objs = md.Application.objects.all()
        business_objs = md.Business.objects.all()
        return render(request, 'host.html',{'hosts': host_objs, 'applications': application_objs, 'business': business_objs})

    elif request.method == "POST":
        ret = {'status': True, 'error': None, 'data': None}
        operation = request.GET.get("operation", None)
        print(operation)
        db = request.GET.get("db", None)
        print(db)
        if operation == "add":
            # 添加功能
            if db == "host":
                # 往host表中添加数据
                hostname = request.POST.get("hostname", None)
                ip = request.POST.get("ip", None)
                try:
                    port = int(request.POST.get("port", None))
                except:
                    port = 80
                try:
                    business_id = int(request.POST.get("business_id", None))
                except:
                    business_id = 1

                business_obj = md.Business.objects.get(id=business_id)

                md.Host.objects.create(hostname=hostname,
                                       ip=ip,
                                       port=port,
                                       business=business_obj)
                return HttpResponse(json.dumps(ret))

            elif db == "application":
                # 往application表中添加数据
                name = request.POST.get("name", None)
                host_list = request.POST.getlist("host", None)
                new_obj = md.Application.objects.create(name=name)
                new_obj.r.add(*host_list)
                print(new_obj.r.all())
                return HttpResponse(json.dumps(ret))

        elif operation == "delete":
            # 删除功能
            if db == "host":
                try:
                    id = int(request.POST.get("id", None))
                except:
                    id = 1

                md.Host.objects.get(id=id).delete()
                return HttpResponse(json.dumps(ret))

            elif db == "application":
                try:
                    id = int(request.POST.get("id", None))
                except:
                    id = 1

                md.Application.objects.get(id=id).delete()
                return HttpResponse(json.dumps(ret))

        elif operation == "update":
            # 更新功能
            if db == "host":
                id = int(request.GET.get("id", None))
                hostname = request.POST.get("hostname", None)
                ip = request.POST.get("ip", None)
                try:
                    port = int(request.POST.get("id", None))
                except:
                    port = 80

                business_id = request.POST.get("business_id", None)

                business_obj = md.Business.objects.get(id=business_id)
                md.Host.objects.filter(id=id).update(hostname=hostname,
                                                    ip=ip,
                                                    port=port,
                                                    business=business_obj)
                return HttpResponse(json.dumps(ret))
            elif db == "application":
                id = int(request.GET.get("id", None))
                name = request.POST.get("name", None)

                host_list = request.POST.getlist("host_id", None)

                md.Application.objects.filter(id=id).update(name=name)
                obj = md.Application.objects.get(id=id)
                obj.r.set(host_list)
                return HttpResponse(json.dumps(ret))


