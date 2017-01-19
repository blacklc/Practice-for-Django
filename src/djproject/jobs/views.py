#!/usr/bin/env python
#coding:utf-8

# Create your views here.
from .models import Job
from django.shortcuts import get_object_or_404, render_to_response

"""
def index(request):
    object_list = Job.objects.order_by('-pub_date')[:10] #返回最近的10个job
    t = loader.get_template('jobs/job_list.html')        #调用模版
    c = Context({
        'object_list': object_list,
    })
    return HttpResponse(t.render(c))
"""

def job_index(request):
    """
    首页
    """
    object_list = Job.objects.order_by('-pub_date')[:10] #返回最近的10个job
    return render_to_response('templates/jobs/job_list.html', {'object_list': object_list})

def detail(request,object_id):
    """
    详细页面
    """
    job = get_object_or_404(Job, pk=object_id)
    print job
    return render_to_response('templates/jobs/job_detail.html',
                              {'object': job})