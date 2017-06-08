# coding: UTF-8
"""
Created on 2017/05/02

@author: Yang Wanjun
"""
from __future__ import unicode_literals
import datetime
from django import template

from utils import common
from eb import biz

register = template.Library()


@register.tag(name='paging')
def paging(parser, token):
    try:
        tag_name, page_object = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires one arguments" % token.contents.split()[0])
    if page_object[0] == page_object[-1] and page_object[0] in ('"', "'"):
        raise template.TemplateSyntaxError("%r tag's argument should not be in quotes" % tag_name)

    return GeneratePagingTag(page_object)


class GeneratePagingTag(template.Node):
    def __init__(self, page_object_name):
        self.page_object_name = page_object_name

    def render(self, context):
        paginator = context.get('paginator', None)
        page_object = context.get(self.page_object_name, None)
        html = ''
        if paginator and page_object:
            params = context.get('params', '')
            orders = context.get('orders', '')
            nodes = list()
            nodes.append(u'<div class="pagination">')
            nodes.append(u'<span class="step-links">')
            if page_object.has_previous():
                nodes.append(u'<a href="?page={0}{1}{2}">&lt;</a>'.format(page_object.previous_page_number(), params, orders))
            if len(paginator.page_range) > 1:
                for page in paginator.page_range:
                    if page == page_object.number:
                        nodes.append(u'<span class="current">{0}</span>'.format(page))
                    else:
                        nodes.append(u'<a href="?page={0}{1}{2}">{0}</a>'.format(page, params, orders))
            if page_object.has_next():
                nodes.append(u'<a href="?page={0}{1}{2}">&gt;</a>'.format(page_object.next_page_number(), params, orders))
            nodes.append(u'&nbsp;<span>{0} 件</span>'.format(paginator.count))
            nodes.append(u'</span>')
            nodes.append(u'</div>')
            html = "".join(nodes)
        return html


@register.tag(name='organization_filter')
def organization_filter(parser, token):
    try:
        tag_name, ele_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires one arguments" % token.contents.split()[0])
    if ele_name[0] == ele_name[-1] and ele_name[0] in ('"', "'"):
        ele_name = ele_name[1:-1]
    else:
        raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)

    return GenerateOrganizationFilter(ele_name)


class GenerateOrganizationFilter(template.Node):
    def __init__(self, ele_name):
        self.ele_name = ele_name

    def render(self, context):
        top_org_list = biz.get_on_sales_top_org()
        nodes = list()
        nodes.append('<select id="{0}" name="{0}">'.format(self.ele_name))
        nodes.append('<option value="">======部署======</option>')
        for org in top_org_list:
            if org.children.count() == 0:
                nodes.append('<option value="%s">%s</option>' % (org.pk, unicode(org)))
            else:
                nodes.append('<option class="group" value="%s">%s</option>' % (org.pk, unicode(org)))
                for sec in org.children.all():
                    if sec.children.count() == 0:
                        nodes.append('<option value="%s">%s%s</option>' % (sec.pk, '&nbsp;' * 4, unicode(sec)))
                    else:
                        nodes.append('<option class="group" value="%s">%s%s</option>' % (sec.pk, '&nbsp;' * 4, unicode(sec)))
                        if sec.children.count() > 0:
                            for sub_sec in sec.children.all():
                                nodes.append('<option value="%s">%s%s</option>' % (sub_sec.pk, '&nbsp;' * 8, unicode(sub_sec)))
        nodes.append('</select>')
        return "".join(nodes)


@register.simple_tag()
def is_belong_to(user, member, year, month, *args, **kwargs):
    date = datetime.date(int(year), int(month), 1)
    return member.is_belong_to(user, date)


@register.simple_tag()
def get_default_bp_order_no(year, month, *args, **kwargs):
    date = common.get_bp_order_publish_date(year, month, None)
    return date.strftime('%Y/%m/%d')
