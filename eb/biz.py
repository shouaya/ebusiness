# coding: UTF-8
"""
Created on 2016/01/12

@author: Yang Wanjun
"""
import datetime
import uuid
import StringIO

from django.db.models import Q, Max, Prefetch
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.humanize.templatetags import humanize
from django.utils import timezone
from django.core.urlresolvers import reverse

from utils import common, errors, constants
from eb import models
from . import biz_config
from eboa import models as eboa_models
from contract import models as contract_models


def get_batch_manage(name):
    """バッチ名によてバッチを取得する。

    :param name: バッチ名
    :return:
    """
    try:
        return models.BatchManage.objects.get(name=name)
    except ObjectDoesNotExist:
        return None


def is_salesperson_user(user):
    """該当するユーザーは営業員なのか

    :param user:
    :return:
    """
    if hasattr(user, 'salesperson'):
        return True
    else:
        return False


def get_bp_next_employee_id():
    """自動採番するため、次に使う番号を取得する。

    これは最終的に使う社員番号ではありません。
    実際の番号は追加後の主キーを使って、設定しなおしてから、もう一回保存する 。

    :return: string
    """
    max_id = models.Member.objects.all().aggregate(Max('id'))
    max_id = max_id.get('id__max', None)
    if max_id:
        return 'BP%05d' % (int(max_id) + 1,)
    else:
        return ''


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


def get_year_list():
    start = biz_config.get_year_start()
    end = biz_config.get_year_end()
    return range(int(start), int(end))


def get_members_by_section(all_members, section_id):
    if not section_id:
        return all_members
    today = datetime.date.today()
    return all_members.filter((Q(membersectionperiod__start_date__lte=today) &
                               Q(membersectionperiod__end_date__isnull=True)) |
                              (Q(membersectionperiod__start_date__lte=today) &
                               Q(membersectionperiod__end_date__gte=today)),
                              Q(membersectionperiod__division__pk=section_id) |
                              Q(membersectionperiod__section__pk=section_id) |
                              Q(membersectionperiod__subsection__pk=section_id),
                              membersectionperiod__is_deleted=False)


def get_members_by_salesperson(all_members, salesperson_id):
    if not salesperson_id:
        return all_members
    today = datetime.date.today()
    return all_members.filter((Q(membersalespersonperiod__start_date__lte=today) &
                               Q(membersalespersonperiod__end_date__isnull=True)) |
                              (Q(membersalespersonperiod__start_date__lte=today) &
                               Q(membersalespersonperiod__end_date__gte=today)),
                              membersalespersonperiod__salesperson__pk=salesperson_id,
                              membersalespersonperiod__is_deleted=False)


def get_project_members_by_section(project_members, section_id, date):
    return project_members.filter((Q(member__membersectionperiod__start_date__lte=date) &
                                   Q(member__membersectionperiod__end_date__isnull=date)) |
                                  (Q(member__membersectionperiod__start_date__lte=date) &
                                   Q(member__membersectionperiod__end_date__gte=date)),
                                  Q(member__membersectionperiod__division__pk=section_id) |
                                  Q(member__membersectionperiod__section__pk=section_id) |
                                  Q(member__membersectionperiod__subsection__pk=section_id),
                                  member__membersectionperiod__is_deleted=False).distinct()


def get_project_members_by_salesperson(project_members, salesperson_id, date):
    return project_members.filter((Q(member__membersalespersonperiod__start_date__lte=date) &
                                   Q(member__membersalespersonperiod__end_date__isnull=date)) |
                                  (Q(member__membersalespersonperiod__start_date__lte=date) &
                                   Q(member__membersalespersonperiod__end_date__gte=date)),
                                  member__membersalespersonperiod__salesperson__pk=salesperson_id,
                                  member__membersalespersonperiod__is_deleted=False).distinct()


def get_on_sales_top_org():
    """営業対象のトップレベルの部署を取得する

    :return:
    """
    return models.Section.objects.public_filter(is_on_sales=True, parent__isnull=True)


def get_on_sales_section():
    """営業対象の部署を取得する。

    :return:
    """
    return models.Section.objects.public_filter(is_on_sales=True)


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
    return models.get_sales_members().filter(subcontractor__isnull=False)


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


def get_members_section(section):
    all_members = models.get_sales_members()
    return get_members_by_section(all_members, section.id)


