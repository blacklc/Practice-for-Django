#!/usr/bin/env python
#coding:utf-8

from django.contrib import admin
from books.models import Book,Publisher,Author

# Register your models here.
class Author_Admin(admin.ModelAdmin):
    """
    Author管理类
    """
    list_display=("first_name","last_name","email")
    search_fields=("first_name","last_name","email")

class Publisher_Admin(admin.ModelAdmin):
    """
    Publisher管理类
    """
    list_display=("name","address","city","state_province","country","website")
    search_fields=("name",)
    
class Book_Admin(admin.ModelAdmin):
    """
    Book管理类
    """
    list_display=("title","publisher","publication_date") #多对多属性不能在list_display中显示
    search_fields = ("title", "author","publisher") #可根据指定属性进行查找
    list_filter=("publication_date",) #根据指定属性添加过滤器
    date_hierarchy = 'publication_date' #增加深度过滤
    ordering=("-publication_date",) #按时间排序(倒序)
    fields = ('title', 'authors', 'publisher') #自定义管理页面表单

#将类添加到管理工具    
admin.site.register(Book, Book_Admin)
admin.site.register(Publisher, Publisher_Admin)
admin.site.register(Author, Author_Admin)
