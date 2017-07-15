# coding: UTF-8
"""
Created on 2017/04/24

@author: Yang Wanjun
"""
from django.db.models import Prefetch, Subquery, OuterRef, CharField
from eb import models as sales_models
from . import models


def get_members():
    contract_set = models.Contract.objects.filter(
        is_deleted=False
    ).exclude(status='04').order_by('-employment_date', '-contract_no')
    queryset = sales_models.Member.objects.all().annotate(
        contract_member_type=Subquery(
            models.Contract.objects.filter(
                is_deleted=False, member=OuterRef('pk')
            ).exclude(status='04').order_by(
                '-employment_date', '-contract_no'
            ).values('member_type')[:1],
            output_field=CharField()
        ),
        endowment_insurance=Subquery(
            models.Contract.objects.filter(
                is_deleted=False, member=OuterRef('pk')
            ).exclude(status='04').order_by(
                '-employment_date', '-contract_no'
            ).values('endowment_insurance')[:1],
            output_field=CharField()
        )
    )
    return queryset.prefetch_related(
        Prefetch('contract_set', queryset=contract_set, to_attr='latest_contract_set')
    )


def get_latest_contract(member):
    contract_set = member.contract_set.filter(
        is_deleted=False
    ).exclude(status='04').order_by('-employment_date', '-contract_no')
    return contract_set
