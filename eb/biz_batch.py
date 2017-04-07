# coding: UTF-8
"""
Created on 2016/06/03

@author: Yang Wanjun
"""
import datetime
import urllib2
import json
import re
import os
import traceback

from . import biz, biz_config
from utils import constants, common, file_gen
from eb import models
from eboa import models as eboa_models

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.utils.text import get_text_list
from django.utils.translation import ugettext as _


def sync_members():
    company = biz.get_company()
    url = biz_config.get_config(constants.CONFIG_SERVICE_MEMBERS)
    response = urllib2.urlopen(url)
    html = response.read()
    dict_data = json.loads(html.replace("\r", "").replace("\n", ""))
    message_list = []
    lll = []
    if 'employeeList' in dict_data:
        for data in dict_data.get("employeeList"):
            employee_code = data.get("id", None)
            name = data.get("name", None)
            birthday = data.get("birthDate", None)
            address = data.get("address", None)
            department_name = data.get("department", None)
            if department_name == u"SS　1部":
                department_name = u"開発部　1部"
            elif department_name == u"SS　2部":
                department_name = u"開発部　2部"
            elif department_name == u"SS　4部":
                department_name = u"開発部　4部"
            elif department_name == u"SS　5部":
                department_name = u"開発部　5部"
            department_id = data.get('departmentId', None)
            if (department_id, department_name) not in lll:
                lll.append((department_id, department_name))
            eb_mail = data.get("ebMailAddress", None)
            introduction = data.get("introduction", None)
            join_date = data.get("joinDate", None)
            name_jp = data.get("kana", None)
            private_mail = data.get("mailAddress", None)
            phone = data.get("phone", None)
            postcode = data.get("postcode", None)
            sex = data.get("sex", None)
            station = data.get("station", None)
            if employee_code:
                if employee_code < '0402':
                    continue
                if department_name == u"営業部" or employee_code in ('0123', '0126', '0198', '0150', '0249', '0335'):
                    # 0123 馬婷婷
                    # 0150 孫雲釵
                    # 0198 劉 暢
                    # 0126 丁 玲
                    # 0249 齋藤 善次
                    # 0335 蒋杰
                    query_set = models.Salesperson.objects.raw('select * from eb_salesperson where id_from_api=%s',
                                                               [employee_code])
                    if len(list(query_set)) == 0:
                        member = models.Salesperson(employee_id=employee_code, id_from_api=employee_code)
                    else:
                        # message_list.append(("WARN", name, birthday, address, u"既に存在しているレコードです。"))
                        continue
                else:
                    query_set = models.Member.objects.raw('select * from eb_member where id_from_api=%s',
                                                          [employee_code])
                    if len(list(query_set)) == 0:
                        member = models.Member(employee_id=employee_code, id_from_api=employee_code)
                    else:
                        # message_list.append(("WARN", name, birthday, address, u"既に存在しているレコードです。"))
                        continue

                try:
                    # コストを取得する。
                    member.first_name = common.get_first_last_name(name)[0]
                    member.last_name = common.get_first_last_name(name)[1]
                    if name_jp:
                        lst = common.get_first_last_ja_name(name_jp)
                        if len(lst) == 2 and lst[0]:
                            member.first_name_ja = common.get_first_last_ja_name(name_jp)[0]
                            member.last_name_ja = common.get_first_last_ja_name(name_jp)[1]
                        elif len(lst) == 1:
                            member.first_name_ja = common.get_first_last_ja_name(name_jp)[0]
                    if birthday:
                        try:
                            member.birthday = common.parse_date_from_string(birthday)
                        except Exception as ex:
                            print ex.message
                            message_list.append(("WARN", name, birthday, address, u"生年月日が存在しません。"))
                            member.birthday = None
                    else:
                        member.birthday = datetime.date.today()
                    member.address1 = address if address else station
                    if department_name:
                        try:
                            section = models.Section.objects.get(name=department_name)
                        except ObjectDoesNotExist:
                            section = models.Section(name=department_name)
                            section.company = company
                            section.save()
                    else:
                        section = None
                    member.email = eb_mail
                    member.private_email = private_mail
                    member.comment = introduction
                    if join_date:
                        member.join_date = common.parse_date_from_string(join_date)
                    if phone:
                        member.phone = phone.replace("-", "")
                    if postcode:
                        member.post_code = postcode.strip().replace("/", "").replace("-", "").strip()
                        if len(member.post_code.strip()) == 8:
                            member.post_code = member.post_code[3:] + member.post_code[4:]
                        if len(member.post_code) != 7:
                            member.post_code = None
                    member.nearest_station = station if station and len(station) <= 15 else None
                    member.sex = "2" if sex == "0" else "1"
                    member.cost = get_cost(employee_code)
                    member.company = company
                    member.save()
                    # 部署を設定する。
                    sp = models.MemberSectionPeriod(member=member, section=section, start_date=member.join_date)
                    sp.save()
                    message_list.append(("INFO", employee_code, name, birthday, address, u"完了"))
                except Exception as e:
                    message_list.append(("ERROR", employee_code, name, birthday, address, u"エラー：" + str(e)))
    return message_list


