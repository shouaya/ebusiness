# coding: UTF-8
"""
Created on 2016/01/12

@author: Yang Wanjun
"""
import datetime

from django.db.models import Q, Max
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.humanize.templatetags import humanize
from django.utils import timezone

from utils import common
from eb import models
from eboa import models as eboa_models


def get_company():
    company_list = models.Company.objects.all()
    if company_list.count() == 0:
        return None
    else:
        return company_list[0]


def get_admin_user():
    try:
        return User.objects.get(username='admin')
    except ObjectDoesNotExist:
        return None


def get_all_members():
    """営業対象部署のすべてのメンバー、且つ入社済みのメンバーを取得する。

    :return:
    """
    today = datetime.date.today()
    return models.Member.objects.public_filter(Q(join_date__isnull=True) | Q(join_date__lte=today),
                                               section__is_on_sales=True)


def get_sales_members():
    """営業対象メンバーを取得する。

    :return:
    """
    return get_all_members().filter(is_on_sales=True)


def get_working_members(date=None):
    """稼働中のメンバー

    :param date: 対象年月
    :return:
    """
    if not date:
        first_day = last_day = datetime.date.today()
    else:
        first_day = common.get_first_day_by_month(date)
        last_day = common.get_last_day_by_month(date)
    members = get_sales_members().filter(projectmember__start_date__lte=last_day,
                                         projectmember__end_date__gte=first_day,
                                         projectmember__is_deleted=False,
                                         projectmember__status=2).distinct()
    return members


def get_waiting_members():
    """待機中のメンバー

    :return:
    """
    working_members = get_working_members()
    return get_sales_members().filter(is_on_sales=True).exclude(pk__in=working_members)


def get_off_sales_members():
    """営業対象外のメンバーを取得する。

    :return:
    """
    return get_all_members().filter(is_on_sales=False)


def get_members_in_coming():
    """新規入場要員リストを取得する。

    :return:
    """
    today = datetime.date.today()
    return models.Member.objects.public_filter(join_date__gt=today)


def get_subcontractor_all_members():
    """すべての協力社員を取得する。

    :return:
    """
    return get_all_members().filter(subcontractor__isnull=False)


def get_subcontractor_sales_members():
    """すべての協力社員を取得する。

    :return:
    """
    return get_subcontractor_all_members().filter(is_on_sales=True)


def get_subcontractor_working_members(date=None):
    """対象月の稼働中の協力社員を取得する。

    :param date: 対象年月
    :return:
    """
    if not date:
        first_day = last_day = datetime.date.today()
    else:
        first_day = common.get_first_day_by_month(date)
        last_day = common.get_last_day_by_month(date)

    return get_subcontractor_sales_members().filter(projectmember__start_date__lte=last_day,
                                                    projectmember__end_date__gte=first_day,
                                                    projectmember__is_deleted=False,
                                                    projectmember__status=2).distinct()


def get_subcontractor_waiting_members(date=None):
    """対象月の待機中の協力社員を取得する

    :param date: 対象年月
    :return:
    """
    working_members = get_subcontractor_working_members(date)
    return get_subcontractor_sales_members().exclude(pk__in=working_members)


def get_subcontractor_off_sales_members():
    """営業対象外の協力社員を取得する。

    :return:
    """
    return get_subcontractor_all_members().filter(is_on_sales=False)


def get_project_members_month(date):
    """指定月の案件メンバー全部取得する。

    :param date 指定月
    :return
    """
    first_day = common.get_first_day_by_month(date)
    today = datetime.date.today()
    if date.year == today.year and date.month == today.month:
        first_day = today
    last_day = common.get_last_day_by_month(date)
    return models.ProjectMember.objects.public_filter(end_date__gte=first_day,
                                                      end_date__lte=last_day,
                                                      project__status=4,
                                                      status=2)


def get_subcontractor_project_members_month(date):
    """指定月の案件メンバー全部取得する。

    :param date 指定月
    :return
    """
    return get_project_members_month(date).filter(member__member_type=4)


