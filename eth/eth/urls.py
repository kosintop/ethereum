"""eth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from . import API
from .views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home.index),
    path('create_user',API.create_user, name='create_user'),
    path('create_vendor',API.create_vendor, name='create_vendor'),
    path('add_point',API.add_point, name='add_point'),
    path('get_points_by_user',API.get_point_by_user, name='get_point_by_user'),
    path('transfer_point',API.transfer_point, name='transfer_point'),
    path('add_reward',API.add_reward, name='add_reward'),
    path('exchange_reward',API.exchange_reward, name='exchange_reward'),
    path('get_all_account',API.get_all_account, name='get_all_account'),
    path('test', API.test, name='test'),
]