def get_business_partner_members():
    """BPメンバーを取得する

    :return:
    """
    today = datetime.date.today()
    # 現在所属の営業員を取得
    sales_set = models.MemberSalespersonPeriod.objects.filter((Q(start_date__lte=today) & Q(end_date__isnull=True)) |
                                                              (Q(start_date__lte=today) & Q(end_date__gte=today)))
    # 現在の案件
    project_member_set = models.ProjectMember.objects.public_filter(
        start_date__lte=today,
        end_date__gte=today,
        status=2
    )

    queryset = models.Member.objects.filter(
        subcontractor__isnull=False
    ).select_related('subcontractor').order_by('subcontractor')
    return queryset.prefetch_related(
        Prefetch('membersalespersonperiod_set', queryset=sales_set, to_attr='current_salesperson_period'),
        Prefetch('projectmember_set', queryset=project_member_set, to_attr='current_project_member'),
    )


def get_business_partner_members_with_contract():
    queryset = get_business_partner_members()
    contract_set = contract_models.BpContract.objects.public_all().order_by('-start_date')

    return queryset.prefetch_related(
        Prefetch('bpcontract_set', queryset=contract_set, to_attr='latest_contract_set'),
    )


def get_project_members_month_section(section, date, user=None):
    """該当する日付に指定された部署に配属される案件メンバーを取得する。

    :param section: 部署
    :param date: 日付
    :param user:
    :return:
    """
    project_members = models.get_project_members_by_month(date)
    # 出勤情報を取得する
    current_attendance_set = models.MemberAttendance.objects.filter(year="%04d" % date.year,
                                                                    month="%02d" % date.month,
                                                                    is_deleted=False)
    prev_month = common.add_months(date, months=-1)
    prev_attendance_set = models.MemberAttendance.objects.filter(year="%04d" % prev_month.year,
                                                                 month="%02d" % prev_month.month,
                                                                 is_deleted=False)
    # 請求明細情報
    project_request_detail_set = models.ProjectRequestDetail.objects.filter(
        project_request__year="%04d" % date.year,
        project_request__month="%02d" % date.month
    )
    all_children = section.get_children()
    org_pk_list = [org.pk for org in all_children]
    org_pk_list.append(section.pk)

    queryset = project_members.filter((Q(member__membersectionperiod__start_date__lte=date) &
                                       Q(member__membersectionperiod__end_date__isnull=date)) |
                                      (Q(member__membersectionperiod__start_date__lte=date) &
                                       Q(member__membersectionperiod__end_date__gte=date)),
                                      Q(member__membersectionperiod__division__in=org_pk_list) |
                                      Q(member__membersectionperiod__section__in=org_pk_list) |
                                      Q(member__membersectionperiod__subsection__in=org_pk_list),
                                      member__membersectionperiod__is_deleted=False).distinct().prefetch_related(
        Prefetch('member'),
        Prefetch('project'),
        Prefetch('memberattendance_set', queryset=current_attendance_set, to_attr='current_attendance_set'),
        Prefetch('memberattendance_set', queryset=prev_attendance_set, to_attr='prev_attendance_set'),
        Prefetch('projectrequestdetail_set', queryset=project_request_detail_set, to_attr='project_request_detail_set'),
    )
    # 待機案件
    first_day = common.get_first_day_by_month(date)
    last_day = common.get_last_day_by_month(date)
    queryset2 = models.ProjectMember.objects.public_filter(end_date__gte=first_day,
                                                           start_date__lte=last_day,
                                                           project__status=4,
                                                           status=2,
                                                           project__is_reserve=True,
                                                           project__department__in=org_pk_list
                                                           ).distinct().prefetch_related(
        Prefetch('member'),
        Prefetch('project'),
    )

    return queryset | queryset2


def get_lump_projects_by_section(section, date):
    all_children = section.get_children()
    all_children = list(all_children)
    all_children.append(section)
    first_day = common.get_first_day_by_month(date)
    last_day = common.get_last_day_by_month(first_day)

    # 請求情報
    project_request_set = models.ProjectRequest.objects.filter(
        year="%04d" % date.year,
        month="%02d" % date.month
    )
    queryset = models.Project.objects.public_filter(
        is_lump=True,
        department__in=list(all_children),
        start_date__lte=last_day,
        end_date__gte=first_day
    ).distinct().prefetch_related(
        Prefetch('projectrequest_set', queryset=project_request_set, to_attr='project_request_set'),
    )
    return queryset


