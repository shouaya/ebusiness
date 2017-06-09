# coding: UTF-8
"""
Created on 2017/04/14

@author: Yang Wanjun
"""
import re
from django import template

from eb import biz


register = template.Library()


@register.tag(name='year_month_filter')
def year_month_filter(parser, token):
    try:
        tag_name, context_year, context_month = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires two arguments" % token.contents.split()[0])
    # if not (year_name[0] == year_name[-1] and year_name[0] in ('"', "'")) or \
    #         not (month_name[0] == month_name[-1] and month_name[0] in ('"', "'")):
    #     raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)
    # if not re.match(r"[0-9]{4}", year_name) or not re.match(r"[0-9]{2}", month_name):
    #     raise template.TemplateSyntaxError("%s or %s is illegal year or month" % (year_name, month_name))

    return GenerateFilterTag(context_year, context_month)


class GenerateFilterTag(template.Node):
    def __init__(self, context_year, context_month):
        self.context_year = context_year
        self.context_month = context_month
        self.year_name = "_year"
        self.month_name = "_month"

    def render(self, context):
        year_list = biz.get_year_list()
        html = ""
        nodes = []
        current_year = context.get(self.context_year, None)
        current_month = context.get(self.context_month, None)
        if year_list and current_year and current_month:
            nodes.append(u"<span>対象年月：</span>")
            nodes.append(u'<select id="{0}" name="{0}">'.format(self.year_name))
            for y in year_list:
                if "%04d" % y == current_year:
                    nodes.append(u'<option selected value="{0}">{0}</option>'.format(y))
                else:
                    nodes.append(u'<option value="{0}">{0}</option>'.format(y))
            nodes.append(u'</select>')
            nodes.append(u'<select id="{0}" name="{0}">'.format(self.month_name))
            for m in range(1, 13):
                if "%02d" % m == current_month:
                    nodes.append(u'<option selected value="{0:02d}">{0:02d}</option>'.format(m))
                else:
                    nodes.append(u'<option value="{0:02d}">{0:02d}</option>'.format(m))
            nodes.append(u'</select>')

            html = "".join(nodes)
        return html
