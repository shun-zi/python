from django.conf.urls import url, include
from machineManage import views

urlpatterns = [
    url('login/$', views.login),
    url('register/$', views.register),
    url('machine/$', views.machine, name="host"),
    url('machine/host/$', views.host),
    url('machine/host/add-host/$', views.add_host),
    url('machine/host/edit-host/$', views.edit_host),
    url('machine/app/$', views.app),
    url('machine/app/add-app/$', views.add_app),
    url('machine/app/edit-app/$', views.edit_app)
]
