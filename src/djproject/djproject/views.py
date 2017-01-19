#!/usr/bin/env python
#coding:utf-8

# Create your views here.
import csv
import datetime

from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.contrib import auth,messages
from djproject.form import login_form
from django.shortcuts import render_to_response,Http404,render
from django.http.response import  HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm

def current_datetime():
    """
    获取当前系统时间
    """
    now=datetime.datetime.now()
    return now

def future_time(request,offset):
    """
    计算未来时间
    """
    try:
        offset=int(offset)
    except ValueError:
        raise Http404
    dt=current_datetime()+datetime.timedelta(hours=offset)
    #assert False 强制出发错误，以便跟踪调试程序
    return render_to_response('templates/future.html', {'future_time':dt})

def show_picture(request):
    """
    视图返回一个非html类型
    """
    image_data=open("/Library/Desktop Pictures/El Capitan.jpg","rb").read()
    return HttpResponse(image_data,content_type="image/jpeg")

def create_csv(request):
    """
    使用httpresponse创建csv文件
    """
    data=[146,184,235,200,226,251,299,273,281,304,203]
    response=HttpResponse(content_type="test/csv")
    response["content-Disposition"]="attachment;filename='test_csv.csv'"
    writer=csv.writer(response)
    writer.writerow(["Year","Unruly Airline Passengers"])
    #zip方法能够使两个list中对应并排的元素配对，返回一个包含多个描述配对的tuple的list
    for (year,num) in zip(range(1995,2006),data):
        writer.writerow([year,num])
    return response

def create_pdf(request):
    """
    使用httpresponse创建pdf文件
    """
    response=HttpResponse(content_type="application/pdf")
    response["Content-Disposition"]="attachment;filename='test_pdf.pdf'"
    buffer=BytesIO() #创建临时空间存放大容量pdf
    p=canvas.Canvas(buffer)
    p.drawString(100,100,"django create pdf test")
    p.showPage()
    p.save()
    pdf=buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
    """
    create simple pdf version 
    response=HttpResponse(content_type="application/pdf")
    response["Content-Disposition"]="attachment;filename='test_pdf.pdf'"
    p=canvas.Canvas(response)
    p.drawString(100,100,"django create pdf test")
    p.showPage()
    p.save()
    return response
    """
    
def index(request):
    """
    首页
    """
    #assert False 强制出发错误，以便跟踪调试程序
    messages.add_message(request,messages.SUCCESS,"Login successful")
    #s=get_messages(request) #获取messages内容
    #messages.success(request,"Welcome %s"%request.user.username) #添加messages的快捷方法
    #注意url要带“/”
    context={
            'app':"/jobs/",
            "app2":"/books/",
            'time':current_datetime(),
            'offset':2,
            'a':1,
            'b':1,
            'cstring':"abc",
            "request":request,
            'request_META':request.META.items(),
            }
    return render(request,"index.html",context) #在1.10版本后使用Requestcontext就使用此方法(django.shortcuts render)即可
    """
    return render_to_response('templates/index.html',
                              {'app':"/jobs/",
                               "app2":"/books/",
                               'time':current_datetime(),
                               'offset':2,
                               'a':1,
                               'b':1,
                               'cstring':"abc",
                               "request":request,
                               'request_META':request.META.items(),
            })
    """

def login_view(request,register_info):
    """
    处理用户登陆，使用django的认证系统
    """
    #判断用户是否已经登陆
    if request.user.is_authenticated():
        return HttpResponseRedirect("/index/") #实现已登陆自动跳转页面
    #若通过post提交表单(登陆操作)
    if request.method=="POST":
        form=login_form(request.POST)
        #判断用户输入是否合法；若合法则返回干净数据
        if form.is_valid():
            form_context=form.cleaned_data
            username=form_context["username"]
            password=form_context["password"]
        else:
            username=None
            password=None
        user=auth.authenticate(username=username,password=password) #验证用户的证书(合法性)
        #判断用户是否可以登陆以及合法
        if user is not None and user.is_active:
            auth.login(request,user)
            return HttpResponseRedirect("/index/")
        #判断用户是否被锁定
        elif user is not None:
            form.error="The user is locked"
        #否则用户不存在
        else:
            form.error="The user not exist"
    else:
        #若是第一次登陆(没有通过post提交任何表单)此页面或注销后，则返回初始表单
        form=login_form()
    context={"form":form,"register_info":register_info}
    return render(request,"login.html",context)#在1.10版本后使用Requestcontext就使用此方法(django.shortcuts render)即可

def logout_view(request):
    """
    处理用户注销，使用django的认证系统
    """
    auth.logout(request)
    return HttpResponseRedirect("/")

def register(request):
    """
    处理用户注册，使用django的内置表单
    """
    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            new_user=form.save()
            return HttpResponseRedirect("/Creating user scussefull/")
    else:
        form=UserCreationForm()
    context={"form":form}
    return render(request,"register.html", context)#在1.10版本后使用Requestcontext就使用此方法(django.shortcuts render)即可








