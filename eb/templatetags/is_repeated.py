# coding: UTF-8
"""
Created on 2017/04/21

@author: Yang Wanjun
"""
from django import template


register = template.Library()


@register.simple_tag(takes_context=True, name='is_repeated')
def is_repeated(context, pk):
    if 'repeat_check_list' not in context:
        context['repeat_check_list'] = []
    if pk in context['repeat_check_list']:
        return True
    else:
        context['repeat_check_list'].append(pk)
        return False
