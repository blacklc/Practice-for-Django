#!/usr/bin/env python
#coding:utf-8

from django.utils import timezone
from django.core.mail import send_mail
from django.shortcuts import render_to_response,Http404,render
from books.models import Author,Publisher,Book
from django.http.response import  HttpResponseRedirect
from books.form import Contact_form
from django.views.generic import ListView,DetailView

# Create your views here.

class author_listview(DetailView):
    """
    重写django的通用视图DetailView(该通用视图主要是返回单一对象信息)
    列举author信息
    """
    model=Author
    template_name="list_author.html"
    #context_object_name="author_list"
    slug_field="first_name" #filter中需要查询的表中字段名
    slug_url_kwarg="fn" #url传的参数名
    
    def get_queryset(self):
        """
        重写get_queryset方法
        设置查询结果，自定义显示内容
        """
        queryset=Author.objects.filter(first_name=self.kwargs["fn"])
        return queryset
    
    def get_object(self):
        """
        重写get_object方法
        实现更新后台数据
        """
        object=super(author_listview,self).get_object()
        object.last_accessed=timezone.now()
        object.save()
        return object
           
    def get_context_data(self, **kwargs):
        """
        重写get_context_data方法
        返回需要列举对象的渲染数据(context)
        """
        #queryset=Author.objects.filter(first_name=self.kwargs["first_name"])
        #kwargs["object_list"]=queryset #自定义显示内容
        context=super(author_listview,self).get_context_data(**kwargs)
        context["author_list"]=Author.objects.filter(first_name=self.kwargs["fn"])
        context["extra_context"]=Book.objects.filter(authors__first_name=self.kwargs["fn"]) #通过双下划线来指定外键对应表中的域来查找符合条件的对象
        return context
    
class publisher_listview(ListView):
    """
    重写django的通用视图ListView(该通用视图主要是返回多个对象信息)
    列举publisher信息
    """
    model=Publisher #指定列举对象的模版。此语句相当于是 queryset = Publisher.objects.all()
    #queryset=Publisher.objects.all() #设定需要显示的对象结果集
    #queryset=Publisher.objects.order_by("city") #自定义显示内容:显示对象的子集
    template_name="list_publisher.html" #指定需要渲染的模版
    context_object_name="publisher_list" #指定context中对象队列的名称
    
    def get_queryset(self):
        """
        重写get_queryset方法
        设置查询结果，自定义显示内容
        """
        queryset=Publisher.objects.filter(name=self.kwargs["pname"]) #接受URL中传递的参数(命名组参数保存在self.kwargs中，无名参数保存在self.args中)
        return queryset
    
    def get_context_data(self,**kwargs):
        """
        重写get_context_data方法
        返回需要列举对象的渲染数据(context)
        """
        context=super(publisher_listview,self).get_context_data(**kwargs)
        context["extra_context"]=Book.objects.filter(publisher__name=self.kwargs["pname"]) #通过双下划线来指定外键对应表中的域来查找符合条件的对象
        #context["extra_context"]=Book.objects.all() #自定义context，使得通用视图返回的context中有更多的信息
        return context
        
def method_splitter(request,*args,**kwargs):
    """
    通用视图:根据请求方法调用指定视图
    """
    get_view=kwargs.pop("GET",None)
    post_view=kwargs.pop("POST",None)
    if request.method=="GET" and get_view is not None:
        return get_view(request,*args,**kwargs)
    elif request.method=="POST" and post_view is not None:
        return post_view(request,*args,**kwargs)
    raise Http404

def index_thank(request,template="",context=""):
    #从URL传过来的变量都为字符串类型 ?此项需要验证
    return render_to_response(template,context)

def search(request):
    #错误信息队列
    error=[]
    #判断是否是首次登陆到此应用(页面)
    if "book_title" in request.GET:
        #判断前台输入是否为空
        if not request.GET["book_title"]:
            error.append("Please enter a search term")
        elif len(request.GET["book_title"])>20:
            error.append("Please enter at most 20 characters.")
        else:
            search_request=Book.objects.filter(title=request.GET["book_title"])
            return render_to_response("search_request.html",{"object":search_request})
    #当前前台输入的字符串为空时重定向到当前页面
    return render_to_response("search_from.html", {"error":error})

def contact(request):
    #判断是否是首次登陆到此应用(页面)
    if request.method=="POST":
        form=Contact_form(request.POST)
        #判断用户输入是否合法；若合法则返回干净数据
        if form.is_valid():
           form_context=form.cleaned_data
           send_mail(
                form_context["subject"],
                form_context["message"],
                form_context["email"],
                ["li_chen6@founder.com.cn"],
            )
           return HttpResponseRedirect("/books/contact/thanks/")
    else:
        form=Contact_form(
                initial={
                         "subject":"subject's max length is 100",   #初始化表单
                         "email":"please input email address",
                         "message":"please input message",
                        })
    #方法一:不使用csrf
    #return render_to_response("contact_form.html",{"form":form})
    #方法二:使用csrf情况下;使用requestcontext渲染模版;在1.10版本后使用Requestcontext就使用此方法(django.shortcuts render)即可
    #若需要使用context_processors，则在settings中context_processors内注册好自定义的context_processor即可
    context={"form":form}
    return render(request,"contact_form.html",context)
      
    """
    error=[]
    #判断是否是首次登陆到此应用(页面)
    if request.method=="POST":
        #必填项
        if not request.POST.get("subject",""):  #get():如果取到返回values；若没有键则给该键赋值逗号后的值
            error.append("Please Enter subject")
        if not request.POST.get("message",""):
            error.append("Please Enter message")
        #选填项
        if request.POST.get("email") and "@" not in request.POST["email"]:
            error.append("Enter a valid e‐mail address.")
        if not request.POST.get("email"):
            from_addr="575784862@qq.com"
        else:
            from_addr=request.POST["email"]
        if not error:
            send_mail(
                request.POST["subject"],
                request.POST["message"],
                from_addr, 
                ["li_chen6@founder.com.cn"],
            )
            return HttpResponseRedirect("/books/contact/thanks/")
    #返回错误信息，并将用户原有输入数据返回 
    return render_to_response(
                "contact_form.html",
                {"error":error,
                "subject":request.POST.get("subject",""),
                "message":request.POST.get("message",""),
                "email":request.POST.get("email",""),
            })
    """
    
    
    
    
    
    
    
    
    