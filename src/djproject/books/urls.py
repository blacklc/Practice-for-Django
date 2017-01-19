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
from books import views
from models import *

"""
定义特定应用的url配置
"""
#URL继续顺序是自顶向下(同防火墙的ACL)
urlpatterns = [
    #url(r"^$","books.views.index")
    url(r"^$",views.index_thank,{
         "template":"books_index.html",        #关键字参数字段对应view方法的各个参数
         "context":{
                    "search":"/books/search",
                    "contact_form":"/books/contact/form",
                    "publisher_apress":"/books/publisher_list/Apress",
                    "publisher_apple":"/books/publisher_list/Apple",
                    "authors_sunx":"/books/authors/sun",
                    "authors_jacktomas":"/books/authors/jack",
                    "authors_zz":"/books/authors/z",
                    #"test":Book.objects.title_count("test"),
                    }
    }),
    url(r"^search/$",views.search),
    url(r"^contact/form/$",views.contact),
    url(r"^contact/thanks/$",views.index_thank,{
         "template":"thanks.html",
         "context":None
    }),
    url(r"^publisher_list/(?P<pname>\w+)/$",views.publisher_listview.as_view()),
    url(r"^authors/(?P<fn>\w+)/$",views.author_listview.as_view())
]












