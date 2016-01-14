# coding: UTF-8
"""
Created on 2015/10/29

@author: Yang Wanjun
"""
import os
import datetime
import StringIO
import xlsxwriter

try:
    import pythoncom
    import win32com.client
except:
    pass

import constants
import common
import errors
from django.contrib.humanize.templatetags.humanize import intcomma

from eb.models import ProjectMember


def generate_resume(member):
    output = StringIO.StringIO()

    book = xlsxwriter.Workbook(output)
    sheet = book.add_worksheet()
    # 全体の設定
    sheet.set_column('A:AP', 1.9)
    # タイトル設定
    title_format = book.add_format({'bold': True,
                                    'border': 1,
                                    'align': 'center',
                                    'valign': 'vcenter',
                                    'font_size': 24})
    sheet.merge_range('A1:AP3', u"技　術　者　経　歴　書", title_format)
    # 最終更新日
    title_format = book.add_format({'bold': True,
                                    'border': 0,
                                    'align': 'right',
                                    'valign': 'vcenter',
                                    'font_size': 11})
    content_format = book.add_format({'bold': True,
                                      'border': 0,
                                      'align': 'center',
                                      'valign': 'vcenter',
                                      'font_size': 11})
    sheet.merge_range('A4:AI4', u"最終更新日：", title_format)
    today = datetime.date.today()
    sheet.merge_range('AJ4:AP4', u"%d年%02d月" % (today.year, today.month), content_format)
    # 基本情報設定
    title_format_top = book.add_format({'bold': True,
                                        'top': 1,
                                        'left': 1,
                                        'right': 1,
                                        'align': 'center',
                                        'valign': 'vcenter',
                                        'bg_color': '#c0c0c0',
                                        'font_size': 10,
                                        'text_wrap': True})
    title_format_inner = book.add_format({'bold': True,
                                          'top': 4,
                                          'left': 1,
                                          'right': 1,
                                          'align': 'center',
                                          'valign': 'vcenter',
                                          'bg_color': '#c0c0c0',
                                          'font_size': 10,
                                          'text_wrap': True})
    title_format_bottom = book.add_format({'bold': True,
                                           'top': 4,
                                           'left': 1,
                                           'right': 1,
                                           'bottom': 1,
                                           'align': 'center',
                                           'valign': 'vcenter',
                                           'bg_color': '#c0c0c0',
                                           'font_size': 10,
                                           'text_wrap': True})
    content_format_top = book.add_format({'valign': 'vcenter',
                                          'font_size': 9,
                                          'right': 1,
                                          'top': 1})
    content_format_inner = book.add_format({'valign': 'vcenter',
                                            'font_size': 9,
                                            'right': 1,
                                            'top': 4})
    content_format_inner2 = book.add_format({'valign': 'vcenter',
                                             'font_size': 9,
                                             'top': 4})
    content_format_inner3 = book.add_format({'valign': 'vcenter',
                                             'font_size': 18,
                                             'top': 4})
    content_format_inner_center = book.add_format({'valign': 'vcenter',
                                                   'align': 'center',
                                                   'font_size': 9,
                                                   'right': 1,
                                                   'left': 4,
                                                   'top': 4})
    content_format_bottom = book.add_format({'valign': 'vcenter',
                                             'font_size': 9,
                                             'right': 1,
                                             'top': 4,
                                             'bottom': 1})
    sheet.merge_range('A5:C5', u"フリガナ", title_format_top)
    sheet.merge_range('A6:C7', u"氏　　名", title_format_inner)
    sheet.merge_range('A8:C9', u"現 住 所", title_format_inner)
    sheet.merge_range('A10:C10', u"最 寄 駅", title_format_inner)
    sheet.merge_range('A11:C12', u"在日年数", title_format_bottom)

    sheet.merge_range('D5:L5', member.first_name_ja + " " + member.last_name_ja if member.last_name_ja else "",
                      content_format_top)
    sheet.merge_range('D6:L7', member.first_name + " " + member.last_name if member.last_name else "",
                      content_format_inner3)
    sheet.merge_range('D8:L9', member.address1, content_format_inner)
    sheet.merge_range('D10:L10', member.nearest_station, content_format_inner)
    sheet.merge_range('D11:L12', u"%s 年" % (member.years_in_japan,) if member.years_in_japan else "",
                      content_format_bottom)

    sheet.merge_range('M5:O6', u"性　 　別", title_format_top)
    sheet.merge_range('M7:O8', u"本     籍", title_format_inner)
    sheet.merge_range('M9:O10', u"生年月日", title_format_inner)
    sheet.merge_range('M11:O12', u"婚　　姻\r\n状　　況", title_format_bottom)

    sheet.merge_range('P5:X6', member.get_sex_display(), content_format_top)
    sheet.merge_range('P7:X8', member.country, content_format_inner)
    sheet.merge_range('P9:T10', u"%d年%2d月%2d日" % (member.birthday.year, member.birthday.month, member.birthday.day),
                      content_format_inner2)
    sheet.merge_range('U9:X10', str(member.get_age()), content_format_inner_center)
    sheet.merge_range('P11:X12', member.get_is_married_display(), content_format_bottom)

    sheet.merge_range('Y5:AA7', u"日 本 語\r\n／英語", title_format_top)
    sheet.merge_range('Y8:AA10', u"資　　格", title_format_inner)
    sheet.merge_range('Y11:AA12', u"得　　意", title_format_bottom)

    sheet.merge_range('AB5:AP7', member.japanese_description, content_format_top)
    sheet.merge_range('AB8:AP10', member.certificate, content_format_inner)
    sheet.merge_range('AB11:AP12', member.skill_description, content_format_bottom)

    # 学歴を書き込む
    title_format_1 = book.add_format({'bold': True,
                                      'align': 'center',
                                      'valign': 'vcenter',
                                      'bg_color': '#c0c0c0',
                                      'font_size': 18,
                                      'left': 1,
                                      'top': 1,
                                      'bottom': 1,
                                      'right': 4})
    title_format_2 = book.add_format({'bold': True,
                                      'align': 'center',
                                      'valign': 'vcenter',
                                      'bg_color': '#c0c0c0',
                                      'font_size': 10,
                                      'left': 4,
                                      'top': 1,
                                      'bottom': 4,
                                      'right': 4})
    title_format_3 = book.add_format({'bold': True,
                                      'align': 'center',
                                      'valign': 'vcenter',
                                      'bg_color': '#c0c0c0',
                                      'font_size': 10,
                                      'left': 4,
                                      'top': 1,
                                      'bottom': 4,
                                      'right': 1})
    content_format_inner = book.add_format({'font_size': 10,
                                            'bottom': 4,
                                            'left': 4,
                                            'right': 4})
    content_format_right = book.add_format({'font_size': 10,
                                            'bottom': 4,
                                            'left': 4,
                                            'right': 1})
    content_format_bottom = book.add_format({'font_size': 10,
                                             'bottom': 1,
                                             'left': 4,
                                             'right': 4})
    content_format_bottom_right = book.add_format({'font_size': 10,
                                                   'bottom': 1,
                                                   'left': 4,
                                                   'right': 1})
    sheet.merge_range('A14:E16', u"学    歴", title_format_1)
    sheet.merge_range('F14:N14', u"期       間", title_format_2)
    sheet.merge_range('O14:AP14', u"学校名称　／　学部　／　専門　／学位", title_format_3)
    for i, degree in enumerate(member.degree_set.all()):
        period = u"%d/%02d/%02d - %d/%02d/%02d" % (degree.start_date.year, degree.start_date.month,
                                                   degree.start_date.day,
                                                   degree.end_date.year, degree.end_date.month, degree.end_date.day)
        sheet.merge_range(14 + i, 5, 14 + i, 13, period,
                          content_format_inner if i == 0 else content_format_bottom)
        sheet.merge_range(14 + i, 14, 14 + i, 41, degree.description,
                          content_format_right if i == 0 else content_format_bottom_right)
    else:
        cnt = member.degree_set.all().count()
        if cnt == 1:
            sheet.merge_range(14 + 1, 5, 14 + 1, 13, "", content_format_bottom)
            sheet.merge_range(14 + 1, 14, 14 + 1, 41, "", content_format_bottom_right)
        elif cnt == 0:
            sheet.merge_range(14 + 0, 5, 14 + 0, 13, "", content_format_inner)
            sheet.merge_range(14 + 0, 14, 14 + 0, 41, "", content_format_right)
            sheet.merge_range(14 + 1, 5, 14 + 1, 13, "", content_format_bottom)
            sheet.merge_range(14 + 1, 14, 14 + 1, 41, "", content_format_bottom_right)

    # 業務経歴を書き込む
    title_format = book.add_format({'bold': True,
                                    'align': 'center',
                                    'font_size': 18,
                                    'bg_color': '#ffff99',
                                    'border': 1})
    title_format_left_top = book.add_format({'bold': True,
                                             'align': 'center',
                                             'valign': 'vcenter',
                                             'bg_color': '#c0c0c0',
                                             'font_size': 10,
                                             'top': 1,
                                             'left': 1,
                                             'bottom': 1,
                                             'right': 4})
    title_format_inner = book.add_format({'bold': True,
                                          'align': 'center',
                                          'valign': 'vcenter',
                                          'bg_color': '#c0c0c0',
                                          'font_size': 10,
                                          'top': 1,
                                          'left': 4,
                                          'bottom': 1,
                                          'right': 4,
                                          'text_wrap': True})
    title_format_right_top = book.add_format({'bold': True,
                                              'align': 'center',
                                              'valign': 'vcenter',
                                              'bg_color': '#c0c0c0',
                                              'font_size': 10,
                                              'top': 1,
                                              'left': 4,
                                              'bottom': 4,
                                              'right': 1,
                                              'text_wrap': True})
    title_format_bottom = book.add_format({'bold': True,
                                           'align': 'center',
                                           'valign': 'vcenter',
                                           'bg_color': '#c0c0c0',
                                           'font_size': 10,
                                           'top': 4,
                                           'left': 4,
                                           'bottom': 1,
                                           'right': 4,
                                           'text_wrap': True})
    title_format_bottom_right = book.add_format({'bold': True,
                                                 'align': 'center',
                                                 'valign': 'vcenter',
                                                 'bg_color': '#c0c0c0',
                                                 'font_size': 10,
                                                 'top': 4,
                                                 'left': 4,
                                                 'bottom': 1,
                                                 'right': 1,
                                                 'text_wrap': True})
    content_format_left = book.add_format({'align': 'center',
                                           'valign': 'vcenter',
                                           'font_size': 9,
                                           'left': 1,
                                           'top': 1,
                                           'bottom': 1,
                                           'right': 4})
    content_format_inner = book.add_format({'valign': 'vcenter',
                                            'font_size': 9,
                                            'left': 4,
                                            'top': 1,
                                            'bottom': 1,
                                            'right': 4,
                                            'text_wrap': True})
    content_format_inner2 = book.add_format({'valign': 'vcenter',
                                             'font_size': 9,
                                             'left': 4,
                                             'top': 1,
                                             'bottom': 4,
                                             'right': 4})
    content_format_inner3 = book.add_format({'align': 'center',
                                             'valign': 'vcenter',
                                             'font_size': 9,
                                             'left': 4,
                                             'top': 1,
                                             'bottom': 4,
                                             'right': 4})
    content_format_inner4 = book.add_format({'valign': 'vcenter',
                                            'font_size': 9,
                                            'left': 4,
                                            'top': 4,
                                            'bottom': 1,
                                            'right': 4,
                                            'text_wrap': True})
    content_format_right = book.add_format({'valign': 'vcenter',
                                            'font_size': 9,
                                            'left': 4,
                                            'top': 1,
                                            'bottom': 1,
                                            'right': 1,
                                            'text_wrap': True})
    sheet.merge_range('A18:AP19', u"業  務  経  歴", title_format)
    sheet.merge_range('A20:A24', u"No.", title_format_left_top)
    sheet.merge_range('B20:E24', u"作業期間", title_format_inner)
    sheet.merge_range('F20:Q24', u"業務内容", title_format_inner)
    sheet.merge_range('R20:W24', u"機種／OS", title_format_inner)
    sheet.merge_range('X20:AC24', u"言語／ツール\r\nＤＢ", title_format_inner)
    sheet.merge_range('AD20:AF24', u"作\r\n業\r\n区\r\n分", title_format_inner)
    sheet.merge_range('AG20:AP20', u"作業工程", title_format_right_top)
    sheet.merge_range('AG21:AG24', u"要\r\n件\r\n定\r\n義", title_format_bottom)
    sheet.merge_range('AH21:AH24', u"調\r\n査\r\n分\r\n析", title_format_bottom)
    sheet.merge_range('AI21:AI24', u"基\r\n本\r\n設\r\n計", title_format_bottom)
    sheet.merge_range('AJ21:AJ24', u"詳\r\n細\r\n設\r\n計", title_format_bottom)
    sheet.merge_range('AK21:AK24', u"開\r\n発\r\n製\r\n造", title_format_bottom)
    sheet.merge_range('AL21:AL24', u"単\r\n体\r\n試\r\n験", title_format_bottom)
    sheet.merge_range('AM21:AM24', u"結\r\n合\r\n試\r\n験", title_format_bottom)
    sheet.merge_range('AN21:AN24', u"総\r\n合\r\n試\r\n験", title_format_bottom)
    sheet.merge_range('AO21:AO24', u"保\r\n守\r\n運\r\n用", title_format_bottom)
    sheet.merge_range('AP21:AP24', u"サ\r\nポ\r\nー\r\nト", title_format_bottom_right)

    project_count = member.projectmember_set.all().count()
    all_project_count = member.historyproject_set.all().count() + project_count

    # 案件一覧
    for i, project_member in enumerate(member.projectmember_set.all()):
        first_row = 24 + (i * 3)
        sheet.set_row(first_row + 1, 30)
        sheet.set_row(first_row + 2, 30)
        sheet.merge_range(first_row, 0, first_row + 2, 0, str(i + 1), content_format_left)
        period = u"%d年%02d月～\r\n%d年%02d月" % (project_member.project.start_date.year,
                                                 project_member.project.start_date.month,
                                                 project_member.project.end_date.year,
                                                 project_member.project.end_date.month)
        sheet.merge_range(first_row, 1, first_row + 2, 4, period, content_format_inner)
        sheet.merge_range(first_row, 5, first_row, 13, project_member.project.name, content_format_inner2)
        sheet.merge_range(first_row, 14, first_row, 16, "", content_format_inner3)
        sheet.merge_range(first_row + 1, 5, first_row + 2, 16, project_member.project.description,
                          content_format_inner4)
        os_list = [os.name for os in project_member.project.os.all()]
        sheet.merge_range(first_row, 17, first_row + 2, 22, u"\r\n".join(os_list), content_format_inner)
        skill_list = [skill.name for skill in project_member.project.skills.all()]
        sheet.merge_range(first_row, 23, first_row + 2, 28, u"\r\n".join(skill_list), content_format_inner)
        sheet.merge_range(first_row, 29, first_row + 2, 31, project_member.role, content_format_inner)
        sheet.merge_range(first_row, 32, first_row + 2, 32, u"●" if project_member.is_in_rd() else "",
                          content_format_inner)
        sheet.merge_range(first_row, 33, first_row + 2, 33, u"●" if project_member.is_in_sa() else "",
                          content_format_inner)
        sheet.merge_range(first_row, 34, first_row + 2, 34, u"●" if project_member.is_in_bd() else "",
                          content_format_inner)
        sheet.merge_range(first_row, 35, first_row + 2, 35, u"●" if project_member.is_in_dd() else "",
                          content_format_inner)
        sheet.merge_range(first_row, 36, first_row + 2, 36, u"●" if project_member.is_in_pg() else "",
                          content_format_inner)
        sheet.merge_range(first_row, 37, first_row + 2, 37, u"●" if project_member.is_in_pt() else "",
                          content_format_inner)
        sheet.merge_range(first_row, 38, first_row + 2, 38, u"●" if project_member.is_in_it() else "",
                          content_format_inner)
        sheet.merge_range(first_row, 39, first_row + 2, 39, u"●" if project_member.is_in_st() else "",
                          content_format_inner)
        sheet.merge_range(first_row, 40, first_row + 2, 40, u"●" if project_member.is_in_maintain() else "",
                          content_format_inner)
        sheet.merge_range(first_row, 41, first_row + 2, 41, u"●" if project_member.is_in_support() else "",
                          content_format_right)

    # 以前やっていた案件を出力する。
    for i, project in enumerate(member.historyproject_set.all()):
        first_row = 24 + (project_count * 3) + (i * 3)
        sheet.set_row(first_row + 1, 30)
        sheet.set_row(first_row + 2, 30)
        sheet.merge_range(first_row, 0, first_row + 2, 0, str(project_count + i + 1), content_format_left)
        period = u"%d年%02d月～\r\n%d年%02d月" % (project.start_date.year, project.start_date.month,
                                             project.end_date.year, project.end_date.month)
        sheet.merge_range(first_row, 1, first_row + 2, 4, period, content_format_inner)
        sheet.merge_range(first_row, 5, first_row, 13, project.name, content_format_inner2)
        sheet.merge_range(first_row, 14, first_row, 16, project.location, content_format_inner3)
        sheet.merge_range(first_row + 1, 5, first_row + 2, 16, project.description, content_format_inner4)
        os_list = [os.name for os in project.os.all()]
        sheet.merge_range(first_row, 17, first_row + 2, 22, u"\r\n".join(os_list), content_format_inner)
        skill_list = [skill.name for skill in project.skill.all()]
        sheet.merge_range(first_row, 23, first_row + 2, 28, u"\r\n".join(skill_list), content_format_inner)
        sheet.merge_range(first_row, 29, first_row + 2, 31, project.role, content_format_inner)
        sheet.merge_range(first_row, 32, first_row + 2, 32, u"●" if project.is_in_rd() else "", content_format_inner)
        sheet.merge_range(first_row, 33, first_row + 2, 33, u"●" if project.is_in_sa() else "", content_format_inner)
        sheet.merge_range(first_row, 34, first_row + 2, 34, u"●" if project.is_in_bd() else "", content_format_inner)
        sheet.merge_range(first_row, 35, first_row + 2, 35, u"●" if project.is_in_dd() else "", content_format_inner)
        sheet.merge_range(first_row, 36, first_row + 2, 36, u"●" if project.is_in_pg() else "", content_format_inner)
        sheet.merge_range(first_row, 37, first_row + 2, 37, u"●" if project.is_in_pt() else "", content_format_inner)
        sheet.merge_range(first_row, 38, first_row + 2, 38, u"●" if project.is_in_it() else "", content_format_inner)
        sheet.merge_range(first_row, 39, first_row + 2, 39, u"●" if project.is_in_st() else "", content_format_inner)
        sheet.merge_range(first_row, 40, first_row + 2, 40, u"●" if project.is_in_maintain() else "",
                          content_format_inner)
        sheet.merge_range(first_row, 41, first_row + 2, 41, u"●" if project.is_in_support() else "",
                          content_format_right)
    if all_project_count == 0:
        all_project_count = 13
        for i in range(13):
            first_row = 24 + (i * 3)
            sheet.merge_range(first_row, 0, first_row + 2, 0, str(i + 1), content_format_left)
            sheet.merge_range(first_row, 1, first_row + 2, 4, "", content_format_inner)
            sheet.merge_range(first_row, 5, first_row, 13, "", content_format_inner2)
            sheet.merge_range(first_row, 14, first_row, 16, "", content_format_inner3)
            sheet.merge_range(first_row + 1, 5, first_row + 2, 16, "", content_format_inner4)
            sheet.merge_range(first_row, 17, first_row + 2, 22, "", content_format_inner)
            sheet.merge_range(first_row, 23, first_row + 2, 28, "", content_format_inner)
            sheet.merge_range(first_row, 29, first_row + 2, 31, "", content_format_inner)
            sheet.merge_range(first_row, 32, first_row + 2, 32, "", content_format_inner)
            sheet.merge_range(first_row, 33, first_row + 2, 33, "", content_format_inner)
            sheet.merge_range(first_row, 34, first_row + 2, 34, "", content_format_inner)
            sheet.merge_range(first_row, 35, first_row + 2, 35, "", content_format_inner)
            sheet.merge_range(first_row, 36, first_row + 2, 36, "", content_format_inner)
            sheet.merge_range(first_row, 37, first_row + 2, 37, "", content_format_inner)
            sheet.merge_range(first_row, 38, first_row + 2, 38, "", content_format_inner)
            sheet.merge_range(first_row, 39, first_row + 2, 39, "", content_format_inner)
            sheet.merge_range(first_row, 40, first_row + 2, 40, "", content_format_inner)
            sheet.merge_range(first_row, 41, first_row + 2, 41, "", content_format_right)

    row_tail = 24 + (all_project_count * 3)
    tail_format = book.add_format({'align': 'center',
                                   'valign': 'vcenter',
                                   'font_size': 9,
                                   'border': 1})
    sheet.merge_range(row_tail, 0, row_tail, 41,
                      u"作業区分：   M：ﾏﾈｰｼﾞｬｰ、L：ﾘｰﾀﾞｰ、SL：ｻﾌﾞﾘｰﾀﾞｰ、SE：.ｼｽﾃﾑｴﾝｼﾞﾆｱ、SP：ｼｽﾃﾑﾌﾟﾛｸﾞﾗﾏｰ、PG：ﾌﾟﾛｸﾞﾗﾏｰ、OP：ｵﾍﾟﾚｰﾀｰ",
                      tail_format)

    book.close()
    output.seek(0)
    return output


