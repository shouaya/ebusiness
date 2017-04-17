# coding: UTF-8
"""
Created on 2017/04/17

@author: Yang Wanjun
"""

from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='flow-index'),
    url(r'^new/(?P<workflow_id>[0-9]+).html$', views.NewWorkflowView.as_view(), name='new_workflow'),
]