def get_next_change_list():
    """入退場リスト

    :return:
    """
    first_day = common.get_first_day_current_month()
    last_day = common.get_last_day_by_month(first_day)
    next_first_day = common.get_first_day_by_month(common.add_months(first_day, 1))
    next_last_day = common.get_last_day_by_month(next_first_day)
    members = models.Member.objects.public_filter(Q(projectmember__end_date__gte=first_day,
                                                    projectmember__end_date__lte=last_day,
                                                    projectmember__is_deleted=False,
                                                    projectmember__status=2)
                                                  | Q(projectmember__start_date__gte=next_first_day,
                                                      projectmember__start_date__lte=next_last_day,
                                                      projectmember__is_deleted=False,
                                                      projectmember__status=2)).distinct()
    return members.filter(section__is_on_sales=True)


def get_release_members_by_month(date, p=None):
    """指定年月にリリースするメンバーを取得する。

    :param date 指定月
    :param p: 画面からの絞り込み条件
    """
    working_member_next_date = get_working_members(date=common.add_months(date, 1))
    project_members = get_project_members_month(date).filter(member__section__is_on_sales=True,
                                                             member__is_on_sales=True)\
        .exclude(member__in=working_member_next_date)
    if p:
        project_members = project_members.filter(**p)
    return project_members


def get_release_current_month():
    """今月にリリースするメンバーを取得する。

    """
    return get_release_members_by_month(datetime.date.today())


def get_release_next_month():
    """来月にリリースするメンバーを取得する。

    """
    next_month = common.add_months(datetime.date.today(), 1)
    return get_release_members_by_month(next_month)


def get_release_next_2_month():
    """再来月にリリースするメンバーを取得する。

    """
    next_2_month = common.add_months(datetime.date.today(), 2)
    return get_release_members_by_month(next_2_month)


def get_subcontractor_release_members_by_month(date):
    """指定年月にリリースする協力社員を取得する。

    :param date 指定月
    """
    return get_release_members_by_month(date).filter(member__member_type=4)


def get_subcontractor_release_current_month():
    """今月にリリースする協力社員を取得する

    """
    return get_subcontractor_release_members_by_month(datetime.date.today())


def get_subcontractor_release_next_month():
    """来月にリリースする協力社員を取得する

    """
    next_month = common.add_months(datetime.date.today(), 1)
    return get_subcontractor_release_members_by_month(next_month)


def get_subcontractor_release_next_2_month():
    """再来月にリリースする協力社員を取得する

    """
    next_month = common.add_months(datetime.date.today(), 2)
    return get_subcontractor_release_members_by_month(next_month)


def get_projects(q=None, o=None):
    """案件を取得する。

    :param q:絞り込み条件
    :param o:並び順
    :return:
    """
    projects = models.Project.objects.public_all()
    if q:
        projects = projects.filter(**q)
    if o:
        projects = projects.order_by(*o)
    return projects


def get_projects_orders(ym, q=None, o=None):
    """案件の注文情報を取得する。

    :param ym:対象年月
    :param q:絞り込み条件
    :param o:並び順
    :return:
    """
    first_day = common.get_first_day_from_ym(ym)
    last_day = common.get_last_day_by_month(first_day)

    project_orders = models.ClientOrder.projects.through.objects\
        .filter(Q(clientorder__isnull=True) | Q(clientorder__start_date__lte=last_day,
                                                clientorder__end_date__gte=first_day),
                project__start_date__lte=last_day,
                project__end_date__gte=first_day).distinct()

    if q:
        if 'project__projectrequest__request_no__contains' in q:
            q.update({'project__projectrequest__year': ym[:4],
                      'project__projectrequest__month': ym[4:]})
        project_orders = project_orders.filter(**q)

    order_by_request_no = None
    if o:
        if 'project__projectrequest__request_no' in o:
            order_by_request_no = 'ASC'
            o.remove('project__projectrequest__request_no')
        elif '-project__projectrequest__request_no' in o:
            order_by_request_no = 'DESC'
            o.remove('-project__projectrequest__request_no')
        project_orders = project_orders.order_by(*o)

    all_project_orders = []
    for project_order in project_orders:
        project_request = project_order.project.get_project_request(ym[:4], ym[4:], project_order.clientorder)
        all_project_orders.append((project_order.project, project_request, project_order.clientorder))
    if order_by_request_no == 'ASC':
        all_project_orders.sort(key=lambda d: d[1].request_no)
    elif order_by_request_no == 'DESC':
        all_project_orders.sort(key=lambda d: d[1].request_no, reverse=True)
    return all_project_orders


