# coding: UTF-8
"""
Created on 2015/08/25

@author: Yang Wanjun
"""
import re
import datetime
import calendar


def add_months(source_date, months=1):
    month = source_date.month - 1 + months
    year = int(source_date.year + month / 12)
    month = month % 12 + 1
    day = min(source_date.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


def get_release_months(cnt):
    if not cnt:
        cnt = 3

    now = datetime.date.today()
    release_month_list = []
    for i in range(cnt):
        next_month = add_months(now, i)
        release_month_list.append((next_month.year, next_month.month))

    return release_month_list


def get_ordering_dict(data, fields):
    """ＵＲＬからの引数を解析し、並び順を取得する。

    Arguments：
      data: 解析対象の引数の内容

    Returns：
      dict

    Raises：
      なし
    """
    d = {}
    if not data:
        data = ""

    order_list = data.split(".")

    for i, order in enumerate(fields):
        is_asc = False if order in order_list else True
        priority = get_order_priority(data, order)
        is_in_ordering = True if order in [field.lstrip("-") for field in data.split(".")] else False
        url_list = get_ordering_list(data, order)
        url_removed = None
        if is_in_ordering:
            url_removed = ".".join(get_order_removed(data, order))
        d[order] = {'is_asc': is_asc,
                    'priority': priority,
                    'url': ".".join(url_list),
                    'is_in_ordering': is_in_ordering,
                    'url_list_removed': url_removed}

    return d


def get_order_removed(data, field):
    if not data or not field:
        return []

    if not data:
        data = ""

    order_list = [order.lstrip("-") for order in data.split(".")]
    if field in order_list:
        order_list.remove(field)
    return order_list


def get_order_priority(data, field):
    if not data:
        data = ""

    order_list = [order.lstrip("-") for order in data.split(".")]
    if field in order_list:
        return order_list.index(field) + 1

    return None


def get_ordering_list(data, field=None):

    if not data:
        data = ""

    if not field:
        if not data:
            return []
        else:
            return data.split(".")

    d = {}
    for j, order in enumerate(data.split(".")):
        m = re.match("^(-?)(\w+)$", order)
        if m:
            d[m.group(2)] = (j, order)

    field_name = re.match("^(-?)(\w+)$", field).group(2)

    def get_new_orders():
        temp_list = []
        i = 1
        for o, n in orders:
            if n == field_name:
                temp_list.append("-" + field_name)
            elif n == "-" + field_name:
                temp_list.append(field_name)
        for o, n in orders:
            if n.lstrip("-") != field_name:
                temp_list.append(n)
                i += 1
        return temp_list

    if isinstance(d, dict):
        orders = d.values()
        orders.sort(key=lambda it: it[0])
        if field_name in d:
            new_orders = get_new_orders()
            return new_orders
        else:
            new_orders = [field_name]
            k = 1
            for o1, n1 in orders:
                new_orders.append(n1)
                k += 1
            return new_orders


if __name__ == "__main__":
    # ls = get_ordering_list("-name.age.-second", "-aaa_3")
    # print ".".join(ls)

    print get_ordering_dict("name", ['name', 'first'])