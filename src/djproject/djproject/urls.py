#!/usr/bin/env python
#coding:utf-8

"""djproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import *
from django.contrib import admin
from djproject.views import index,future_time,show_picture,create_csv,create_pdf,login_view,logout_view,register

urlpatterns = [
    url(r"^$",login_view,{"register_info":None}),#定义跟目录
    url(r"^(?P<register_info>[A-Za-z]+\s[A-Za-z]+\s[A-Za-z]+)",login_view), #用户注册成功后，跳转回登陆页面(匹配注册方法跳转的url)
    url(r"^index/",index),
    url(r"^logout/",logout_view),
    url(r"^register/",register),
    url(r'^future/(\d{1,2})/',future_time),
    url(r'^admin/', admin.site.urls),
    url(r"^picture/",show_picture),
    url(r"^create_csv/",create_csv),
    url(r"^create_pdf/",create_pdf),
    url(r'^jobs/',include('jobs.urls')), #定义自定义应用
    url(r"^books/",include("books.urls")),#include是将正则和url匹配后多余的字符串(最后一个斜杠后)传给后续
]
