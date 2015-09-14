# coding: UTF-8
"""
Created on 2015/08/25

@author: Yang Wanjun
"""
import io
import os
import re
import datetime
import calendar

import pythoncom
import win32com.client


EXCEL_APPLICATION = "Excel.Application"
EXCEL_FORMAT_EXCEL2003 = 56

MARK_POST_CODE = u"〒"

DOWNLOAD_REQUEST = "request"


def add_months(source_date, months=1):
    month = source_date.month - 1 + months
    year = int(source_date.year + month / 12)
    month = month % 12 + 1
    day = min(source_date.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


def get_last_day_by_month(source_date):
    next_month = add_months(source_date, 1)
    return next_month + datetime.timedelta(days=-source_date.day)


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


def generate_request(project, company):
    """請求書を出力する。

    Arguments：
      data: 解析対象の引数の内容

    Returns：
      dict

    Raises：
      なし
    """
    pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
    template_book = get_excel_template(DOWNLOAD_REQUEST)
    template_sheet = template_book.Worksheets(1)
    book = get_new_book()
    cnt = book.Sheets.Count
    # テンプレートを生成対象ワークブックにコピーする。
    template_sheet.Copy(None, book.Worksheets(cnt))
    template_book.Close()
    sheet = book.Worksheets(cnt + 1)

    sheet.Range("POS_CLIENT_POST_CODE").Value = MARK_POST_CODE + project.client.post_code
    sheet.Range("POS_CLIENT_ADDRESS").Value = project.client.address1 + project.client.address2
    sheet.Range("POS_CLIENT_TEL").Value = "Tel: " + project.client.tel
    sheet.Range("POS_CLIENT_COMPANY").Value = project.client.name
    now = datetime.date.today()
    first_day = datetime.date(now.year, now.month, 1)
    last_day = get_last_day_by_month(now)
    period = u"%s年%s月%s日 ～ %s年%s月%s日" % (first_day.year, first_day.month, first_day.day,
                                         last_day.year, last_day.month, last_day.day)
    sheet.Range("POS_WORK_PERIOD").Value = period
    sheet.Range("POS_REQUEST_DATE").Value = last_day
    sheet.Range("POS_CONTRACT_NAME").Value = project.name
    next_month = add_months(now, 1)
    sheet.Range("POS_REMIT_DATE").Value = get_last_day_by_month(next_month)
    sheet.Range("POS_PUBLISH_DATE").Value = now
    sheet.Range("POS_POST_CODE").Value = MARK_POST_CODE + company.post_code
    sheet.Range("POS_ADDRESS").Value = company.address1 + company.address2
    sheet.Range("POS_COMPANY_NAME").Value = company.name
    member = company.get_master()
    sheet.Range("POS_MASTER").Value = u"%s %s" % (member.first_name, member.last_name) if member else ""
    sheet.Range("POS_TEL").Value = company.tel

    project_members = project.get_project_members_current_month()
    members_amount = 0
    for project_member in project_members:
        members_amount += project_member.price
    sheet.Range("POS_MEMBERS_AMOUNT").Value = members_amount

    for i in range(cnt, 0, -1):
        book.Worksheets(i).Delete()
    return save_and_close_book(book, DOWNLOAD_REQUEST)


def get_excel_template(name):
    path_file = os.path.join(get_template_folder(), "%s.xls" % (name,))
    if not os.path.exists(path_file):
        return None

    xl_app = win32com.client.dynamic.Dispatch(EXCEL_APPLICATION)
    xl_app.DisplayAlerts = False
    xl_app.Visible = 0
    book = xl_app.Workbooks.Open(path_file)
    return book


def get_new_book():
    xl_app = win32com.client.dynamic.Dispatch(EXCEL_APPLICATION)
    xl_app.DisplayAlerts = False
    xl_app.Visible = 0
    book = xl_app.Workbooks.Add()
    return book


def get_template_folder():
    path_root = os.path.dirname(os.path.abspath(__file__))
    path_folder = os.path.join(path_root, "templates")
    return path_folder


def save_and_close_book(book, name):
    file_folder = get_template_folder()
    file_name = "tmp_%s_%s.xls" % (name, datetime.datetime.now().strftime("%Y%m%d_%H%M%S%f"))
    path = os.path.join(file_folder, file_name)
    # 保存
    book.SaveAs(path, FileFormat=EXCEL_FORMAT_EXCEL2003)
    return path


if __name__ == "__main__":
    # ls = get_ordering_list("-name.age.-second", "-aaa_3")
    # print ".".join(ls)

    print get_ordering_dict("name", ['name', 'first'])