def get_activities_incoming():
    """これから実施する活動一覧

    :return:
    """
    now = timezone.now()
    activities = models.ProjectActivity.objects.public_filter(open_date__gte=now).order_by('open_date')
    return activities[:5]


def get_salesperson_director():
    """営業の管理者を取得する。
    """
    return models.Salesperson.objects.public_filter(member_type=0, is_notify=True)


def get_salesperson_members():
    """営業のメンバーを取得する。
    """
    return models.Salesperson.objects.public_filter(member_type=5, is_notify=True)


def get_members_information():
    status_list = []
    summary = {'all_member_count': 0,
               'working_member_count': 0,
               'waiting_member_count': 0,
               'current_month_count': 0,
               'next_month_count': 0,
               'next_2_month_count': 0,
               }
    for salesperson in models.Salesperson.objects.public_filter(user__isnull=False, member_type=5):
        d = dict()
        d['salesperson'] = salesperson
        d['all_member_count'] = salesperson.get_all_members().count()
        d['working_member_count'] = salesperson.get_working_members().count()
        d['waiting_member_count'] = salesperson.get_waiting_members().count()
        d['current_month_count'] = get_release_current_month().count()
        d['next_month_count'] = get_release_next_month().count()
        d['next_2_month_count'] = get_release_next_2_month().count()
        status_list.append(d)

        summary['all_member_count'] += d['all_member_count']
        summary['working_member_count'] += d['working_member_count']
        summary['waiting_member_count'] += d['waiting_member_count']
        summary['current_month_count'] += d['current_month_count']
        summary['next_month_count'] += d['next_month_count']
        summary['next_2_month_count'] += d['next_2_month_count']

    return status_list, summary


def get_order_no(user):
    """注文番号を取得する。

    :param user ログインしているユーザ
    """
    prefix = '-'
    today = datetime.date.today()
    if hasattr(user, 'salesperson'):
        if user.salesperson.first_name_en:
            prefix = user.salesperson.first_name_en[0]

    order_no = "EB{0:04d}{1:02d}{2:02d}{3}".format(today.year, today.month, today.day, prefix)
    max_order_no = models.SubcontractorOrder.objects.public_filter(order_no__startswith=order_no)\
        .aggregate(Max('order_no'))
    max_order_no = max_order_no.get('order_no__max')
    if max_order_no:
        index = int(max_order_no[-2:]) + 1
    else:
        index = 1
    return "{0}{1:02d}".format(order_no, index)


def get_order_filename(subcontractor, order_no):
    """生成した註文書の名称を取得する。

    :param subcontractor 発注先
    :param order_no 請求番号
    :return 註文書の名称
    """
    now = datetime.datetime.now()
    return u"{0}_{1}_{2}.xls".format(order_no, subcontractor.name, now.strftime('%Y%m%d%H%M%S'))


def get_user_profile(user):
    """ログインしているユーザの詳細情報を取得する。

    :param user ログインしているユーザ
    """
    if hasattr(user, 'salesperson'):
        return user.salesperson
    return None


