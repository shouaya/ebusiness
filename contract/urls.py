# coding: UTF-8
"""
Created on 2017/04/24

@author: Yang Wanjun
"""

from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='contract-index'),
    url(r'^contract/(?P<api_id>[0-9]+).html$', views.ContractView.as_view(), name='contract_change'),
]