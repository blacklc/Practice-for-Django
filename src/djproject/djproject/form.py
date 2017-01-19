#!/usr/bin/env python
#coding:utf-8

'''
Created on 2016年8月22日

@author: lichen
'''
from django import forms

class login_form(forms.Form):
    """
    用户登陆表单类
    """
    username=forms.CharField(max_length=100) #定义字符长度
    password=forms.CharField(max_length=100) #此项选填,可使用label参数自定义<input>标签的name属性
    error=None #自定义错误
    
    def clean_username(self):
        """
        username字段格式检验
        """
        special_characters=["!","@","#","$","%","^","&","*"]
        username=self.cleaned_data["username"]
        for character in special_characters:
            if character in username:
                raise forms.ValidationError("Don't input special characters!") #抛出异常
        return username #必须有该返回项，否则将自动返回none，导致数据丢失
    
            
        
        
        
        
        
        
        