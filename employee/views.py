# coding: UTF-8
"""
Created on 2015/08/21

@author: Yang Wanjun
"""
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from eb.models import Company


def home(request):
    if Company.objects.all().count() == 0:
        return HttpResponseRedirect("/admin/eb/company/add/")
    else:
        return HttpResponseRedirect("/eb/")


def page_not_found(request):
    return render_to_response('404.html')