def generate_quotation(project, user, company):
    """見積書を生成する。

    Arguments：
      project: 対象の案件
      company: 会社名

    Returns：
      dict

    Raises：
      FileNotExistException
    """
    pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
    template_file = project.client.quotation_file if project.client.quotation_file else company.quotation_file
    if not template_file or not os.path.exists(template_file.path):
        raise errors.FileNotExistException(constants.ERROR_TEMPLATE_NOT_EXISTS)

    template_book = get_excel_template(template_file.path)
    template_sheet = template_book.Worksheets(1)
    book = get_new_book()
    cnt = book.Sheets.Count
    # テンプレートを生成対象ワークブックにコピーする。
    template_sheet.Copy(None, book.Worksheets(cnt))
    template_book.Close()
    sheet = book.Worksheets(cnt + 1)

    data = dict()
    # お客様会社名
    data['CLIENT_COMPANY_NAME'] = project.client.name
    # 見積書番号
    data['QUOTATION_NO'] = common.get_quotation_no(user)
    # 案件名称
    data['PROJECT_NAME'] = project.name
    # 業務内容
    data['PROJECT_DESCRIPTION'] = project.description
    # 開発期間
    data['START_DATE'] = u"%s年%s月%s日" % (project.start_date.year, project.start_date.month, project.start_date.day)
    data['END_DATE'] = u"%s年%s月%s日" % (project.end_date.year, project.end_date.month, project.end_date.day)
    # 基準時間
    data['MIN_HOUR'] = u"%d" % (project.min_hours,)
    data['MAX_HOUR'] = u"%d" % (project.max_hours,)
    # 開発場所
    data['ADDRESS'] = project.address

    # メンバー毎の料金
    detail_members = []
    for project_member in project.projectmember_set.public_all():
        dict_member = dict()
        dict_member['ITEM_NAME'] = project_member.member.__unicode__()
        dict_member['ITEM_PRICE'] = u"￥%s人/月" % (project_member.price,)
        dict_member['ITEM_PLUS'] = project_member.plus_per_hour
        dict_member['ITEM_MINUS'] = project_member.minus_per_hour
        detail_members.append(dict_member)

    data['quotation_details'] = detail_members
    data['details_start_col'] = 3

    replace_excel_dict(sheet, data)

    for i in range(cnt, 0, -1):
        book.Worksheets(i).Delete()

    file_folder = os.path.join(os.path.dirname(template_file.path), "temp")
    if not os.path.exists(file_folder):
        os.mkdir(file_folder)
    file_name = "tmp_%s_%s.xls" % (constants.DOWNLOAD_QUOTATION, datetime.datetime.now().strftime("%Y%m%d_%H%M%S%f"))
    path = os.path.join(file_folder, file_name)
    book.SaveAs(path, FileFormat=constants.EXCEL_FORMAT_EXCEL2003)
    return path