def generate_order_data(company, subcontractor, user, ym):
    """註文書を生成するために使うデータを生成する。

    :param company 発注元会社
    :param subcontractor 発注先
    :param user ログインしているユーザ
    :param ym 対象年月
    :return エクセルのバイナリー
    """
    data = {'DETAIL': {}}
    # 発行年月日
    date = datetime.date.today()
    data['DETAIL']['PUBLISH_DATE'] = u"%s年%02d月%02d日" % (date.year, date.month, date.day)
    # 下請け会社名
    data['DETAIL']['SUBCONTRACTOR_NAME'] = subcontractor.name
    # 委託業務責任者（乙）
    data['DETAIL']['SUBCONTRACTOR_MASTER'] = subcontractor.president
    # 作成者
    salesperson = get_user_profile(user)
    data['DETAIL']['AUTHOR_FIRST_NAME'] = salesperson.first_name if salesperson else ''
    # 会社名
    data['DETAIL']['COMPANY_NAME'] = company.name
    # 本社郵便番号
    data['DETAIL']['POST_CODE'] = common.get_full_postcode(company.post_code)
    # 本社電話番号
    data['DETAIL']['TEL'] = company.tel
    # 代表取締役
    member = company.get_master()
    data['DETAIL']['MASTER'] = u"%s %s" % (member.first_name, member.last_name) if member else ""
    # 本社住所
    data['DETAIL']['ADDRESS1'] = company.address1
    data['DETAIL']['ADDRESS2'] = company.address2
    # 作業期間
    if not ym:
        first_day = common.get_first_day_current_month()
    else:
        first_day = common.get_first_day_from_ym(ym)
    last_day = common.get_last_day_by_month(first_day)
    data['DETAIL']['START_DATE'] = u"%s年%02d月%02d日" % (first_day.year, first_day.month, first_day.day)
    data['DETAIL']['END_DATE'] = u"%s年%02d月%02d日" % (last_day.year, last_day.month, last_day.day)

    members = []
    # 全ての協力社員の注文情報を取得する。
    for member in subcontractor.get_members_by_month(first_day):
        bp_member_info = member.get_bp_member_info(first_day)
        members.append({'ITEM_NAME': member.__unicode__(),  # 協力社員名前
                        'ITEM_COST': humanize.intcomma(member.cost),  # 月額基本料金
                        'ITEM_MIN_HOUR': humanize.intcomma(bp_member_info.min_hours),  # 基準時間（最小値）
                        'ITEM_MAX_HOUR': humanize.intcomma(bp_member_info.max_hours),  # 基準時間（最大値）
                        'ITEM_PLUS_PER_HOUR': humanize.intcomma(bp_member_info.plus_per_hour),  # 超過単価
                        'ITEM_MINUS_PER_HOUR': humanize.intcomma(bp_member_info.minus_per_hour),  # 不足単価
                        })
    data['MEMBERS'] = members

    # 注文情報を追加する
    try:
        order = models.SubcontractorOrder.objects.get(subcontractor=subcontractor,
                                                      year=str(first_day.year),
                                                      month="%02d" % (first_day.month,))
        data['DETAIL']['ORDER_NO'] = order.order_no
        order.updated_user = user
    except ObjectDoesNotExist:
        data['DETAIL']['ORDER_NO'] = get_order_no(user)
        order = models.SubcontractorOrder(subcontractor=subcontractor,
                                          order_no=data['DETAIL']['ORDER_NO'],
                                          year=str(first_day.year),
                                          month="%02d" % (first_day.month,))
        order.created_user = user
    order.save()
    return data


def get_request_members_in_project(project, client_order, ym):
    """指定案件の指定注文書の中に、対象のメンバーを取得する。

    :param project: 指定案件
    :param client_order: 指定注文書
    :param ym: 対象年月
    :return: メンバーのリスト
    """
    if client_order.projects.public_filter(is_deleted=False).count() > 1:
        # 一つの注文書に複数の案件がある場合
        projects = client_order.projects.public_filter(is_deleted=False)
        project_members = models.ProjectMember.objects.public_filter(project__in=projects)
    elif project.get_order_by_month(ym[:4], ym[4:]).count() > 1:
        # １つの案件に複数の注文書ある場合
        project_members = []
        if client_order.member_comma_list:
            # 重複したメンバーを外す。
            member_id_list = sorted(set(client_order.member_comma_list.split(",")))
            for pm_id in member_id_list:
                try:
                    project_members.append(
                        models.ProjectMember.objects.get(pk=int(pm_id), is_deleted=False, status=2))
                except ObjectDoesNotExist:
                    pass
    else:
        project_members = project.get_project_members_by_month(ym=ym)
    return project_members


