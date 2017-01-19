#!/usr/bin/env python
#coding:utf-8

from __future__ import unicode_literals
from django.db import models

# Create your models here.
"""
设计类时需要注意：template内只能调用不含参数的类方法
"""
class Location(models.Model):
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50)

    def __str__(self):
        if self.state:
            return "%s, %s, %s" % (self.city, self.state, self.country)
        else:
            return "%s, %s" % (self.city, self.country)
        
class Job(models.Model):
    pub_date = models.DateField()
    job_title = models.CharField(max_length=50)
    job_description = models.TextField()
    location = models.ForeignKey(Location)

    def __str__(self):
        return "%s (%s)" % (self.job_title, self.location)