def get_subcontractor_project_members_month(date):
    """指定月の案件メンバー全部取得する。

    :param date 指定月
    :return
    """
    return models.get_project_members_by_month(date).filter(member__member_type=4)


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
                                                    projectmember__status=2) |
                                                  Q(projectmember__start_date__gte=next_first_day,
                                                      projectmember__start_date__lte=next_last_day,
                                                      projectmember__is_deleted=False,
                                                      projectmember__status=2)).distinct()
    return members.filter(membersectionperiod__section__is_on_sales=True)


def get_subcontractor_release_members_by_month(date):
    """指定年月にリリースする協力社員を取得する。

    :param date 指定月
    """
    return models.get_release_members_by_month(date).filter(member__member_type=4)


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
    today = datetime.date.today()
    working_members = models.ProjectMember.objects.public_filter(start_date__lte=today,
                                                                 end_date__gte=today)
    projects = projects.prefetch_related(
        'projectmember_set',
        Prefetch('projectmember_set', queryset=working_members, to_attr='working_project_members')
    )
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


def get_user_profile(user):
    """ログインしているユーザの詳細情報を取得する。

    :param user ログインしているユーザ
    """
    if hasattr(user, 'salesperson'):
        return user.salesperson
    return None


def generate_bp_order_data(project_member, year, month, contract, user, bp_order, publish_date=None):
    """ＢＰ注文書を作成するためのデータを取得する。

    :param project_member:
    :param year:
    :param month:
    :param contract:
    :param user:
    :param bp_order:
    :param publish_date
    :return:
    """
    if not contract:
        raise errors.CustomException(constants.ERROR_BP_NO_CONTRACT)
    company = get_company()
    first_day = datetime.date(int(year), int(month), 1)
    if project_member.start_date > first_day:
        first_day = project_member.start_date
    last_day = common.get_last_day_by_month(first_day)
    data = {'DETAIL': {}}
    data['DETAIL']['YM'] = '%04d%02d' % (int(year), int(month))
    # 発行年月日
    publish_date = common.get_bp_order_publish_date(year, month, publish_date)
    data['DETAIL']['PUBLISH_DATE'] = common.to_wareki(publish_date)
    # 下請け会社名
    data['DETAIL']['SUBCONTRACTOR_NAME'] = project_member.member.subcontractor.name
    # 下請け会社郵便番号
    if project_member.member.subcontractor.post_code and len(project_member.member.subcontractor.post_code) == 7:
        post_code = project_member.member.subcontractor.post_code[:3] + '-' + \
                    project_member.member.subcontractor.post_code[3:]
    else:
        post_code = ''
    data['DETAIL']['SUBCONTRACTOR_POST_CODE'] = post_code
    # 下請け会社住所
    data['DETAIL']['SUBCONTRACTOR_ADDRESS1'] = project_member.member.subcontractor.address1
    data['DETAIL']['SUBCONTRACTOR_ADDRESS2'] = project_member.member.subcontractor.address2
    # 下請け会社電話番号
    data['DETAIL']['SUBCONTRACTOR_TEL'] = project_member.member.subcontractor.tel
    # 下請け会社ファックス
    data['DETAIL']['SUBCONTRACTOR_FAX'] = project_member.member.subcontractor.fax
    # 委託業務責任者（乙）
    data['DETAIL']['SUBCONTRACTOR_MASTER'] = project_member.member.subcontractor.president
    # 連絡窓口担当者（甲）
    salesperson = project_member.member.get_salesperson(datetime.date(int(year), int(month), 20))
    data['DETAIL']['MIDDLEMAN'] = unicode(salesperson) if salesperson else ''
    # 連絡窓口担当者（乙）
    data['DETAIL']['SUBCONTRACTOR_MIDDLEMAN'] = project_member.member.subcontractor.middleman
    # 作成者
    create_user = get_user_profile(user)
    data['DETAIL']['AUTHOR_FIRST_NAME'] = create_user.first_name if create_user else ''
    # 会社名
    data['DETAIL']['COMPANY_NAME'] = company.name
    # 本社郵便番号
    data['DETAIL']['POST_CODE'] = common.get_full_postcode(company.post_code)
    # 本社電話番号
    data['DETAIL']['TEL'] = company.tel
    # 代表取締役
    data['DETAIL']['MASTER'] = company.president if company.president else ""
    # 本社住所
    data['DETAIL']['ADDRESS1'] = company.address1
    data['DETAIL']['ADDRESS2'] = company.address2
    # 業務名称
    data['DETAIL']['PROJECT_NAME'] = project_member.project.name
    # 作業期間
    data['DETAIL']['START_DATE'] = common.to_wareki(first_day)
    data['DETAIL']['END_DATE'] = common.to_wareki(last_day)
    # 作業責任者
    data['DETAIL']['MEMBER_NAME'] = unicode(project_member.member)
    # 時給
    data['DETAIL']['IS_HOURLY_PAY'] = contract.is_hourly_pay
    # 基本給
    allowance_base = humanize.intcomma(contract.allowance_base + contract.allowance_other) if contract else ''
    if contract.allowance_base_memo:
        allowance_base_memo = contract.allowance_base_memo
    elif contract.is_hourly_pay:
        allowance_base_memo = u"時間単価：￥%s/h  (消費税を含まない)" % allowance_base
    elif contract.is_fixed_cost:
        allowance_base_memo = u"月額基本料金：￥%s円/月  (固定、税金抜き)" % allowance_base
    else:
        allowance_base_memo = u"月額基本料金：￥%s円/月  (税金抜き)" % allowance_base
    data['DETAIL']['ALLOWANCE_BASE'] = allowance_base
    data['DETAIL']['ALLOWANCE_BASE_MEMO'] = allowance_base_memo
    # 固定
    data['DETAIL']['IS_FIXED_COST'] = contract.is_fixed_cost
    # 計算式を表示するか
    data['DETAIL']['IS_SHOW_FORMULA'] = contract.is_show_formula
    if not contract.is_fixed_cost:
        # 超過単価
        allowance_overtime = humanize.intcomma(contract.allowance_overtime) if contract else ''
        if contract.allowance_overtime_memo:
            allowance_overtime_memo = contract.allowance_overtime_memo
        else:
            allowance_overtime_memo = u"超過単価：￥%s/%sh=￥%s/h" % (
                allowance_base, contract.allowance_time_max, allowance_overtime
            )
        data['DETAIL']['ALLOWANCE_OVERTIME'] = allowance_overtime
        data['DETAIL']['ALLOWANCE_OVERTIME_MEMO'] = allowance_overtime_memo
        # 不足単価
        allowance_absenteeism = humanize.intcomma(contract.allowance_absenteeism) if contract else ''
        if contract.allowance_absenteeism_memo:
            allowance_absenteeism_memo = contract.allowance_absenteeism_memo
        else:
            allowance_absenteeism_memo = u"不足単価：￥%s/%sh=￥%s/h" % (
                allowance_base, contract.allowance_time_min, allowance_absenteeism
            )
        data['DETAIL']['ALLOWANCE_ABSENTEEISM'] = allowance_absenteeism
        data['DETAIL']['ALLOWANCE_ABSENTEEISM_MEMO'] = allowance_absenteeism_memo
        # 基準時間
        data['DETAIL']['ALLOWANCE_TIME_MIN'] = unicode(contract.allowance_time_min)
        data['DETAIL']['ALLOWANCE_TIME_MAX'] = unicode(contract.allowance_time_max)
        if contract.allowance_time_memo:
            allowance_time_memo = contract.allowance_time_memo
        else:
            allowance_time_memo = u"※基準時間：%s～%sh/月" % (contract.allowance_time_min, contract.allowance_time_max)
        data['DETAIL']['ALLOWANCE_TIME_MEMO'] = allowance_time_memo
    # 追記コメント
    data['DETAIL']['COMMENT'] = contract.comment
    # 作業場所
    data['DETAIL']['LOCATION'] = project_member.project.address if project_member.project.address else u"弊社指定場所"
    # 納入物件
    data['DETAIL']['DELIVERY_PROPERTIES'] = models.Config.get_bp_order_delivery_properties()
    # 支払条件
    data['DETAIL']['PAYMENT_CONDITION'] = models.Config.get_bp_order_payment_condition()
    # 契約条項
    data['DETAIL']['CONTRACT_ITEMS'] = models.Config.get_bp_order_contract_items()

    data['DETAIL']['ORDER_NO'] = bp_order.order_no
    return data


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
    member = get_master()
    data['DETAIL']['MASTER'] = company.president
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
            first_day = common.get_first_day_from_ym(ym)
            last_day = common.get_last_day_by_month(first_day)
            for pm_id in member_id_list:
                try:
                    project_members.append(
                        models.ProjectMember.objects.get(pk=int(pm_id), is_deleted=False, status=2,
                                                         start_date__lte=last_day,
                                                         end_date__gte=first_day))
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
    data['DETAIL']['CLIENT_ADDRESS'] = (project.client.address1 or '') + (project.client.address2 or '')
    # お客様電話番号
    data['DETAIL']['CLIENT_TEL'] = project.client.tel or ''
    # お客様名称
    data['DETAIL']['CLIENT_COMPANY_NAME'] = project.client.name
    # 作業期間
    f = u'%Y年%m月%d日'
    period_start = first_day.strftime(f.encode('utf-8')).decode('utf-8')
    period_end = last_day.strftime(f.encode('utf-8')).decode('utf-8')
    data['DETAIL']['WORK_PERIOD'] = period_start + u" ～ " + period_end
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
    data['DETAIL']['ADDRESS'] = (company.address1 or '') + (company.address2 or '')
    # 会社名
    data['DETAIL']['COMPANY_NAME'] = company.name
    # 代表取締役
    member = get_master()
    data['DETAIL']['MASTER'] = company.president
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
        detail_all['ITEM_COMMENT'] = project.lump_comment if project.is_lump and project.lump_comment else u""
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
                dict_expenses['ITEM_PRICE'] = project_member.hourly_pay or 0
                # Min/Max（H）
                dict_expenses['ITEM_MIN_MAX'] = u""
            else:
                # 単価（円）
                dict_expenses['ITEM_PRICE'] = project_member.price or 0
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


