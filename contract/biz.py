# coding: UTF-8
"""
Created on 2017/04/24

@author: Yang Wanjun
"""
from django.db.models import Prefetch
from eb import models as sales_models
from . import models


def get_members():
    queryset = sales_models.Member.objects.all()
    contract_set = models.Contract.objects.filter(
        is_deleted=False
    ).exclude(status='04').order_by('-employment_date', '-contract_no')
    return queryset.prefetch_related(
        Prefetch('contract_set', queryset=contract_set, to_attr='latest_contract_set')
    )


def get_latest_contract(member):
    contract_set = member.contract_set.filter(
        is_deleted=False
    ).exclude(status='04').order_by('-employment_date', '-contract_no')
    return contract_set