def sync_members_for_change(batch):
    members = models.Member.objects.public_filter(eboa_user_id__isnull=False)
    logger = batch.get_logger()
    user = batch.get_log_entry_user()
    for member in members:
        try:
            oa_member = eboa_models.EbEmployee.objects.get(user__userid=member.eboa_user_id)
            changed_list = []
            zip_code = oa_member.zipcode.replace('-', '') if oa_member.zipcode else ""
            # 郵便番号
            if re.match(r'^[0-9]{7}$', zip_code) and member.post_code != zip_code:
                common.get_object_changed_message(member, 'post_code', zip_code, changed_list)
                member.post_code = zip_code
            # 住所
            address = unicode(oa_member.address.decode('utf8')) if oa_member.address else ''
            old_address = member.address1 if member.address1 else ''
            old_address += member.address2 if member.address2 else ''
            if address and old_address != address:
                common.get_object_changed_message(member, 'address1', address, changed_list)
                common.get_object_changed_message(member, 'address2', "", changed_list)
                member.address1 = address
                member.address2 = ""
            # 電話番号
            private_tel_number = oa_member.private_tel_number.replace("-", "") if oa_member.private_tel_number else ''
            if re.match(r'^[0-9]{11}$', private_tel_number) and member.phone != private_tel_number:
                common.get_object_changed_message(member, 'phone', private_tel_number, changed_list)
                member.phone = private_tel_number
            # 会社メールアドレス
            if oa_member.business_mail_addr and oa_member.business_mail_addr.endswith("@e-business.co.jp") \
                    and member.email != oa_member.business_mail_addr:
                common.get_object_changed_message(member, 'email', oa_member.business_mail_addr, changed_list)
                member.email = oa_member.business_mail_addr
            if changed_list:
                member.save()
            if changed_list and user:
                change_message = _('Changed %s.') % get_text_list(changed_list, _('and')) if changed_list else ''
                prefix = u"【%s】" % batch.title
                LogEntry.objects.log_action(user_id=user.pk,
                                            content_type_id=ContentType.objects.get_for_model(member).pk,
                                            object_id=member.pk,
                                            object_repr=unicode(member),
                                            action_flag=CHANGE,
                                            change_message=(prefix + change_message) or _('No fields changed.'))
                args = (member.eboa_user_id, member.__unicode__(), change_message)
                msg = u"【INFO】eboa_user_id: %s, name: %s, %s" % args
                logger.info(msg)
        except ObjectDoesNotExist:
            args = (member.eboa_user_id, member.__unicode__(), u"ＥＢＯＡのＤＢに該当するデータがありません。")
            msg = u"【ERROR】eboa_user_id: %s, name: %s, %s" % args
            logger.error(msg)
        except MultipleObjectsReturned:
            args = (member.eboa_user_id, member.__unicode__(), u"ＥＢＯＡのＤＢに該当するデータ複数存在している。")
            msg = u"【ERROR】eboa_user_id: %s, name: %s, %s" % args
            logger.error(msg)
        except Exception as ex:
            args = (member.eboa_user_id, member.__unicode__(), unicode(ex))
            msg = u"【ERROR】eboa_user_id: %s, name: %s, 予期しないエラー: %s" % args
            logger.error(msg)
            logger.error(traceback.format_exc())


def get_cost(code):
    if code:
        url = biz_config.get_config(constants.CONFIG_SERVICE_CONTRACT) % (code,)
        response = urllib2.urlopen(url)
        html = response.read()
        data = json.loads(html.replace("\r", "").replace("\n", ""))
        period_list = []
        for item in data['contractList']:
            period_list.append(item['EMPLOYMENT_PERIOD_END'])
        latest_period = None
        if period_list:
            latest_period = max(period_list)
        for item in data['contractList']:
            if latest_period and item['EMPLOYER_NO'] == code and item['EMPLOYMENT_PERIOD_END'] == latest_period:
                if item['ALLOWANLE_COST'] != "-":
                    return item['ALLOWANLE_COST']
        for item in data['contractList']:
            if item['EMPLOYER_NO'] == code:
                return item['ALLOWANLE_COST'] if item['ALLOWANLE_COST'] != "-" else 0
    return 0


def get_batch_manager(name):
    try:
        batch = models.BatchManage.objects.get(name=name)
    except ObjectDoesNotExist:
        batch = models.BatchManage(name=name)
    return batch


