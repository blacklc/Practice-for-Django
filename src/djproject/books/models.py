#!/usr/bin/env python
#coding:utf-8

from __future__ import unicode_literals
from django.db import models,connection

# Create your models here.
class Publisher(models.Model):
    """
    出版商模型
    """
    name=models.CharField(max_length=30)
    address=models.CharField(max_length=50)
    city=models.CharField(max_length=60)
    state_province=models.CharField(max_length=30)
    country=models.CharField(max_length=50)
    website=models.URLField()
    
    def __unicode__(self):
        """
        将对象以unicode方式展现
        """
        return self.name
    
    class Meta:
        """
        设定模型特定选项
        """
        #自动排序结果集
        ordering=['name']

class authorManager(models.Manager):
    """
    author自定义manager方法
    使用django自带的sql接口
    """
    def get_first_name(self,last_name):
        """
        依据last_name查询first_name
        """
        cursor=connection.cursor()
        sql="select distinct first_name from books_author where last_name=%s"
        data=["tomas"]
        cursor.execute(sql,data)
        query_list=cursor.fetchone()
        return query_list
    
class Author(models.Model):
    """
    作者模型
    """
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=40)
    email=models.EmailField(blank=True,verbose_name="E-mail") #可选填,自定义管理页面中标签名
    last_accessed=models.DateField(blank=True,null=True)
    objects=models.Manager() #若想使用多个自定义manager，需要将objects属性设置成默认实例
    personal_objects=authorManager() #自定义manager
    
    def __unicode__(self):
        """
        将对象以unicode方式展现
        """
        return u"%s,%s" %(self.first_name,self.last_name)
    
    def get_fullname(self):
        """
        自定义模版方法
        获取作者全名
        """
        return u"%s %s" %(self.first_name,self.last_name)
    
    #property属性
    full_name=property(get_fullname)
    
    class Meta:
        """
        设定模型特定选项
        """
        #自动排序结果集
        ordering=['first_name']

class BookManager(models.Manager):
    """
    book自定义manager方法
    """
    def title_count(self,keyword):
        """
        计算书名包含某一关键字的书的数量
        """
        return self.filter(title__icontains=keyword).count() #__icontains:关键字

class personal_bookmanager(models.Manager):
    """
    重写Manager中的部分方法
    """
    def get_queryset(self):
        return super(personal_bookmanager,self).get_queryset().filter(authors=3) #注意:这里如果使用外键或者多对多关系过滤的时候，填写的过滤条件与数据库中存储的对应关系一致，而不是填写具体内容
    
class Book(models.Model):
    """
    书模型
    """
    title=models.CharField(max_length=100)
    authors=models.ManyToManyField(Author)
    publisher=models.ForeignKey(Publisher)
    publication_date=models.DateField(blank=True,null=True) #指定日期和数字型的可选填需要两个参数
    num_pages=models.IntegerField(blank=True,null=True)
    #objects=BookManager() #将自定义manager类赋值给objects属性，取代默认的manager方法
    objects=models.Manager() #若想使用多个自定义manager，需要将objects属性设置成默认实例
    personal_objects=personal_bookmanager() #自定义manager

    def __unicode__(self):
        """
        将对象以unicode方式展现
        """
        return self.title
    
    class Meta:
        """
        设定模型特定选项
        """
        #自动排序结果集
        ordering=['title']











