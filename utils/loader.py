# coding: UTF-8
"""
Created on 2015/09/28

@author: Yang Wanjun
"""
import re
import xlrd
import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max

from eb.models import Member, Degree, HistoryProject, OS, Skill, ProjectStage

import constants
import common


def load_resume(file_content, member_id=None):
    book = xlrd.open_workbook(file_contents=file_content)
    sheet = book.sheet_by_index(0)

    if member_id is None:
        member = Member()

        # 姓名
        name = sheet.cell(5, 3).value
        member.first_name = common.get_first_last_name(name)[0]
        member.last_name = common.get_first_last_name(name)[1]

        members = Member.objects.raw(u"select * from eb_member"
                                     u" where CONCAT(first_name, last_name) = %s",
                                     [member.first_name + member.last_name])
        members = list(members)
        if members:
            # 読み込んだファイルに同じ名前のメンバーが存在する場合。
            return member, members
        else:
            member_id = 0

    if member_id == 0:
        # 姓名
        member = Member()
        name = sheet.cell(5, 3).value
        member.first_name = common.get_first_last_name(name)[0]
        member.last_name = common.get_first_last_name(name)[1]
        # 基本情報読み込む
        # フリカナ
        name_jp = sheet.cell(4, 3).value
        member.first_name_ja = common.get_first_last_ja_name(name_jp)[0]
        member.last_name_ja = common.get_first_last_ja_name(name_jp)[1]
        # 性別
        sex = sheet.cell(4, 15).value
        if sex and sex in (u"男", u"女"):
            member.sex = '1' if sex == u"男" else "2"
        # 生年月日
        birthday = sheet.cell(8, 15).value
        dt = datetime.datetime(*xlrd.xldate_as_tuple(birthday, book.datemode))
        member.birthday = datetime.date(dt.year, dt.month, dt.day)
        # 最寄駅
        station = sheet.cell(9, 3).value
        member.nearest_station = station.strip() if station else None
    else:
        member = Member.objects.get(pk=member_id)
    # 国家・地域
    country = sheet.cell(6, 15).value
    member.country = country.strip() if country else None
    # 在日年数
    years = sheet.cell(10, 3).value
    if years and years.strip():
        m = re.search(ur"\d+", years)
        member.years_in_japan = int(m.group()) if m else None
    # 婚姻状況
    married = sheet.cell(10, 15).value
    if married and married.strip():
        member.is_married = '0' if married.strip() == u"未婚" else "1"
    # 日本語能力の説明
    japanese = sheet.cell(4, 27).value
    member.japanese_description = japanese.strip() if japanese else None
    # 資格の説明
    certificate = sheet.cell(7, 27).value
    member.certificate = certificate.strip() if certificate else None
    # 得意
    skill_description = sheet.cell(10, 27).value
    member.skill_description = skill_description.strip() if skill_description else None

    if member_id == 0:
        max_employee_id = Member.objects.all().aggregate(Max('employee_id'))
        member.employee_id = common.get_next_employee_id(max_employee_id.get('employee_id__max'))
        member.save()

    # 学歴読み込む
    for row in range(14, sheet.nrows):
        if sheet.cell(row, 5).value:
            period = sheet.cell(row, 5).value
            date_list = []
            for m in re.finditer(constants.REG_DATE_STR, period, re.U):
                date_list.append(common.parse_date_from_string(m.group()))
            if date_list:
                # 学歴のインスタンスを作成
                try:
                    degree = Degree.objects.get(member=member, start_date=date_list[0], end_date=date_list[1])
                except ObjectDoesNotExist:
                    degree = Degree(member=member, start_date=date_list[0], end_date=date_list[1])
                for col in range(6, sheet.ncols):
                    if sheet.cell(row, col).value:
                        degree.description = sheet.cell(row, col).value
                        break
                degree.save()
        else:
            break

    # 業務経歴を読み込む
    start_row = -1
    col_period = col_content = col_os = col_language = col_role = -1
    col_stage_def = col_stage_search = col_stage_bd = col_stage_dd = col_stage_pg = -1
    col_stage_pt = col_stage_it = col_stage_st = col_stage_maintain = col_stage_support = -1
    for row in range(19, sheet.nrows):
        if sheet.cell(row, 0).value and sheet.cell(row, 0).value == u"No.":
            for col in range(sheet.ncols):
                if sheet.cell(row, col).value == u"作業期間":
                    col_period = col
                elif sheet.cell(row, col).value == u"業務内容":
                    col_content = col
                elif sheet.cell(row, col).value == u"機種／OS":
                    col_os = col
                elif u"言語／ツール" in sheet.cell(row, col).value:
                    col_language = col
                elif sheet.cell(row, col).value == u"作業区分":
                    col_role = col
                elif sheet.cell(row, col).value == u"作業工程":
                    col_stage_def = col + 0
                    col_stage_search = col + 1
                    col_stage_bd = col + 2
                    col_stage_dd = col + 3
                    col_stage_pg = col + 4
                    col_stage_pt = col + 5
                    col_stage_it = col + 6
                    col_stage_st = col + 7
                    col_stage_maintain = col + 8
                    col_stage_support = col + 9
            start_row = row + 1
            break

    if start_row > 0:
        for row in range(start_row, sheet.nrows):
            if sheet.cell(row, col_period).value:
                # 作業期間
                date_list = []
                period = sheet.cell(row, col_period).value
                if re.search(constants.REG_DATE_STR, period, re.U):
                    for m in re.finditer(constants.REG_DATE_STR, period, re.U):
                        split1 = m.group(1)
                        split2 = m.group(2)
                        split3 = m.group(3)
                        date_list.append(common.parse_date_from_string(m.group(), split1, split2, split3))
                    else:
                        if u"現在" in period or u"现在" in period and len(date_list) == 1:
                            date_list.append(datetime.date.today())
                elif re.search(constants.REG_DATE_STR2, period, re.U):
                    for m in re.finditer(constants.REG_DATE_STR2, period, re.U):
                        split1 = m.group(1)
                        split2 = m.group(2)
                        date_list.append(common.parse_date_from_string2(m.group(), split1, split2))
                    else:
                        if u"現在" in period or u"现在" in period and len(date_list) == 1:
                            date_list.append(datetime.date.today())
                # 案件名称
                title = sheet.cell(row, col_content).value
                project_name = title.strip() if title else None
                # 業務経歴の対象を作成
                try:
                    project = HistoryProject.objects.get(name=project_name, member=member,
                                                         start_date=date_list[0], end_date=date_list[1])
                except ObjectDoesNotExist:
                    project = HistoryProject(name=project_name, member=member,
                                             start_date=date_list[0], end_date=date_list[1])

                # 作業場所
                for i in range(col_content + 1, col_os):
                    if sheet.cell(row, i).value:
                        location = sheet.cell(row, i).value
                        project.location = location.strip() if location else None
                        break

                # 案件概要
                description = sheet.cell(row + 1, col_content).value
                project.description = description.strip() if description else None
                # 機種／OS
                project_os_list = []
                str_os = sheet.cell(row, col_os).value
                if str_os:
                    os_list = [common.parse_os_lang(os) for os in str_os.split("\n")
                               if common.parse_os_lang(os)]
                    for name in os_list:
                        try:
                            os = OS.objects.get(name=name)
                        except ObjectDoesNotExist:
                            # 存在しない場合は追加する。
                            os = OS(name=name)
                            os.save()
                        project_os_list.append(os)
                # 言語／ツール ＤＢ
                project_skill_list = []
                str_languages = sheet.cell(row, col_language).value
                if str_languages:
                    lang_list = [common.parse_os_lang(lang) for lang in str_languages.split("\n")
                                 if common.parse_os_lang(lang)]
                    for lang in lang_list:
                        try:
                            skill = Skill.objects.get(name=lang)
                        except ObjectDoesNotExist:
                            skill = Skill(name=lang)
                            skill.save()
                        project_skill_list.append(skill)
                # 作業区分
                role = sheet.cell(row, col_role).value
                role = common.parse_project_role(role)
                if role:
                    project.role = role
                # 作業工程
                project_stage_list = []
                for i, col in enumerate((col_stage_def, col_stage_search, col_stage_bd,
                                         col_stage_dd, col_stage_pg, col_stage_pt,
                                         col_stage_it, col_stage_st, col_stage_maintain, col_stage_support)):
                    if sheet.cell(row, col).value:
                        try:
                            stage = ProjectStage.objects.get(name=constants.PROJECT_STAGE[i])
                        except ObjectDoesNotExist:
                            stage = ProjectStage(name=constants.PROJECT_STAGE[i])
                            stage.save()
                        project_stage_list.append(stage)

                # 履歴を保存する
                project.save()
                project.os = project_os_list
                project.skill = project_skill_list
                project.stages = project_stage_list
                project.save()

    member.save()

    return member, None
