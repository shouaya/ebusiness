# coding: UTF-8
"""
Created on 2017/05/02

@author: Yang Wanjun
"""
from django import template

register = template.Library()


@register.tag(name='paging')
def paging(parser, token):
    try:
        tag_name, page_object = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires one arguments" % token.contents.split()[0])
    if page_object[0] == page_object[-1] and page_object[0] in ('"', "'"):
        raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)

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
                nodes.append(u'<a href="?page={0}{1}{2}">&lt;</a>'.format(page_object.previous_page_number, params, orders))
            if len(paginator.page_range) > 1:
                for page in paginator.page_range:
                    if page == page_object.number:
                        nodes.append(u'<span class="current">{0}</span>'.format(page))
                    else:
                        nodes.append(u'<a href="?page={0}{1}{2}">{0}</a>'.format(page, params, orders))
            if page_object.has_next():
                nodes.append(u'<a href="?page={0}{1}{2}">&gt;</a>'.format(page_object.next_page_number, params, orders))
            nodes.append(u'<span>{0} 件</span>'.format(paginator.count))
            nodes.append(u'</span>')
            nodes.append(u'</div>')
            html = "".join(nodes)
        return html
