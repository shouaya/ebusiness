# coding: UTF-8
"""
Created on 2017/04/24

@author: Yang Wanjun
"""

from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='contract-index'),
    url(r'^contract_change/(?P<api_id>[0-9]+).html$', views.ContractChangeView.as_view(), name='contract_change'),
    url(r'^contract/(?P<contract_id>[0-9]+).html$', views.ContractView.as_view(),
        name='contract'),
    url(r'^contract/(?P<member_id>[0-9]+)/certificate.html$', views.CertificateView.as_view(), name='certificate'),
    url(r'^contract/(?P<member_id>[0-9]+)/income.html$', views.IncomeView.as_view(), name='income'),
    url(r'^member/(?P<member_id>[0-9]+)/gen_api_id.html$', views.GenerateApiIdView.as_view(), name='gen_api_id'),
    url(r'^member_change/(?P<member_id>[0-9]+).html$', views.MemberChangeView.as_view(), name='member_change'),
    url(r'^member/add.html$', views.MemberChangeView.as_view(), name='member_add'),
]