def get_members_information():
    all_members = models.get_on_sales_members()
    working_members = models.get_working_members()
    waiting_members = models.get_waiting_members()
    current_month_release = models.get_release_current_month()
    next_month_release = models.get_release_next_month()
    next_2_month_release = models.get_release_next_2_month()

    summary = {'all_member_count': all_members.count(),
               'working_member_count': working_members.count(),
               'waiting_member_count': waiting_members.count(),
               'current_month_count': current_month_release.count(),
               'next_month_count': next_month_release.count(),
               'next_2_month_count': next_2_month_release.count(),
               }

    status_list = []
    for salesperson in get_salesperson_members():
        d = dict()
        d['salesperson'] = salesperson
        d['all_member_count'] = salesperson.get_on_sales_members().count()
        d['working_member_count'] = salesperson.get_working_members().count()
        d['waiting_member_count'] = salesperson.get_waiting_members().count()
        d['current_month_count'] = salesperson.get_release_current_month().count()
        d['next_month_count'] = salesperson.get_release_next_month().count()
        d['next_2_month_count'] = salesperson.get_release_next_2_month().count()
        status_list.append(d)

    return status_list, summary


def notify_member_status_mails(batch, status_list, summary):
    """メールを通知する。

    :param batch バッチに管理ファイル
    :param status_list 通知の内容リスト
    :param summary 通知の集計情報
    """
    def get_status_info(salesperson_id):
        for status in status_list:
            if status['salesperson'].pk == salesperson_id:
                return [status]
        return []

    logger = batch.get_logger()
    today = datetime.date.today()
    next_month = common.add_months(today, 1)
    next_2_months = common.add_months(today, 2)
    next_ym = next_month.strftime('%Y%m')
    next_2_ym = next_2_months.strftime('%Y%m')
    # 営業部長取得する
    directors = get_salesperson_director()
    if directors:
        context = {'salesperson_list': directors,
                   'status_list': status_list,
                   'summary': summary,
                   'domain': biz_config.get_domain_name(),
                   'next_ym': next_ym,
                   'next_2_ym': next_2_ym,
                   }
        recipient_list = []
        for salesperson in directors:
            recipient_list.extend(salesperson.get_notify_mail_list())
        if recipient_list:
            batch.send_notify_mail(context, recipient_list)
    salesperson_list = get_salesperson_members()
    if salesperson_list:
        for salesperson in salesperson_list:
            recipient_list = salesperson.get_notify_mail_list()
            context = {'salesperson_list': [salesperson],
                       'status_list': get_status_info(salesperson.pk),
                       'summary': None,
                       'domain': biz_config.get_domain_name(),
                       'next_ym': next_ym,
                       'next_2_ym': next_2_ym,
                       }
            if recipient_list:
                batch.send_notify_mail(context, recipient_list, no_cc=True)
            else:
                logger.warning(u"%s の宛先が空白になっている。" % (salesperson.__unicode__(),))


def send_attendance_format(batch, date):
    """勤怠フォーマットを各部署の部長に送付する。

    :param date: 対象年月の出勤情報
    :param batch:
    :return:
    """
    logger = batch.get_logger()
    if not batch.attachment1 or not os.path.exists(batch.attachment1.path):
        logger.warning(u"出勤フォーマットの添付ファイルが設定していません。")
        return

    sections = biz.get_on_sales_section()
    if not date:
        date = datetime.datetime.today()
    for section in sections:
        statistician = section.get_attendance_statistician()
        if statistician.count() == 0:
            logger.warning(u"部署「%s」の勤務統計者が設定していません。" % (section.__unicode__(),))
            continue
        recipient_list = []
        name_list = []
        for member in statistician:
            recipient_list.extend(member.get_notify_mail_list())
            name_list.append(member.__unicode__())
        if not recipient_list:
            logger.error(u"%s の送信先メールアドレスが設定していません。" % (u",".join(name_list),))
            continue

        project_members = biz.get_project_members_month_section(section, date)
        output = file_gen.generate_attendance_format(batch.attachment1.path, project_members, date)

        context = {'statistician': statistician,
                   'section': section,
                   }
        attachment = (constants.NAME_SECTION_ATTENDANCE % (section.name, date.year, date.month) + ".xlsx",
                      output,
                      constants.MIME_TYPE_EXCEL)
        batch.send_notify_mail(context, recipient_list, [attachment])


def get_salesperson_director():
    """営業の管理者を取得する。
    """
    return models.Salesperson.objects.public_filter(member_type=0)


def get_salesperson_members():
    """営業のメンバーを取得する。
    """
    return models.Salesperson.objects.public_filter(member_type=5)
