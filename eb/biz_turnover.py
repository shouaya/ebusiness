# -*- coding: utf-8 -*-
"""
Created on 2016/06/02

@author: Yang Wanjun
"""
from __future__ import unicode_literals
# import pandas as pd
# import StringIO
# import matplotlib.pyplot as plt
# from matplotlib.font_manager import FontProperties
# from matplotlib.ticker import FuncFormatter

from eb import models

from django.db.models import Sum
from django.db.models.functions import Concat
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django.contrib.humanize.templatetags import humanize


def turnover_company_year():
    """年単位の会社の売上情報を取得する。

    :return: QuerySet
    """
    turnover_year = models.ProjectRequest.objects.filter(projectrequestheading__isnull=False).\
        values('year',).\
        annotate(amount__sum=Sum('amount'),
                 turnover_amount=Sum('turnover_amount'),
                 tax_amount=Sum('tax_amount'),
                 expenses_amount=Sum('expenses_amount')).distinct()\
        .order_by('year')
    for d in turnover_year:
        cost = models.ProjectRequestDetail.objects.filter(project_request__year=d['year']).aggregate(Sum('cost'))
        d['cost_amount'] = cost.get('cost__sum', 0)

    return turnover_year


def turnover_company_year2():
    """年単位の会社の売上情報を取得する。

    :return: QuerySet
    """
    turnover_year = models.ProjectRequest.objects.filter(projectrequestheading__isnull=False).\
        values('year',).distinct().order_by('year')
    for d in turnover_year:
        queryset = models.ProjectRequest.objects.annotate(ym=Concat('year', 'month')).filter(
            projectrequestheading__isnull=False,
            ym__gte='%s04' % d['year'],
            ym__lte='%s03' % (int(d['year']) + 1)
        ).distinct()
        d['amount__sum'] = queryset.aggregate(Sum('amount')).get('amount__sum', 0)
        d['turnover_amount'] = queryset.aggregate(Sum('turnover_amount')).get('turnover_amount__sum', 0)
        d['tax_amount'] = queryset.aggregate(Sum('tax_amount')).get('tax_amount__sum', 0)
        d['expenses_amount'] = queryset.aggregate(Sum('expenses_amount')).get('expenses_amount__sum', 0)
        cost = models.ProjectRequestDetail.objects.annotate(ym=Concat('project_request__year',
                                                                      'project_request__month')).filter(
            ym__gte='%s04' % d['year'],
            ym__lte='%s03' % (int(d['year']) + 1)
        ).aggregate(Sum('cost'))
        d['cost_amount'] = cost.get('cost__sum', 0)

    return turnover_year


def turnover_company_monthly():
    """月単位の会社の売上情報を取得する。

    :return: QuerySet
    """
    turnover_monthly = models.ProjectRequest.objects.filter(projectrequestheading__isnull=False).\
        values('year', 'month').\
        annotate(amount__sum=Sum('amount'),
                 turnover_amount=Sum('turnover_amount'),
                 tax_amount=Sum('tax_amount'),
                 expenses_amount=Sum('expenses_amount')).distinct()\
        .order_by('year', 'month')
    for d in turnover_monthly:
        d['ym'] = d['year'] + d['month']
        cost = models.ProjectRequestDetail.objects.filter(project_request__year=d['year'],
                                                          project_request__month=d['month']).aggregate(Sum('cost'))
        d['cost_amount'] = cost.get('cost__sum', 0)

    return turnover_monthly


def get_turnover_sections(ym):
    """全ての部署を取得する

    メンバー売上画面にて、絞り込み条件の部署のドロップダウンに使う。
    """
    sections = models.Section.objects.public_filter(projectrequestdetail__project_request__year=ym[:4],
                                                    projectrequestdetail__project_request__month=ym[4:]).distinct()
    return sections


def sections_turnover_monthly(ym):
    """部署別の売上を取得する。

    :param ym: 対象年月
    :return:
    """
    turnover_details = models.ProjectRequestDetail.objects.filter(project_request__year=ym[:4],
                                                                  project_request__month=ym[4:]).\
        values('member_section').annotate(cost_amount=Sum('cost'),
                                          attendance_amount=Sum('total_price'),
                                          expenses_amount=Sum('expenses_price')).order_by('member_section').distinct()
    sections_turnover = []
    for turnover_detail in turnover_details:
        d = dict()
        d['section'] = models.Section.objects.get(pk=turnover_detail['member_section'])
        d['cost_amount'] = turnover_detail['cost_amount']
        d['attendance_amount'] = turnover_detail['attendance_amount']
        d['attendance_tex'] = int(d['attendance_amount'] * 0.08)
        d['expenses_amount'] = turnover_detail['expenses_amount']
        d['all_amount'] = d['attendance_amount'] + d['attendance_tex'] + d['expenses_amount']
        sections_turnover.append(d)
    return sections_turnover


