import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from machine import views
from django.conf.urls import url,include

urlpatterns = [
    url('home/', views.Home.as_view())
]