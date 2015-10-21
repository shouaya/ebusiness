# coding: UTF-8
"""
Created on 2015/08/25

@author: Yang Wanjun
"""
import os
import re
import sys
import datetime
import calendar
import xlsxwriter
import StringIO

import constants
import errors

try:
    import pythoncom
    import win32com.client
except:
    pass


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
      FileNotExistException
    """
    pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
    if not project.client.request_file:
        raise errors.FileNotExistException(constants.ERROR_TEMPLATE_NOT_EXISTS)

    template_book = get_excel_template(project.client.request_file.path)
    template_sheet = template_book.Worksheets(1)
    book = get_new_book()
    cnt = book.Sheets.Count
    # テンプレートを生成対象ワークブックにコピーする。
    template_sheet.Copy(None, book.Worksheets(cnt))
    template_book.Close()
    sheet = book.Worksheets(cnt + 1)

    sheet.Range("POS_CLIENT_POST_CODE").Value = constants.MARK_POST_CODE + project.client.post_code
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
    sheet.Range("POS_POST_CODE").Value = constants.MARK_POST_CODE + company.post_code
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

    file_folder = os.path.join(os.path.dirname(project.client.request_file.path), "temp")
    if not os.path.exists(file_folder):
        os.mkdir(file_folder)
    file_name = "tmp_%s_%s.xls" % (constants.DOWNLOAD_REQUEST, datetime.datetime.now().strftime("%Y%m%d_%H%M%S%f"))
    path = os.path.join(file_folder, file_name)
    book.SaveAs(path, FileFormat=constants.EXCEL_FORMAT_EXCEL2003)

    return path


def get_excel_template(path_file):
    if not os.path.exists(path_file):
        raise errors.FileNotExistException(constants.ERROR_TEMPLATE_NOT_EXISTS)

    xl_app = win32com.client.dynamic.Dispatch(constants.EXCEL_APPLICATION)
    xl_app.DisplayAlerts = False
    xl_app.Visible = 0
    book = xl_app.Workbooks.Open(path_file)
    return book


def get_new_book():
    xl_app = win32com.client.dynamic.Dispatch(constants.EXCEL_APPLICATION)
    xl_app.DisplayAlerts = False
    xl_app.Visible = 0
    book = xl_app.Workbooks.Add()
    return book


def generate_business_plan(projects, filename):
    # create a workbook in memory
    output = StringIO.StringIO()
    row = 1
    col = 1

    book = xlsxwriter.Workbook(output)
    sheet = book.add_worksheet()
    # 見出しを書き込む
    title_format = book.add_format({'bold': True,
                                    'font_color': 'white',
                                    'bg_color': '#8db4e2',
                                    'border': 1})
    sheet.write(row + 1, col, u"顧客", title_format)
    sheet.set_column(get_excel_col_entire(col), 11)
    sheet.write(row + 1, col + 1, u"窓口", title_format)
    sheet.set_column(get_excel_col_entire(col + 1), 11)
    sheet.write(row + 1, col + 2, u"現場", title_format)
    sheet.set_column(get_excel_col_entire(col + 2), 11)
    sheet.write(row + 1, col + 3, u"部門", title_format)
    sheet.set_column(get_excel_col_entire(col + 3), 12)
    sheet.write(row + 1, col + 4, u"リーダー", title_format)
    sheet.set_column(get_excel_col_entire(col + 4), 12)
    sheet.write(row + 1, col + 5, u"メンバー", title_format)
    sheet.set_column(get_excel_col_entire(col + 5), 12)
    sheet.write(row + 1, col + 6, u"所属", title_format)
    sheet.set_column(get_excel_col_entire(col + 6), 6)
    sheet.write(row + 1, col + 7, u"入場時期", title_format)
    sheet.set_column(get_excel_col_entire(col + 7), 16)
    sheet.write(row + 1, col + 8, u"終了予定", title_format)
    sheet.set_column(get_excel_col_entire(col + 8), 16)
    sheet.write(row + 1, col + 9, u"現状・確認点", title_format)
    sheet.set_column(get_excel_col_entire(col + 9), 12)
    sheet.write(row + 1, col + 10, u"担当", title_format)
    sheet.set_column(get_excel_col_entire(col + 10), 12)
    sheet.write(row + 1, col + 11, u"進み状況", title_format)
    sheet.set_column(get_excel_col_entire(col + 11), 12)
    sheet.write(row + 1, col + 12, u"解決", title_format)
    sheet.set_column(get_excel_col_entire(col + 12), 12)

    # 詳細を書き込む
    cell_format = book.add_format({'bold': True,
                                   'border': 1})
    bp_format = book.add_format({'bold': True,
                                 'bg_color': 'yellow',
                                 'border': 1})
    date_format = book.add_format({'num_format': u'yyyy年mm月dd日',
                                   'bold': True,
                                   'border': 1})
    i = 0
    for project in projects:
        if project.members.all().count() == 0:
            continue
        # 顧客
        sheet.write(row + 2 + i, col + 0, project.client.name, cell_format)
        # 窓口
        sheet.write(row + 2 + i, col + 1, project.middleman.name, cell_format)
        sheet.write(row + 2 + i, col + 2, project.address, cell_format)
        first_project_member = project.get_first_project_member()
        sheet.write(row + 2 + i, col + 3, first_project_member.member.section.name, cell_format)
        member_name = first_project_member.member.__unicode__()
        position_ship = first_project_member.member.get_position_ship()
        member_name = u"%s(%s)" % (member_name, position_ship.get_position_display()) if position_ship else member_name
        if first_project_member.role >= 6:
            sheet.write(row + 2 + i, col + 4, member_name,
                        bp_format if first_project_member.member.subcontractor else cell_format)
            sheet.write(row + 2 + i, col + 5, "", cell_format)
        else:
            sheet.write(row + 2 + i, col + 4, "", cell_format)
            sheet.write(row + 2 + i, col + 5, member_name,
                        bp_format if first_project_member.member.subcontractor else cell_format)
        if first_project_member.member.subcontractor:
            sheet.write(row + 2 + i, col + 6, "BP", bp_format)
        else:
            sheet.write(row + 2 + i, col + 6, "", cell_format)
        sheet.write_datetime(row + 2 + i, col + 7, first_project_member.start_date, date_format)
        sheet.write_datetime(row + 2 + i, col + 8, first_project_member.end_date, date_format)
        sheet.write(row + 2 + i, col + 9, "", cell_format)
        sheet.write(row + 2 + i, col + 10, "", cell_format)
        sheet.write(row + 2 + i, col + 11, "", cell_format)
        sheet.write(row + 2 + i, col + 12, "", cell_format)
        i += 1

        for project_member in project.get_working_project_members():
            if project_member.pk == first_project_member.pk:
                continue
            sheet.write(row + 2 + i, col + 0, "", cell_format)
            sheet.write(row + 2 + i, col + 1, "", cell_format)
            sheet.write(row + 2 + i, col + 2, "", cell_format)
            sheet.write(row + 2 + i, col + 3, project_member.member.section.name, cell_format)
            member_name = project_member.member.__unicode__()
            position_ship = project_member.member.get_position_ship()
            member_name = u"%s(%s)" % (member_name, position_ship.get_position_display()) if position_ship else member_name
            if project_member.role >= 6:
                sheet.write(row + 2 + i, col + 4, member_name,
                            bp_format if project_member.member.subcontractor else cell_format)
                sheet.write(row + 2 + i, col + 5, "", cell_format)
            else:
                sheet.write(row + 2 + i, col + 4, "", cell_format)
                sheet.write(row + 2 + i, col + 5, member_name,
                            bp_format if project_member.member.subcontractor else cell_format)
            if project_member.member.subcontractor:
                sheet.write(row + 2 + i, col + 6, "BP", bp_format)
            else:
                sheet.write(row + 2 + i, col + 6, "", cell_format)
            sheet.write_datetime(row + 2 + i, col + 7, project_member.start_date, date_format)
            sheet.write_datetime(row + 2 + i, col + 8, project_member.end_date, date_format)
            sheet.write(row + 2 + i, col + 9, "", cell_format)
            sheet.write(row + 2 + i, col + 10, "", cell_format)
            sheet.write(row + 2 + i, col + 11, "", cell_format)
            sheet.write(row + 2 + i, col + 12, "", cell_format)
            i += 1

    # ページ設定
    sheet.set_landscape()
    sheet.set_paper(9)
    sheet.set_header('&L' + filename)
    sheet.set_margins(0, 0, 0.3, 0.1)
    sheet.set_print_scale(80)

    book.close()
    output.seek(0)
    return output


def generate_member_list(members, filename):
    output = StringIO.StringIO()
    row = 0
    col = 0

    book = xlsxwriter.Workbook(output)
    sheet = book.add_worksheet()
    # 見出しを書き込む
    title_format_top = book.add_format({'bold': True,
                                        'font_size': 20})
    title_format = book.add_format({'bold': True,
                                    'right': 1,
                                    'top': 2,
                                    'bg_color': '#b7dee8',
                                    'align': 'center',
                                    'text_wrap': True,
                                    'valign': 'vcenter'})
    title_format_left = book.add_format({'bold': True,
                                         'right': 1,
                                         'top': 2,
                                         'left': 2,
                                         'bg_color': '#b7dee8',
                                         'align': 'center',
                                         'valign': 'vcenter'})
    title_format_right = book.add_format({'bold': True,
                                          'right': 2,
                                          'top': 2,
                                          'bg_color': '#b7dee8',
                                          'align': 'center',
                                          'valign': 'vcenter'})
    sheet.write(row, col + 5, filename, title_format_top)
    row += 2
    sheet.set_row(row, 33)
    sheet.write(row, col, u"No.", title_format_left)
    sheet.set_column(get_excel_col_entire(col), 3.5)
    sheet.write(row, col + 1, u"名前", title_format)
    sheet.set_column(get_excel_col_entire(col + 1), 10)
    sheet.write(row, col + 2, u"スキル", title_format)
    sheet.set_column(get_excel_col_entire(col + 2), 26)
    sheet.write(row, col + 3, u"年齢", title_format)
    sheet.set_column(get_excel_col_entire(col + 3), 7)
    sheet.write(row, col + 4, u"性別", title_format)
    sheet.set_column(get_excel_col_entire(col + 4), 7)
    sheet.write(row, col + 5, u"レベル", title_format)
    sheet.set_column(get_excel_col_entire(col + 5), 9)
    sheet.write(row, col + 6, u"役割", title_format)
    sheet.write(row, col + 7, u"IT業界\r\n経験年数", title_format)
    sheet.set_column(get_excel_col_entire(col + 7), 9.13)
    sheet.write(row, col + 8, u"最寄駅", title_format)
    sheet.set_column(get_excel_col_entire(col + 8), 11)
    sheet.write(row, col + 9, u"得意業務", title_format)
    sheet.set_column(get_excel_col_entire(col + 9), 12)
    sheet.write(row, col + 10, u"日本語", title_format)
    sheet.set_column(get_excel_col_entire(col + 10), 12)
    sheet.write(row, col + 11, u"参加可能日", title_format)
    sheet.set_column(get_excel_col_entire(col + 11), 11)
    sheet.write(row, col + 12, u"備考", title_format_right)
    sheet.set_column(get_excel_col_entire(col + 12), 20)

    # 詳細を書き込む
    cell_format_center = book.add_format({'align': 'center',
                                          'valign': 'vcenter',
                                          'border': 1})
    cell_format_left = book.add_format({'valign': 'vcenter',
                                        'text_wrap': True,
                                        'border': 1})
    row += 1
    for i, member in enumerate(members):
        sheet.set_row(row + i, 27)
        # No.
        sheet.write(row + i, col, i + 1, cell_format_center)
        # 名前
        sheet.write(row + i, col + 1, member.__unicode__(), cell_format_center)
        # スキル
        skill_list = member.get_skill_list()
        sheet.write(row + i, col + 2, ",".join([skill.name for skill in skill_list]), cell_format_center)
        # 年齢
        sheet.write(row + i, col + 3, member.get_age(), cell_format_center)
        # 性別
        sheet.write(row + i, col + 4, member.get_sex_display(), cell_format_center)
        # レベル
        sheet.write(row + i, col + 5, ",".join(member.get_project_role_list()), cell_format_center)
        # 役割
        position_ship = member.get_position_ship(is_min=True)
        position_name = position_ship.get_position_display() if position_ship else u"メンバー"
        sheet.write(row + i, col + 6, position_name, cell_format_center)
        # IT業界経験年数
        sheet.write(row + i, col + 7, "", cell_format_center)
        # 最寄駅
        sheet.write(row + i, col + 8, member.nearest_station, cell_format_center)
        # 得意業務
        sheet.write(row + i, col + 9, "", cell_format_center)
        # 日本語
        sheet.write(row + i, col + 10, member.japanese_description, cell_format_center)
        # 参加可能日
        sheet.write(row + i, col + 11, "", cell_format_center)
        # 備考
        sheet.write(row + i, col + 12, member.comment, cell_format_left)

    # ページ設定
    sheet.set_landscape()
    sheet.set_paper(9)  # 印刷用紙：A4
    sheet.set_print_scale(85)

    book.close()
    output.seek(0)
    return output


def get_excel_col_by_index(col):
    # col は０から
    if (col >= 0) and (col <= 25):
        return chr(col + 65)
    elif (col > 25) and (col < 702):
        a, b = divmod(col, 26)
        return chr(a + 64) + chr(b + 65)


def get_excel_col_entire(col):
    c = get_excel_col_by_index(col)
    return "%s:%s" % (c, c)


def get_default_password(member):
    return "%s@%s" % (member.first_name_en, member.birthday.strftime("%Y%m%d"))


def line_counter():

    def get_line_count(p):
        cnt = 0
        if os.path.exists(p):
            for line in open(p, 'r'):
                if not re.match(r"^\s*#", line) and not re.match(r"^\s*$", line):
                    cnt += 1
        return cnt

    path = os.path.abspath(os.path.dirname(os.path.dirname(sys.argv[0])))
    all_count = 0
    for root, dirs, files in os.walk(path):
        for f in files:
            name, ext = os.path.splitext(f)
            path_file = os.path.join(root, f)
            if ext == ".py" and os.path.dirname(path_file).split("\\")[-1] != "migrations":
                count = get_line_count(path_file)
                all_count += count
                print path_file.ljust(80), count
    print "Total line count: %s" % (all_count,)


def get_insert_sql():
    path = r"C:\Github\ebusiness\data.sql"
    sql_list = []
    for line in open(path, 'r'):
        if line.startswith('CREATE TABLE "eb_') or line.startswith("INSERT INTO `eb_"):
            sql_list.append(line)
    if not sql_list:
        return

    lst = []
    items = []
    for i in sql_list:
        i = i.strip()
        if i.startswith("CREATE TABLE"):
            del lst[:]
            for item in re.findall(r'"([a-z_0-9]+)"', i):
                if (item == "id") or lst:
                    if not item.startswith("eb_") and not item.startswith("auth_") and item not in lst:
                        lst.append(item)
            items = ",".join(lst)
        else:
            print i.replace("VALUES", "(%s) VALUES" % (items,))


def is_salesperson(user):
    try:
        if user.salesperson:
            return True
        else:
            return False
    except:
        return False


def is_salesperson_director(user):
    try:
        if user.salesperson.member_type == 0:
            return True
        else:
            return False
    except:
        return False


def parse_date_from_string(str_date, split1=u'/', split2=u'/', split3=u''):
    """文字列から、日付を解析する。

    Arguments：
      str_date: 解析要の文字列
      split1: 区切り
      split2:
      split3:

    Returns：
      date型

    Raises：
      なし
    """
    if str_date and str_date.strip():
        str_date = str_date.strip().encode("utf-8")
        dt = datetime.datetime.strptime(str_date, "%Y" +
                                        split1.encode("utf-8") + "%m" +
                                        split2.encode("utf-8") + "%d" +
                                        split3.encode("utf-8"))
        return datetime.date(dt.year, dt.month, dt.day)
    else:
        return None


def parse_date_from_string2(str_date, split1=u'/', split2=u''):
    """文字列から、日付を解析する。

    Arguments：
      str_date: 解析要の文字列
      split1: 区切り
      split2:

    Returns：
      date型

    Raises：
      なし
    """
    if str_date and str_date.strip():
        str_date = str_date.strip().encode("utf-8")
        dt = datetime.datetime.strptime(str_date, "%Y" +
                                        split1.encode("utf-8") + "%m" +
                                        split2.encode("utf-8"))
        return datetime.date(dt.year, dt.month, dt.day)
    else:
        return None


def parse_os_lang(name):
    """履歴書を読み込む時、文字列からＯＳを解析する。

    Arguments：
      name: 解析要の文字列

    Returns：
      解析後の文字列

    Raises：
      なし
    """
    if not name:
        return None

    name = name.strip().lower()
    new_name = ""
    for i in name:
        if re.match(ur"[0-9a-z/# ]", i, re.U):
            new_name += i
    if new_name:
        return new_name.title()
    else:
        return None


def parse_project_role(name):
    """案件の作業区分を解析する。

    Arguments：
      name: 解析要の文字列

    Returns：
      解析後の文字列

    Raises：
      なし
    """
    if not name:
        return None
    name = name.strip().upper()
    if name == "PM":
        return "PM"
    elif name == "PL":
        return "L"
    elif name in [v for v, m in constants.CHOICE_PROJECT_ROLE]:
        return name
    else:
        return None


if __name__ == "__main__":
    # get_insert_sql()
    line_counter()
    # for l in range(703):
    #     print get_excel_col_by_index(l)