def salesperson_turnover_monthly(ym):
    """営業員別の売上を取得する。

    :param ym: 対象年月
    :return:
    """
    turnover_details = models.ProjectRequestDetail.objects.filter(project_request__year=ym[:4],
                                                                  project_request__month=ym[4:]).\
        values('salesperson').annotate(cost_amount=Sum('cost'),
                                       attendance_amount=Sum('total_price'),
                                       expenses_amount=Sum('expenses_price')).\
        order_by('salesperson').distinct()
    salesperson_turnover = []
    for turnover_detail in turnover_details:
        d = dict()
        try:
            salesperson = models.Salesperson.objects.get(pk=turnover_detail['salesperson'])
        except ObjectDoesNotExist:
            salesperson = None
        d['salesperson'] = salesperson
        d['cost_amount'] = turnover_detail['cost_amount']
        d['attendance_amount'] = turnover_detail['attendance_amount']
        d['attendance_tex'] = int(d['attendance_amount'] * 0.08)
        d['expenses_amount'] = turnover_detail['expenses_amount']
        d['all_amount'] = d['attendance_amount'] + d['attendance_tex'] + d['expenses_amount']
        salesperson_turnover.append(d)
    return salesperson_turnover


def clients_turnover_yearly(year):
    """お客様別の年間売上を取得する。

    :param year: 対象年
    :return:
    """
    turnover_details = models.ProjectRequest.objects.order_by().filter(year=year,
                                                                       projectrequestheading__client__isnull=False). \
        values('projectrequestheading__client').annotate(attendance_amount=Sum('turnover_amount'),
                                                         tax_amount=Sum('tax_amount'),
                                                         expenses_amount=Sum('expenses_amount'),
                                                         all_amount=Sum('amount')).\
        order_by('projectrequestheading__client').distinct()
    clients_turnover = []
    for turnover_detail in turnover_details:
        d = dict()
        d['client'] = models.Client.objects.get(pk=turnover_detail['projectrequestheading__client'])
        d['attendance_amount'] = turnover_detail['attendance_amount']
        d['attendance_tex'] = turnover_detail['tax_amount']
        d['expenses_amount'] = turnover_detail['expenses_amount']
        d['all_amount'] = turnover_detail['all_amount']
        clients_turnover.append(d)
    return clients_turnover


def clients_turnover_yearly2(year):
    """お客様別の年間売上を取得する。

    :param year: 対象年
    :return:
    """
    ym_start = '%s04' % year
    ym_end = '%s03' % (int(year) + 1)

    turnover_details = models.ProjectRequest.objects.order_by().annotate(ym=Concat('year', 'month')).filter(
        ym__gte=ym_start,
        ym__lte=ym_end,
        projectrequestheading__client__isnull=False,
        projectrequestheading__isnull=False
    ).values('projectrequestheading__client').annotate(
        attendance_amount=Sum('turnover_amount'),
        tax_amount=Sum('tax_amount'),
        expenses_amount=Sum('expenses_amount'),
        all_amount=Sum('amount')
    ).order_by('projectrequestheading__client').distinct()
    clients_turnover = []
    for turnover_detail in turnover_details:
        d = dict()
        d['client'] = models.Client.objects.get(pk=turnover_detail['projectrequestheading__client'])
        d['attendance_amount'] = turnover_detail['attendance_amount']
        d['attendance_tex'] = turnover_detail['tax_amount']
        d['expenses_amount'] = turnover_detail['expenses_amount']
        d['all_amount'] = turnover_detail['all_amount']
        clients_turnover.append(d)
    return clients_turnover