def generate_request_data(company, project, client_order, bank_info, ym, project_request):
    first_day = common.get_first_day_from_ym(ym)
    last_day = common.get_last_day_by_month(first_day)
    data = {'DETAIL': {}, 'EXTRA': {}}
    data['EXTRA']['YM'] = ym
    # お客様郵便番号
    data['DETAIL']['CLIENT_POST_CODE'] = common.get_full_postcode(project.client.post_code)
    # お客様住所
    data['DETAIL']['CLIENT_ADDRESS'] = project.client.address1 + project.client.address2
    # お客様電話番号
    data['DETAIL']['CLIENT_TEL'] = project.client.tel
    # お客様名称
    data['DETAIL']['CLIENT_COMPANY_NAME'] = project.client.name
    # 作業期間
    data['DETAIL']['WORK_PERIOD'] = first_day.strftime(u'%Y年%m月%d日'.encode('utf-8')).decode('utf-8') + u" ～ " + last_day.strftime(u'%Y年%m月%d日'.encode('utf-8')).decode('utf-8')
    data['EXTRA']['WORK_PERIOD_START'] = first_day
    data['EXTRA']['WORK_PERIOD_END'] = last_day
    # 注文番号
    data['DETAIL']['ORDER_NO'] = client_order.order_no if client_order.order_no else u""
    # 注文日
    data['DETAIL']['REQUEST_DATE'] = client_order.order_date.strftime('%Y/%m/%d') if client_order.order_date else ""
    # 契約件名
    data['DETAIL']['CONTRACT_NAME'] = project_request.request_name
    # お支払い期限
    data['DETAIL']['REMIT_DATE'] = project.client.get_pay_date(date=first_day).strftime('%Y/%m/%d')
    data['EXTRA']['REMIT_DATE'] = project.client.get_pay_date(date=first_day)
    # 請求番号
    data['DETAIL']['REQUEST_NO'] = project_request.request_no
    # 発行日（対象月の最終日）
    data['DETAIL']['PUBLISH_DATE'] = last_day.strftime(u"%Y年%m月%d日".encode('utf-8')).decode('utf-8')
    data['EXTRA']['PUBLISH_DATE'] = last_day
    # 本社郵便番号
    data['DETAIL']['POST_CODE'] = common.get_full_postcode(company.post_code)
    # 本社住所
    data['DETAIL']['ADDRESS'] = company.address1 + company.address2
    # 会社名
    data['DETAIL']['COMPANY_NAME'] = company.name
    # 代表取締役
    member = company.get_master()
    data['DETAIL']['MASTER'] = u"%s %s" % (member.first_name, member.last_name) if member else ""
    # 本社電話番号
    data['DETAIL']['TEL'] = company.tel
    # 振込先銀行名称
    data['EXTRA']['BANK'] = bank_info
    data['DETAIL']['BANK_NAME'] = bank_info.bank_name if bank_info else u""
    # 支店番号
    data['DETAIL']['BRANCH_NO'] = bank_info.branch_no if bank_info else u""
    # 支店名称
    data['DETAIL']['BRANCH_NAME'] = bank_info.branch_name if bank_info else u""
    # 預金種類
    data['DETAIL']['ACCOUNT_TYPE'] = bank_info.get_account_type_display() if bank_info else u""
    # 口座番号
    data['DETAIL']['ACCOUNT_NUMBER'] = bank_info.account_number if bank_info else u""
    # 口座名義人
    data['DETAIL']['BANK_ACCOUNT_HOLDER'] = bank_info.account_holder if bank_info else u""

    # 全員の合計明細
    detail_all = dict()
    # メンバー毎の明細
    detail_members = []

    project_members = get_request_members_in_project(project, client_order, ym)
    members_amount = 0
    if project.is_lump:
        members_amount = project.lump_amount
        # 番号
        detail_all['NO'] = u"1"
        # 項目：契約件名に設定
        detail_all['ITEM_NAME_ATTENDANCE_TOTAL'] = data['DETAIL']['CONTRACT_NAME']
        # 数量
        detail_all['ITEM_COUNT'] = u"1"
        # 単位
        detail_all['ITEM_UNIT'] = u"一式"
        # 金額
        detail_all['ITEM_AMOUNT_ATTENDANCE_ALL'] = members_amount
        # 備考
        detail_all['ITEM_COMMENT'] = project.lump_comment if project.is_lump else u""
    else:
        for i, project_member in enumerate(project_members):
            dict_expenses = dict()
            # この項目は請求書の出力ではなく、履歴データをProjectRequestDetailに保存するために使う。
            dict_expenses["EXTRA_PROJECT_MEMBER"] = project_member
            # 番号
            dict_expenses['NO'] = str(i + 1)
            # 項目
            dict_expenses['ITEM_NAME'] = project_member.member.__unicode__()
            # 時給の場合
            if project.is_hourly_pay:
                # 単価（円）
                dict_expenses['ITEM_PRICE'] = project_member.hourly_pay
                # Min/Max（H）
                dict_expenses['ITEM_MIN_MAX'] = u""
            else:
                # 単価（円）
                dict_expenses['ITEM_PRICE'] = project_member.price
                # Min/Max（H）
                dict_expenses['ITEM_MIN_MAX'] = "%s/%s" % (int(project_member.min_hours), int(project_member.max_hours))
            dict_expenses.update(project_member.get_attendance_dict(first_day.year, first_day.month))
            # 金額合計
            members_amount += dict_expenses['ITEM_AMOUNT_TOTAL']
            detail_members.append(dict_expenses)

    detail_expenses, expenses_amount = get_request_expenses_list(project,
                                                                 first_day.year,
                                                                 '%02d' % (first_day.month,),
                                                                 project_members)

    data['detail_all'] = detail_all
    data['MEMBERS'] = detail_members
    data['EXPENSES'] = detail_expenses  # 清算リスト
    data['DETAIL']['ITEM_AMOUNT_ATTENDANCE'] = members_amount
    if project.client.decimal_type == '0':
        data['DETAIL']['ITEM_AMOUNT_ATTENDANCE_TAX'] = int(round(members_amount * project.client.tax_rate))
    else:
        # 出勤のトータル金額の税金
        data['DETAIL']['ITEM_AMOUNT_ATTENDANCE_TAX'] = int(members_amount * project.client.tax_rate)
    data['DETAIL']['ITEM_AMOUNT_ATTENDANCE_ALL'] = members_amount + int(data['DETAIL']['ITEM_AMOUNT_ATTENDANCE_TAX'])
    data['DETAIL']['ITEM_AMOUNT_ALL'] = int(data['DETAIL']['ITEM_AMOUNT_ATTENDANCE_ALL']) + expenses_amount
    data['DETAIL']['ITEM_AMOUNT_ALL_COMMA'] = humanize.intcomma(data['DETAIL']['ITEM_AMOUNT_ALL'])

    project_request.amount = data['DETAIL']['ITEM_AMOUNT_ALL']
    project_request.turnover_amount = members_amount
    project_request.tax_amount = data['DETAIL']['ITEM_AMOUNT_ATTENDANCE_TAX']
    project_request.expenses_amount = expenses_amount

    return data


def get_request_expenses_list(project, year, month, project_members):
    # 清算リスト
    dict_expenses = {}
    for expenses in project.get_expenses(year, month, project_members):
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
    return detail_expenses, expenses_amount


def get_attendance_time_from_eboa(project_member, year, month):
    """EBOAから出勤時間を取得する。

    :param year:
    :param month:
    :return:
    """
    if not project_member.member.eboa_user_id:
        return 0

    period = '%04d/%02d' % (int(year), int(month))
    eboa_attendances = eboa_models.EbAttendance.objects.filter(applicant__userid=project_member.member.eboa_user_id,
                                                               period=period)
    if eboa_attendances.count() > 0:
        return float(eboa_attendances[0].totaltime)
    else:
        return 0

