#!/usr/bin/env python
#coding:utf-8

'''
Created on 2016年8月29日

@author: lichen
'''

def custom_proc(request):
    """
    自定义context_processors
    """
    return {
            "context_test":"test"
            }