def generate_request(project, company, client_order, request_name=None, order_no=None, ym=None, bank=None):
    """請求書を出力する。

    Arguments：
      project: 対象の案件
      company: 会社名
      request_name: 請求書名称
      request_no: 請求番号
      order_no: 注文番号
      ym: 対象年月

    Returns：
      dict

    Raises：
      FileNotExistException
    """
    pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
    if project.is_lump:
        request_file = company.request_lump_file
    else:
        request_file = project.client.request_file if project.client.request_file else company.request_file
    if not request_file or not os.path.exists(request_file.path):
        raise errors.FileNotExistException(constants.ERROR_TEMPLATE_NOT_EXISTS)

    template_book = get_excel_template(request_file.path)
    template_sheet = template_book.Worksheets(1)
    book = get_new_book()
    cnt = book.Sheets.Count
    # テンプレートを生成対象ワークブックにコピーする。
    template_sheet.Copy(None, book.Worksheets(cnt))
    template_book.Close()
    sheet = book.Worksheets(cnt + 1)

    date = datetime.date.today()
    if ym:
        try:
            year = ym[:4]
            month = ym[4:]
            date = datetime.date(int(year), int(month), 1)
        except:
            year = str(date.year)
            month = "%02d" % (date.month,)
    else:
        year = str(date.year)
        month = "%02d" % (date.month,)

    data = dict()
    # お客様郵便番号
    data['CLIENT_POST_CODE'] = common.get_full_postcode(project.client.post_code)
    # お客様住所
    data['CLIENT_ADDRESS'] = project.client.address1 + project.client.address2
    # お客様電話番号
    data['CLIENT_TEL'] = project.client.tel
    # お客様名称
    data['CLIENT_COMPANY_NAME'] = project.client.name
    first_day = datetime.date(date.year, date.month, 1)
    last_day_current_month = common.get_last_day_by_month(date)
    period = u"%s年%s月%s日 ～ %s年%s月%s日" % (first_day.year, first_day.month, first_day.day,
                                         last_day_current_month.year, last_day_current_month.month, last_day_current_month.day)

    project_request = project.get_project_request(year, month)
    # 作業期間
    data['WORK_PERIOD'] = period
    # 注文番号
    data['ORDER_NO'] = order_no if order_no else u""
    # 注文日
    data['REQUEST_DATE'] = client_order.order_date.strftime('%Y/%m/%d') if client_order.order_date else ""
    # 契約件名
    data['CONTRACT_NAME'] = request_name if request_name else project.name
    # お支払い期限
    data['REMIT_DATE'] = project.client.get_pay_date(date=date).strftime('%Y/%m/%d')
    # 請求番号
    data['REQUEST_NO'] = project_request.request_no
    # 発行日（対象月の最終日）
    data['PUBLISH_DATE'] = u"%d年%02d月%02d日" % (last_day_current_month.year, last_day_current_month.month,
                                               last_day_current_month.day)
    # 本社郵便番号
    data['POST_CODE'] = common.get_full_postcode(company.post_code)
    # 本社住所
    data['ADDRESS'] = company.address1 + company.address2
    # 会社名
    data['COMPANY_NAME'] = company.name
    member = company.get_master()
    # 代表取締役
    data['MASTER'] = u"%s %s" % (member.first_name, member.last_name) if member else ""
    # 本社電話番号
    data['TEL'] = company.tel
    # 振込先銀行名称
    data['BANK_NAME'] = bank.bank_name if bank else u""
    # 支店番号
    data['BRANCH_NO'] = bank.branch_no if bank else u""
    # 支店名称
    data['BRANCH_NAME'] = bank.branch_name if bank else u""
    # 預金種類
    data['ACCOUNT_TYPE'] = bank.get_account_type_display() if bank else u""
    # 口座番号
    data['ACCOUNT_NUMBER'] = bank.account_number if bank else u""
    # 口座名義人
    data['BANK_ACCOUNT_HOLDER'] = bank.account_holder if bank else u""

    # 全員の合計明細
    detail_all = dict()
    # メンバー毎の明細
    detail_members = []

    # 案件内すべてのメンバーを取得する。
    if client_order.projects.public_filter(is_deleted=False).count() > 1:
        # 一つの注文書に複数の案件がある場合
        projects = client_order.projects.public_filter(is_deleted=False)
        project_members = ProjectMember.objects.public_filter(project__in=projects)
    elif project.get_order_by_month(year, month).count() > 1:
        # １つの案件に複数の注文書ある場合
        project_members = []
        if client_order.member_comma_list:
            for pm_id in client_order.member_comma_list.split(","):
                try:
                    project_members.append(ProjectMember.objects.get(pk=int(pm_id)))
                except:
                    pass
    else:
        project_members = project.get_project_members_by_month(date)
    members_amount = 0
    if project.is_lump:
        members_amount = project.lump_amount
    else:
        for i, project_member in enumerate(project_members):
            dict_expenses = dict()
            # 番号
            dict_expenses['NO'] = i + 1
            # 項目
            dict_expenses['ITEM_NAME'] = project_member.member.__unicode__()
            # 単価（円）
            dict_expenses['ITEM_PRICE'] = project_member.price
            # Min/Max（H）
            dict_expenses['ITEM_MIN_MAX'] = "%s/%s" % (int(project_member.min_hours), int(project_member.max_hours))
            attendance = project_member.get_attendance(date.year, date.month)
            # その他
            dict_expenses['ITEM_OTHER'] = 0
            # 基本金額
            dict_expenses['ITEM_AMOUNT_BASIC'] = project_member.price if attendance else u""
            # 残業金額
            if attendance:
                # 勤務時間
                dict_expenses['ITEM_WORK_HOURS'] = attendance.total_hours if attendance else u""
                # 残業時間
                dict_expenses['ITEM_EXTRA_HOURS'] = attendance.extra_hours if attendance else u""
                # 率
                dict_expenses['ITEM_RATE'] = attendance.rate if attendance.rate else 1
                # 減（円）
                if project_member.minus_per_hour is None:
                    dict_expenses['ITEM_MINUS_PER_HOUR'] = (project_member.price / project_member.min_hours) \
                        if attendance else u""
                else:
                    dict_expenses['ITEM_MINUS_PER_HOUR'] = project_member.minus_per_hour
                # 増（円）
                if project_member.plus_per_hour is None:
                    dict_expenses['ITEM_PLUS_PER_HOUR'] = (project_member.price / project_member.max_hours) \
                        if attendance else u""
                else:
                    dict_expenses['ITEM_PLUS_PER_HOUR'] = project_member.plus_per_hour

                if attendance.extra_hours > 0:
                    dict_expenses['ITEM_AMOUNT_EXTRA'] = attendance.extra_hours * dict_expenses['ITEM_PLUS_PER_HOUR']
                    dict_expenses['ITEM_PLUS_PER_HOUR2'] = dict_expenses['ITEM_PLUS_PER_HOUR']
                    dict_expenses['ITEM_MINUS_PER_HOUR2'] = u""
                elif attendance.extra_hours < 0:
                    dict_expenses['ITEM_AMOUNT_EXTRA'] = attendance.extra_hours * dict_expenses['ITEM_MINUS_PER_HOUR']
                    dict_expenses['ITEM_PLUS_PER_HOUR2'] = u""
                    dict_expenses['ITEM_MINUS_PER_HOUR2'] = dict_expenses['ITEM_MINUS_PER_HOUR']
                else:
                    dict_expenses['ITEM_AMOUNT_EXTRA'] = 0
                    dict_expenses['ITEM_PLUS_PER_HOUR2'] = u""
                    dict_expenses['ITEM_MINUS_PER_HOUR2'] = u""
                # 基本金額＋残業金額
                dict_expenses['ITEM_AMOUNT_TOTAL'] = attendance.price
                # 備考
                dict_expenses['ITEM_COMMENT'] = attendance.comment
            else:
                dict_expenses['ITEM_RATE'] = u""
                dict_expenses['ITEM_AMOUNT_EXTRA'] = u""
                dict_expenses['ITEM_PLUS_PER_HOUR'] = u""
                dict_expenses['ITEM_MINUS_PER_HOUR'] = u""
                dict_expenses['ITEM_PLUS_PER_HOUR2'] = u""
                dict_expenses['ITEM_MINUS_PER_HOUR2'] = u""
                dict_expenses['ITEM_WORK_HOURS'] = u""
                dict_expenses['ITEM_EXTRA_HOURS'] = u""
                dict_expenses['ITEM_COMMENT'] = u""
                # 基本金額＋残業金額
                dict_expenses['ITEM_AMOUNT_TOTAL'] = project_member.price

            detail_members.append(dict_expenses)

            # 金額合計
            members_amount += dict_expenses['ITEM_AMOUNT_TOTAL']
    # 番号
    detail_all['NO'] = 1
    # 項目：契約件名に設定
    detail_all['ITEM_NAME_ATTENDANCE_TOTAL'] = data['CONTRACT_NAME']
    # 数量
    detail_all['ITEM_COUNT'] = 1
    # 単位
    detail_all['ITEM_UNIT'] = u"一式"
    # 金額
    detail_all['ITEM_AMOUNT_ATTENDANCE_ALL'] = members_amount
    # 備考
    detail_all['ITEM_COMMENT'] = project.lump_comment if project.is_lump else u""

    # 清算リスト
    dict_expenses = {}
    for expenses in project.get_expenses(date.year, date.month, project_members):
        if expenses.category.name not in dict_expenses:
            dict_expenses[expenses.category.name] = [expenses]
        else:
            dict_expenses[expenses.category.name].append(expenses)
    detail_expenses = []
    expenses_amount = 0
    for key, value in dict_expenses.iteritems():
        d = dict()
        member_list = []
        amount = 0
        for expenses in value:
            member_list.append(expenses.project_member.member.first_name +
                               expenses.project_member.member.last_name +
                               u"￥%s" % (expenses.price,))
            amount += expenses.price
            expenses_amount += expenses.price
        d['ITEM_EXPENSES_CATEGORY_SUMMARY'] = u"%s(%s)" % (key, u"、".join(member_list))
        d['ITEM_EXPENSES_CATEGORY_AMOUNT'] = amount
        detail_expenses.append(d)
    if not dict_expenses:
        # 清算がない場合、
        d = dict()
        d['ITEM_EXPENSES_CATEGORY_SUMMARY'] = u""
        d['ITEM_EXPENSES_CATEGORY_AMOUNT'] = u""
        detail_expenses.append(d)

    data['detail_all'] = detail_all
    data['detail_members'] = detail_members
    data['detail_expenses'] = detail_expenses  # 清算リスト
    data['ITEM_AMOUNT_ATTENDANCE'] = members_amount
    if project.client.decimal_type == '0':
        data['ITEM_AMOUNT_ATTENDANCE_TAX'] = int(round(members_amount * project.client.tax_rate))
    else:
        data['ITEM_AMOUNT_ATTENDANCE_TAX'] = int(members_amount * project.client.tax_rate)  # 出勤のトータル金額の税金
    data['ITEM_AMOUNT_ATTENDANCE_ALL'] = members_amount + data['ITEM_AMOUNT_ATTENDANCE_TAX']
    data['ITEM_AMOUNT_ALL'] = data['ITEM_AMOUNT_ATTENDANCE_ALL'] + expenses_amount
    data['ITEM_AMOUNT_ALL_COMMA'] = intcomma(data['ITEM_AMOUNT_ALL'])

    # 請求情報を保存する
    project_request.amount = data['ITEM_AMOUNT_ALL']
    project_request.save()

    replace_excel_dict(sheet, data)

    for i in range(cnt, 0, -1):
        book.Worksheets(i).Delete()

    # GroupBoxを高さを調整する
    for shape in sheet.Shapes:
        shape.Height = 66

    file_folder = os.path.join(os.path.dirname(request_file.path), "temp")
    if not os.path.exists(file_folder):
        os.mkdir(file_folder)
    file_name = "tmp_%s_%s.xls" % (constants.DOWNLOAD_REQUEST, datetime.datetime.now().strftime("%Y%m%d_%H%M%S%f"))
    path = os.path.join(file_folder, file_name)
    book.SaveAs(path, FileFormat=constants.EXCEL_FORMAT_EXCEL2003)

    return path, project_request.request_no


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


