import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from django.conf.urls import url, include

from application_host import views

urlpatterns = [
    url('host/', views.host)
]