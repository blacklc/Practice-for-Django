#!/usr/bin/env python
#coding:utf-8

import os
import sys
from django.core.wsgi import get_wsgi_application

sys.path.append("/Users/lichen/Documents/workspace/djproject/src/djproject")
os.environ['DJANGO_SETTINGS_MODULE'] = 'djproject.settings'
application = get_wsgi_application()

from books.models import Author,Publisher,Book
# Create your tests here.
def main():
    """
    #插入数据
    a1=Author.objects.create(first_name="tom",last_name="cat",email="1235@sts.com")
    p1=Publisher.objects.create(name="Apress",
                                address="855 Telegraph Ave.",
                                city="beijing",
                                state_province="CA",
                                country="China")
    author_list=Author.objects.all()
    print author_list
    for author in author_list:
        print "Author%d:%s"%(author.id,author.first_name)
    """
    #查找数据
    #获取表中所有数据，返回一个对象集合
    author_list=Author.objects.all()
    for author in author_list:
        print "Author%d:%s"%(author.id,author.first_name)
    print "*******************************"
    #过滤查找。相当于sql的where语句
    print "filter search:"
    request_list=Author.objects.filter(last_name="mao")
    for author in request_list:
        print "Author%d:%s %s"%(author.id,author.first_name,author.last_name) 
    print "*******************************"
    #多重过滤，相当于sql的where a and b语句
    print "multi filter:"
    request_list=Author.objects.filter(first_name="li",last_name="mao")
    for author in request_list:
        print "Author%d:%s %s"%(author.id,author.first_name,author.last_name)
    print "*******************************"
    #模糊查找，相当于sql的like语句
    print "like search:"
    request_list=Author.objects.filter(first_name__contains="li")
    for author in request_list:
        print "Author%d:%s %s"%(author.id,author.first_name,author.last_name)
    print "*******************************"
    #查询获取单个对象
    print "get one data:"
    try:
        a_request=Author.objects.get(first_name="sun")
    except Author.DoesNotExist,err:
        print "select faild:%s"%err
    else:
        print "only request:%d %s %s"%(a_request.id,a_request.first_name,a_request.last_name)
    print "*******************************"
    #查询并排序结果，相当于sql中的order by 
    print "order request:"
    request_list=Author.objects.order_by("first_name")
    for author in request_list:
        print "Author%d:%s %s"%(author.id,author.first_name,author.last_name)
    print "*******************************" 
    #逆向排序
    print "turn order:"
    request_list=Author.objects.order_by("-first_name")
    for author in request_list:
        print "Author%d:%s %s"%(author.id,author.first_name,author.last_name)
    print "*******************************" 
    #组合查询
    print "filter+order search:"
    request_list=Author.objects.filter(first_name__contains="li").order_by("id")
    for author in request_list:
        print "Author%d:%s %s"%(author.id,author.first_name,author.last_name)
    print "*******************************" 
    #取结果集中的指定结果
    print "get first:"
    author=Author.objects.order_by("first_name")[0] #只取第一个结果
    print "Author%d:%s %s"%(author.id,author.first_name,author.last_name) 
    print "get last:"
    author=Author.objects.order_by("-first_name")[0] #只取最后一个结果，利用逆向排序
    print "Author%d:%s %s"%(author.id,author.first_name,author.last_name) 
    print "get 3:"
    request_list=Author.objects.order_by("first_name")[0:3] #只取前3个结果，利用切片
    for author in request_list:
        print "Author%d:%s %s"%(author.id,author.first_name,author.last_name)
    print "*******************************" 
    #通过外键反向查找
    print "通过外键反向查找:"
    p=Publisher.objects.get(name="Apress")
    #book_set属性是一个queryset对象;该属性命名由模型名称与_set组合而成。
    print p.book_set.all()
    #book_set属性是一个queryset对象；可以使用查询结果集的方法
    print p.book_set.filter(title="test book")
    print "*******************************"
    #查找多对多关系
    print "多对多关系查找:"
    b=Book.objects.get(title="test book")
    #多对多关系的查找结果是一个queryset对象集合
    print b.authors.all()
    for result in b.authors.all():
        print result.first_name,result.last_name
    #多对多反向查询
    a=Author.objects.get(first_name="jack") 
    #book_set属性是一个queryset对象;该属性命名由模型名称与_set组合而成;可以使用查询结果集的方法
    print a.book_set.all()
    print "*******************************"
    #测试自定义manager方法
    print "测试自定义manager方法:"
    #print Book.objects.title_count("test")
    print Book.personal_objects.all()
    print "*******************************"
    #测试模版方法
    print "测试模版方法"
    print Author.objects.get(first_name="jack").full_name
    print "*******************************"
    #测试自定义sql方法
    print "测试自定义sql方法"
    print Author.personal_objects.get_first_name("tomas")
    """
    request_list=Book.objects.filter(title="test book")
    for b in request_list:
        print "%s,%s,%s,%s"%(b.title,b.publisher,b.publication_date,b.authors)
    """
    #修改数据
    """
    print "update:"
    a=Author.objects.get(first_name="li",last_name="chen")
    a.email="sdlfwo@23123.com"
    a.save() #save方法是将该对象的所有属性(列)都更新一遍，效率不高，容易引起死锁
    #只更新对象的某一个属性.注意:update是结果集(QuerySet)的方法;并且update返回成功更新的条目数
    #注意：update()方法里可以写多个字段的更新 
    update_num=Author.objects.filter(first_name="li",last_name="chen").update(email="238497@skdfjls.com")
    print "there are %d data updated"%update_num
    print "*******************************" 
    """
    #删除数据
    """
    #删除单一数据
    a=Author.objects.get(first_name="lichen")
    a.delete()
    """
    """
    #删除多条数据
    Author.objects.filter(first_name__contains="li").delete()
    """
    
if __name__ == '__main__':  
    main()
 
 
 
 
 
 
 
 
 
 
 
    