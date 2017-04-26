# coding: UTF-8
"""
Created on 2017/04/26

@author: Yang Wanjun
"""
from django.template.defaultfilters import register


@register.filter
def to_wareki(date):
    if 1926 <= date.year <= 1988:
        prefix = u"昭和"
        years = date.year - 1925
    elif 1989 <= date.year:
        prefix = u"平成"
        years = date.year - 1988
    else:
        prefix = ''
        years = date.year
    return u"%s%s年%02d月%02d日" % (prefix, years, date.month, date.day)
