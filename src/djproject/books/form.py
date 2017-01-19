#!/usr/bin/env python
#coding:utf-8

'''
Created on 2016年8月22日

@author: lichen
'''
from django import forms

class Contact_form(forms.Form):
    """
    自定义form类
    """
    subject=forms.CharField(max_length=100) #定义字符长度
    email=forms.EmailField(required=False,label="Your e-mail address") #此项选填,可使用label参数自定义<input>标签的name属性
    message=forms.CharField(widget=forms.Textarea) #将输入框定义Textarea类型
    
    def clean_message(self):
        """
        message字段自定义格式检验
        """
        message=self.cleaned_data["message"]
        num_words=len(message.split())
        if num_words<4:
            raise forms.ValidationError("Not enough words!") #抛出异常
        return message #必须有该返回项，否则将自动返回none，导致数据丢失
    
    def clean_email(self):
        """
        清洗email字段
        """
        email=self.cleaned_data["email"]
        if email=="":
            email="575784862@qq.com"
        return email
            
        
        
        
        
        
        
        