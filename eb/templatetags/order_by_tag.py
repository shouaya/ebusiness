# coding: UTF-8
"""
Created on 2017/01/26

@author: Yang Wanjun
"""
from django import template


register = template.Library()


@register.tag(name='create_order_display')
def create_order_display(parser, token):
    try:
        tag_name, display_name, dict_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    if not (display_name[0] == display_name[-1] and display_name[0] in ('"', "'")) or \
            not (dict_name[0] == dict_name[-1] and dict_name[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)

    return GenerateOrderTag(display_name[1:-1], dict_name[1:-1])


class GenerateOrderTag(template.Node):
    def __init__(self, display_name, dict_name):
        self.display_name = display_name
        self.dict_name = dict_name

    def render(self, context):
        if 'dict_order' not in context:
            return self.display_name
        elif self.dict_name not in context['dict_order']:
            return self.display_name
        else:
            dict_order = context['dict_order']
            order_name = dict_order.get(self.dict_name)
            params = context.get('params', '')
            html = u""
            if order_name.get('is_in_ordering', False):
                html += u"""<div class="sortoptions">
                               <a class="sortremove" href="?o={0}{1}"></a>
                               <span class="sortpriority">{2}</span>
                               <a class="{3}"
                                  href="?o={4}{1}"></a>
                           </div>""".format(order_name.get('url_list_removed'),
                                            params,
                                            order_name.get('priority'),
                                            'descending' if order_name.get('is_asc', False) else 'ascending',
                                            order_name.get('url'))
            html += u"""<div class="text"><a href="?o={0}{1}">{2}</a></div>
                        <div class="clear"></div>
                    """.format(order_name.get('url'),
                                                             params,
                                                             self.display_name)
        return html