def client_turnover_monthly(client):
    # df = pd.read_sql("select r.year"
    #                  "     , r.month"
    #                  "     , r.amount"
    #                  "     , r.expenses_amount"
    #                  "     , r.tax_amount"
    #                  "     , r.turnover_amount"
    #                  "     , (select count(1) "
    #                  "          from eb_projectmember pm2 "
    #                  "		 where pm2.id in (select project_member_id "
    #                  "                            from eb_projectrequestdetail d "
    #                  "						   where d.project_request_id=r.id)"
    #                  "	   ) as member_count"
    #                  "  from eb_projectrequest r "
    #                  "  join eb_projectrequestheading h on r.id = h.project_request_id"
    #                  "  join eb_project p on p.id = r.project_id"
    #                  " where h.client_id = %s" % client.pk, connection)
    # grouped = df.groupby(['year', 'month'])
    # sum_df = grouped.sum()
    # # fp = FontProperties(fname=r'c:\Windows\Fonts\arial.ttf')
    # fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(11, 5))
    # turnover_df = pd.DataFrame(sum_df, columns=['turnover_amount', 'tax_amount', 'expenses_amount'])
    # turnover_df.rename(columns={'turnover_amount': '売上（税抜）', 'tax_amount': '税金', 'expenses_amount': '精算'}, inplace=True)
    # turnover_df.plot(ax=axes[0], kind='bar', stacked=True)
    # # axes[0].set_title("売上（税別）", fontdict={'fontproperties':fp})
    # sum_df['member_count'].plot(ax=axes[1], kind='bar')
    #
    # def x_ax_format(x, p):
    #     index = turnover_df.index.values[x]
    #     return '%s/%s' % (index[0][2:], index[1])
    #
    # def y_ax_format(y, p):
    #     if y >= 1000000:
    #         return '%0dM円' % (y / 1000000)
    #     elif y >= 1000:
    #         return '%0dK円' % (y / 1000)
    #     elif y == 0:
    #         return '0円'
    #     else:
    #         return y
    # axes[0].set_xlabel('売上')
    # axes[0].grid(alpha=0.3)
    # axes[0].get_xaxis().set_major_formatter(FuncFormatter(x_ax_format))
    # axes[0].get_yaxis().set_major_formatter(FuncFormatter(y_ax_format))
    # axes[1].set_xlabel('人数')
    # axes[1].grid(alpha=0.3)
    # axes[1].get_xaxis().set_major_formatter(FuncFormatter(x_ax_format))
    # axes[1].get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: '%d人' % x))
    # for ax in axes:
    #     for tick in ax.get_xticklabels():
    #         tick.set_rotation(30)
    #
    # for i, v in enumerate(sum_df['amount']):
    #     axes[0].text(i, v + 1, '%sK' % (humanize.intcomma(int(round(v / 1000)))), color='black', fontsize=8)
    # for i, v in enumerate(sum_df['member_count']):
    #     axes[1].text(i, v, str(v), color='black', fontsize=8)
    #
    # plt.tight_layout()
    #
    # img_data = StringIO.StringIO()
    # plt.savefig(img_data, format='png')
    # img_data.seek(0)
    # return img_data
    return None


def clients_turnover_monthly(ym):
    """営業員別の売上を取得する。

    :param ym: 対象年月
    :return:
    """
    turnover_details = models.ProjectRequest.objects.order_by().filter(year=ym[:4],
                                                                       month=ym[4:],
                                                                       projectrequestheading__client__isnull=False). \
        values('projectrequestheading__client').annotate(attendance_amount=Sum('turnover_amount'),
                                                         tax_amount=Sum('tax_amount'),
                                                         expenses_amount=Sum('expenses_amount'),
                                                         all_amount=Sum('amount')).\
        order_by('projectrequestheading__client').distinct()
    clients_turnover = []
    for turnover_detail in turnover_details:
        d = dict()
        d['client'] = models.Client.objects.get(pk=turnover_detail['projectrequestheading__client'])
        d['attendance_amount'] = turnover_detail['attendance_amount']
        d['attendance_tex'] = turnover_detail['tax_amount']
        d['expenses_amount'] = turnover_detail['expenses_amount']
        d['all_amount'] = turnover_detail['all_amount']
        clients_turnover.append(d)
    return clients_turnover


def turnover_client_monthly(client_id, ym):
    """案件別の売上を取得する。

    :param client_id: お客様
    :param ym: 対象年月
    :return:
    """
    turnover_details = models.ProjectRequest.objects.order_by().filter(year=ym[:4],
                                                                       month=ym[4:],
                                                                       projectrequestheading__client__id=client_id). \
        values('project').annotate(attendance_amount=Sum('turnover_amount'),
                                   tax_amount=Sum('tax_amount'),
                                   expenses_amount=Sum('expenses_amount'),
                                   all_amount=Sum('amount'))
    for turnover_detail in turnover_details:
        turnover_detail['project'] = models.Project.objects.get(pk=turnover_detail['project'])
    return turnover_details


def members_turnover_monthly(ym, q=None, o=None):
    turnover_details = models.ProjectRequestDetail.objects.filter(project_request__year=ym[:4],
                                                                  project_request__month=ym[4:])
    if q:
        turnover_details = turnover_details.filter(**q)
    if o:
        turnover_details = turnover_details.order_by(*o)

    return turnover_details
