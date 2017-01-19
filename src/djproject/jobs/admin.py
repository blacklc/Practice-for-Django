#!/usr/bin/env python
#coding:utf-8

from django.contrib import admin
from jobs.models import Location,Job

# Register your models here.
class Location_Admin(admin.ModelAdmin):
    """
    Location管理类
    """
    list_display = ("city", "state", "country")   

class Job_Admin(admin.ModelAdmin):
    """
    Job管理类
    """
    list_display=("pub_date","job_title","job_description","location")
    ordering = ["-pub_date"] #指定排序规则:按照日期降序排序
    search_fields = ("job_title", "job_description") #可根据指定属性进行查找
    list_filter = ("location",)
    
#将类添加到管理工具    
admin.site.register(Location, Location_Admin)
admin.site.register(Job, Job_Admin)