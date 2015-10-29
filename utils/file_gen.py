# coding: UTF-8
"""
Created on 2015/10/29

@author: Yang Wanjun
"""
import StringIO
import xlsxwriter


def generate_resume(member, filename):
    output = StringIO.StringIO()
    row = 0
    col = 0

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

    sheet.merge_range('D5:L5', member.first_name_ja + " " + member.last_name_ja, content_format_top)
    sheet.merge_range('D6:L7', member.first_name + " " + member.last_name, content_format_inner3)
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
        if member.degree_set.all().count() == 1:
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

    for i, project in enumerate(member.historyproject_set.all()):
        first_row = 24 + (i * 3)
        sheet.set_row(first_row + 1, 30)
        sheet.set_row(first_row + 2, 30)
        sheet.merge_range(first_row, 0, first_row + 2, 0, str(i + 1), content_format_left)
        period = u"%d年%02d月～\r\n%d年%02d月" % (project.start_date.year, project.start_date.month,
                                             project.end_date.year, project.end_date.month)
        sheet.merge_range(first_row, 1, first_row + 2, 4, period, content_format_inner)
        sheet.merge_range(first_row, 5, first_row, 13, project.name, content_format_inner2)
        sheet.merge_range(first_row, 14, first_row, 16, project.location, content_format_inner3)
        sheet.merge_range(first_row + 1, 5, first_row + 2, 16, project.description, content_format_inner)
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

    tail_format = book.add_format({'align': 'center',
                                   'valign': 'vcenter',
                                   'font_size': 9,
                                   'border': 1})
    row_tail = 24 + (member.historyproject_set.all().count() * 3)
    sheet.merge_range(row_tail, 0, row_tail, 41,
                      u"作業区分：   M：ﾏﾈｰｼﾞｬｰ、L：ﾘｰﾀﾞｰ、SL：ｻﾌﾞﾘｰﾀﾞｰ、SE：.ｼｽﾃﾑｴﾝｼﾞﾆｱ、SP：ｼｽﾃﾑﾌﾟﾛｸﾞﾗﾏｰ、PG：ﾌﾟﾛｸﾞﾗﾏｰ、OP：ｵﾍﾟﾚｰﾀｰ",
                      tail_format)

    book.close()
    output.seek(0)
    return output