def replace_excel_dict(sheet, data):
    """エクセルの文字列を置換する。

    Arguments：
      sheet: エクセルのシート
      data: 置換する対象

    Returns：
      なし

    Raises：
      なし
    """
    if not data:
        return
    for key, value in data.iteritems():
        if key == "detail_all":
            if find_cell_by_string(sheet, "{$ITEM_NAME_ATTENDANCE_TOTAL$}"):
                replace_excel_dict(sheet, value)
        elif key == "detail_members":
            if find_cell_by_string(sheet, "{$ITEM_PRICE$}"):
                replace_excel_list(sheet, value)
        elif key == "detail_expenses":
            # 清算リスト
            if find_cell_by_string(sheet, "{$ITEM_EXPENSES_CATEGORY_AMOUNT$}"):
                replace_excel_list(sheet, value)
        elif key == "quotation_details":
            # 見積書の料金明細
            replace_excel_list(sheet, value, data['details_start_col'])
        else:
            sheet.Cells.Replace(What="{$%s$}" % (key,), Replacement=value, LookAt=constants.xlPart, MatchCase=False,
                                SearchFormat=False, ReplaceFormat=False, SearchOrder=constants.xlByRows)


def replace_excel_list(sheet, data_list, details_start_col=None):
    if data_list:
        rows = get_row_span(sheet, data_list[0])
        positions = get_replace_positions(sheet, data_list[0])
        labels = []
        if positions:
            row, col = positions.values()[0]
            start_cell = sheet.Cells(row + rows, 1)
            end_cell = find_cell_by_string(sheet, "*", after=start_cell)
            # 必要行数
            cnt_all_rows = rows * len(data_list)
            # 既存の行数
            cnt_current_rows = end_cell.Row - (start_cell.Row - 1)
            # 足りない行数
            if cnt_all_rows > cnt_current_rows:
                cnt_extra_rows = cnt_all_rows - cnt_current_rows
                sheet.Range("%s:%s" % (end_cell.Row, end_cell.Row + cnt_extra_rows - 1)).Insert(Shift=constants.xlDown)
            if details_start_col:
                labels = get_replace_labels_position(sheet, row, details_start_col, rows)
        for i, data in enumerate(data_list):
            for key, value in data.iteritems():
                if key in positions:
                    row, col = positions[key]
                    sheet.Cells(row + (i * rows), col).Value = value
                    if key in ('ITEM_WORK_HOURS', 'ITEM_RATE'):
                        sheet.Cells(row + (i * rows), col).NumberFormatLocal = u"G/標準"
            if i > 0:
                for lbl_row, lbl_col, label in labels:
                    sheet.Cells(lbl_row + (i * rows), lbl_col).Value = label