def generate_subcontractor_request_data(subcontractor, year, month, subcontractor_request):
    company = get_company()
    first_day = common.get_first_day_by_month(datetime.date(int(year), int(month), 1))
    last_day = common.get_last_day_by_month(first_day)
    data = {'DETAIL': {}, 'EXTRA': {}}
    data['EXTRA']['YM'] = first_day.strftime('%Y%m')
    data['EXTRA']['COMPANY'] = company
    # お客様郵便番号
    data['DETAIL']['CLIENT_POST_CODE'] = common.get_full_postcode(company.post_code)
    # お客様住所
    data['DETAIL']['CLIENT_ADDRESS'] = (company.address1 or '') + (company.address2 or '')
    # お客様電話番号
    data['DETAIL']['CLIENT_TEL'] = company.tel or ''
    # お客様名称
    data['DETAIL']['CLIENT_COMPANY_NAME'] = company.name
    # 作業期間
    f = u'%Y年%m月%d日'
    period_start = first_day.strftime(f.encode('utf-8')).decode('utf-8')
    period_end = last_day.strftime(f.encode('utf-8')).decode('utf-8')
    data['DETAIL']['WORK_PERIOD'] = period_start + u" ～ " + period_end
    data['EXTRA']['WORK_PERIOD_START'] = first_day
    data['EXTRA']['WORK_PERIOD_END'] = last_day
    # 注文番号
    data['DETAIL']['ORDER_NO'] = u""
    # 注文日
    data['DETAIL']['REQUEST_DATE'] = u""
    # 契約件名
    data['DETAIL']['CONTRACT_NAME'] = u""
    # 部署名称
    data['DETAIL']['ORG_NAME'] = unicode(subcontractor_request.section)
    # お支払い期限
    data['DETAIL']['REMIT_DATE'] = company.get_pay_date(date=first_day).strftime('%Y/%m/%d')
    data['EXTRA']['REMIT_DATE'] = company.get_pay_date(date=first_day)
    # 請求番号
    data['DETAIL']['REQUEST_NO'] = subcontractor_request.request_no
    # 発行日（対象月の最終日）
    data['DETAIL']['PUBLISH_DATE'] = last_day.strftime(u"%Y年%m月%d日".encode('utf-8')).decode('utf-8')
    data['EXTRA']['PUBLISH_DATE'] = last_day
    # 本社郵便番号
    data['DETAIL']['POST_CODE'] = common.get_full_postcode(subcontractor.post_code)
    # 本社住所
    data['DETAIL']['ADDRESS'] = (subcontractor.address1 or '') + (subcontractor.address2 or '')
    # 会社名
    data['DETAIL']['COMPANY_NAME'] = subcontractor.name
    # 代表取締役
    data['DETAIL']['MASTER'] = subcontractor.president
    # 本社電話番号
    data['DETAIL']['TEL'] = subcontractor.tel
    # 振込先銀行名称
    if subcontractor.subcontractorbankinfo_set.all().count() == 0:
        bank_info = None
    else:
        bank_info = subcontractor.subcontractorbankinfo_set.all()[0]
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

    section_members = subcontractor.get_members_by_month_and_section(year, month, subcontractor_request.section)
    members_amount = 0
    if False:
        members_amount = 0
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
        detail_all['ITEM_COMMENT'] = u""
    else:
        for i, member in enumerate(section_members):
            member_attendance_set = models.MemberAttendance.objects.public_filter(
                project_member__member=member,
                year=year,
                month=month,
            )
            if member_attendance_set.count() > 0:
                member_attendance = member_attendance_set[0]
                contract_list = member.bpcontract_set.filter(
                    start_date__lte=last_day,
                    is_deleted=False,
                ).order_by('-start_date')
                if contract_list.count() > 0:
                    contract = contract_list[0]
                    dict_expenses = dict()
                    # この項目は請求書の出力ではなく、履歴データをProjectRequestDetailに保存するために使う。
                    dict_expenses["EXTRA_PROJECT_MEMBER"] = member_attendance.project_member
                    # 番号
                    dict_expenses['NO'] = str(i + 1)
                    # 項目
                    dict_expenses['ITEM_NAME'] = unicode(member)
                    # 時給の場合
                    if contract.is_hourly_pay:
                        # 単価（円）
                        dict_expenses['ITEM_PRICE'] = contract.allowance_base or 0
                        # Min/Max（H）
                        dict_expenses['ITEM_MIN_MAX'] = u""
                    else:
                        # 単価（円）
                        dict_expenses['ITEM_PRICE'] = contract.get_cost() or 0
                        # Min/Max（H）
                        dict_expenses['ITEM_MIN_MAX'] = "%s/%s" % (
                            int(contract.allowance_time_min), int(contract.allowance_time_min)
                        )
                    dict_expenses.update(member_attendance.project_member.get_attendance_dict(first_day.year, first_day.month))
                    # 金額合計
                    members_amount += dict_expenses['ITEM_AMOUNT_TOTAL']
                    detail_members.append(dict_expenses)

    # detail_expenses, expenses_amount = get_request_expenses_list(project,
    #                                                              first_day.year,
    #                                                              '%02d' % (first_day.month,),
    #                                                              project_members)
    detail_expenses, expenses_amount = [], 0

    data['detail_all'] = detail_all
    data['MEMBERS'] = detail_members
    data['EXPENSES'] = detail_expenses  # 清算リスト
    data['DETAIL']['ITEM_AMOUNT_ATTENDANCE'] = members_amount
    if company.decimal_type == '0':
        data['DETAIL']['ITEM_AMOUNT_ATTENDANCE_TAX'] = int(round(members_amount * company.tax_rate))
    else:
        # 出勤のトータル金額の税金
        data['DETAIL']['ITEM_AMOUNT_ATTENDANCE_TAX'] = int(members_amount * company.tax_rate)
    data['DETAIL']['ITEM_AMOUNT_ATTENDANCE_ALL'] = members_amount + int(data['DETAIL']['ITEM_AMOUNT_ATTENDANCE_TAX'])
    data['DETAIL']['ITEM_AMOUNT_ALL'] = int(data['DETAIL']['ITEM_AMOUNT_ATTENDANCE_ALL']) + expenses_amount
    data['DETAIL']['ITEM_AMOUNT_ALL_COMMA'] = humanize.intcomma(data['DETAIL']['ITEM_AMOUNT_ALL'])

    subcontractor_request.amount = data['DETAIL']['ITEM_AMOUNT_ALL']
    subcontractor_request.turnover_amount = members_amount
    subcontractor_request.tax_amount = data['DETAIL']['ITEM_AMOUNT_ATTENDANCE_TAX']
    subcontractor_request.expenses_amount = expenses_amount

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

    :param project_member:
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


def get_master():
    # 代表取締役を取得する。
    members = models.Salesperson.objects.public_filter(member_type=7)
    if members.count() == 1:
        return members[0]
    else:
        return None


def is_first_login(user):
    """初めてのログインなのかどうか

    :param user:
    :return:
    """
    try:
        User.objects.get(username=user.username, last_login__isnull=True)
        return True
    except ObjectDoesNotExist:
        return False
    except MultipleObjectsReturned:
        return False


def gen_qr_code(url_schema, domain):
    import qrcode
    uid = uuid.uuid4()
    # url = domain + reverse('login_qr') + "?uid=" + str(uid)
    url = "%s://%s%s?uid=%s" % (url_schema, domain, reverse('login_qr'), str(uid))
    img = qrcode.make(url)
    output = StringIO.StringIO()
    img.save(output, "PNG")
    contents = output.getvalue().encode("base64")
    output.close()
    return contents
