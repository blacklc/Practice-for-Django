#!/usr/bin/env python
#coding:utf-8

'''
Created on 2016年8月31日

@author: lichen
'''

import re
import datetime
from django import template
from books.models import Author,Publisher,Book

register=template.Library()

def cut(value,arg):
    """
    自定义模版过滤器：
    清除字符串中的所有特定字符
    """
    return value.replace(arg,"")

#注册自定义过滤器
register.filter("cut",cut)

def test_tag(parser,token):
    """
    自定义模版标签编译函数:
    显示当前时间
    """
    try:
        #token的split_contents将字符串按空格拆分同时保证引号内的字符串不拆分
        tag_name,format_str=token.split_contents()
    except:
        msg="%r tag requires a single argument" % token.split_contents[0]
        raise template.TemplateSyntaxError(msg)
    return test_Node(format_str[1:-1]) #利用切片将字符串中的第一和最后一个引号消除

class test_Node(template.Node):
    """
    自定义模版标签节点类型：
    显示当前时间
    """
    def __init__(self,format_string):
        self.format_str=str(format_string) #str方法返回一个可读性强的字符串
        
    def render(self,context):
        """
        重写render方法
        """
        now=datetime.datetime.now()
        return now.strftime(self.format_str) #使用规定的格式格式化时间

def test_tag2(parser,token):
    """
    设置和修改模版变量
    """
    try:
        tag_name,format_str=token.split_contents()
    except:
        msg="%r tag requires a single argument" % token.split_contents[0]
        raise template.TemplateSyntaxError(msg)
    return test_Node2(format_str[1:-1]) #利用切片将字符串中的第一和最后一个引号消除
    
class test_Node2(template.Node):
    """
    将当前时间保存在模版变量中
    """
    def __init__(self,fstr):
        self.format_string=str(fstr)
    
    def render(self,context):
        now=datetime.datetime.now()
        context["tag_context"]="test_tag2:"+now.strftime(self.format_string)
        return ""

def test_tag3(parser,token):
    """
    从自定义标签中提取模版变量名称和对应值
    """
    try:
        tag_name,arg=token.contents.split(" ",1) #按空格切分，并只切分1次
    except:
        msg="%r tag requires arguments" % token.contents[0]
        raise template.TemplateSyntaxError(msg)
    #使用正则提取模版变量名和对应值
    m=re.search(r'(.*?) as (\w+)',arg)
    if m:
        format_str,var_name=m.groups()
    else:
        msg="%r tag had invalid arguments" %tag_name
        raise template.TemplateSyntaxError(msg)
    #判断变量值前后是否有引号或双引号(是否填写规范)
    if not (format_str[0]==format_str[-1] and format_str[0] in ('"',"'")):
        msg="%r tag's argument should be in quotes" %tag_name
        raise template.TemplateSyntaxError(msg)
    return test_Node3(format_str[1:-1],var_name)

class test_Node3(template.Node):
    def __init__(self,fstr,var):
        self.format_string=str(fstr)
        self.var_name=var
    
    def render(self,context):
        now=datetime.datetime.now()
        context[self.var_name]="test_tag3:"+now.strftime(self.format_string)
        return ""

def test_comment(parser,token):
    """
    模拟模版多行注释标签
    """
    nodelist=parser.parse(("endtest_comment",)) #表示解析标签“endtestcomment”之前的所有内容；也可以添加多个结束标签名。
    parser.delete_first_token() #清除endtest_comment标签，防止被处理两次
    return test_comment_node()

class test_comment_node(template.Node):
    def render(self,context):
        """
        实现多行注释功能
        """
        return ""

@register.inclusion_tag("result_snippet.html",takes_context=True) #使包含标签可以使用context中的变量
def publisher_info(context):
    """
    包含标签编译函数：
    列出出版商的详细信息
    """
    info_map={}
    for b in context["object"]:
        p_querylist=Publisher.objects.filter(name=b.publisher)
        for p in p_querylist:
                if not p.name in info_map:
                    info_map[p.name]=p
    return {"publishers":info_map}

#注册自定义标签
register.tag("test_tag",test_tag)
register.tag("test_tag2",test_tag2)
register.tag("test_tag3",test_tag3)
register.tag("test_comment",test_comment)
#register.inclusion_tag("result_sinppet.html", publisher_info, takes_context=True,name=)






