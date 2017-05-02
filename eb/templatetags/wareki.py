# coding: UTF-8
"""
Created on 2017/04/26

@author: Yang Wanjun
"""
from django.template.defaultfilters import register
from utils import common


@register.filter
def to_wareki(date):
    return common.to_wareki(date)