def find_cell_by_string(sheet, s, after=None):
    if after:
        return sheet.Cells.Find(What=s, LookIn=constants.xlFormulas, After=after, LookAt=constants.xlPart,
                                SearchOrder=constants.xlByRows, SearchDirection=constants.xlNext,
                                MatchCase=False, MatchByte=False, SearchFormat=False)
    else:
        return sheet.Cells.Find(What=s, LookIn=constants.xlFormulas, LookAt=constants.xlPart,
                                SearchOrder=constants.xlByRows, SearchDirection=constants.xlNext,
                                MatchCase=False, MatchByte=False, SearchFormat=False)


def get_row_span(sheet, data):
    """明細の一行は何行跨いでいるのかを示す。

    Arguments：
      sheet: エクセルのシート
      data: 置換する対象

    Returns：
      なし

    Raises：
      なし
    """
    rows = []
    for key in data.keys():
        replace_key = "{$%s$}" % (key,)
        cell = find_cell_by_string(sheet, replace_key)
        if cell:
            rows.append(cell.Row)
    return max(rows) - min(rows) + 1


def get_replace_positions(sheet, data):
    """各置換文字列の位置を取得する。

    Arguments：
      sheet: エクセルのシート
      data: 置換する対象

    Returns：
      なし

    Raises：
      なし
    """
    d = dict()
    for key in data.keys():
        replace_key = "{$%s$}" % (key,)
        cell = find_cell_by_string(sheet, replace_key)
        if cell:
            d[key] = (cell.Row, cell.Column)
    return d


def get_replace_labels_position(sheet, start_row, start_col, row_span):
    labels = []
    for row in range(start_row, start_row + row_span):
        for col in range(start_col, sheet.UsedRange.Columns.Count):
            val = sheet.Cells(row, col).Value
            if val and val.strip() and val.find("{$") < 0:
                labels.append((row, col, val))
    return labels
