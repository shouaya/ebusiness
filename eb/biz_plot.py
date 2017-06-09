# -*- coding: utf-8 -*-
"""
Created on 2016/06/02

@author: Yang Wanjun
"""
from __future__ import unicode_literals
import platform
import StringIO
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

from django.db import connection
from django.db.models import Sum, CharField, Case, Value, When
from django.db.models.functions import Concat
from django.contrib.humanize.templatetags import humanize
from eb import models


if platform.system() == "Darwin":
    matplotlib.rcParams['font.family'] = 'AppleGothic'


def members_status_bar():
    df = pd.read_sql("""select first_day
         , (select count(distinct m.id)
              from eb_member m
              join eb_projectmember pm on m.id = pm.member_id
              join eb_project p on p.id = pm.project_id
             where pm.start_date <= last_day
               and pm.end_date >= first_day
               and m.is_deleted = 0
               and pm.is_deleted = 0
               and pm.status = 2
               and p.is_reserve = 0
               and exists(select 1 from eb_membersectionperiod msp where msp.member_id = m.id and msp.is_deleted=0)
               and (m.is_retired = 0 or (m.is_retired = 1 and m.retired_date >= last_day))) as working_count
         , (select count(distinct m.id)
              from eb_member m
             where m.is_deleted = 0
               and (m.is_retired = 0 or (m.is_retired = 1 and m.retired_date > last_day))
               and m.is_on_sales = 1
               and m.join_date <= last_day
               and exists(select 1 from eb_membersectionperiod msp join eb_section s on s.id = msp.section_id
                           where msp.member_id = m.id and msp.is_deleted=0 and s.is_on_sales = 1)
               and not exists(select 1
                                from eb_projectmember pm where pm.member_id = m.id
                                 and pm.start_date <= last_day and pm.end_date >= first_day and pm.is_deleted = 0)
           ) as waiting_count
      from (
    select first_day, LAST_DAY(first_day) as last_day
      from (select DATE_ADD('2016-01-01', INTERVAL t1.i*10 + t0.i MONTH) first_day
              from (select 0 i union select 1 union select 2 union select 3 union select 4 union
                    select 5 union select 6 union select 7 union select 8 union select 9) t0,
                   (select 0 i union select 1 union select 2 union select 3 union select 4 union
                    select 5 union select 6 union select 7 union select 8 union select 9) t1
           ) v
     where first_day between '2016-05-01' and DATE_ADD(CURRENT_DATE(), INTERVAL 2 MONTH)
    ) dates""", connection)
    ax = plt.subplot()
    member_df = df.loc[:, ['working_count', 'waiting_count']]
    member_df.index = df.first_day.map(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').date().strftime('%y.%m'))
    member_df.rename(columns={'working_count': '稼働社員数', 'waiting_count': '待機社員数'}, inplace=True)
    member_df.plot(ax=ax, kind='bar', stacked=True, figsize=(10.8, 2))

    ax.set_xlabel('')
    ax.grid(alpha=0.3)
    for tick in ax.get_xticklabels():
        tick.set_rotation(15)

    plt.tight_layout()

    img_data = StringIO.StringIO()
    plt.savefig(img_data, format='png')
    img_data.seek(0)
    plt.close()
    return img_data


def business_type_pie(year, data_type):
    if data_type == 1:
        ym_start = '%s01' % year
        ym_end = '%s12' % year
    else:
        ym_start = '%s04' % year
        ym_end = '%s03' % (int(year) + 1)

    queryset = models.ProjectRequest.objects.annotate(ym=Concat('year', 'month')).filter(
        project__business_type__isnull=False,
        ym__gte=ym_start,
        ym__lte=ym_end
    ).values('project__business_type').annotate(
        turnover_amount=Sum('turnover_amount'),
        type_name=Case(
            When(project__business_type='01', then=Value('金融（銀行）')),
            When(project__business_type='02', then=Value('金融（保険）')),
            When(project__business_type='03', then=Value('金融（証券）')),
            When(project__business_type='04', then=Value('製造　　　　')),
            When(project__business_type='05', then=Value('サービス　　')),
            When(project__business_type='06', then=Value('その他　　　')),
            default=Value('Unknown'),
            output_field=CharField(),
        ),
    ).order_by('project__business_type').distinct()

    df = pd.DataFrame(list(queryset))
    # s_percent = df.turnover_amount.map(lambda x: "%.2f%%" % (x * 100.0 / df.turnover_amount.sum()))
    # type_name_per = df.type_name.str.cat(s_percent, sep=' ')
    s_amount = df.turnover_amount.map(lambda x: humanize.intcomma(x).rjust(15))
    s_type_name_amount = df.type_name.str.cat(s_amount.astype(str), sep=' ')
    series = pd.Series(df.turnover_amount, name='')
    ax = plt.subplot()
    series.plot.pie(ax=ax, figsize=(6, 6), labels=[''] * len(series), autopct='%.2f%%', pctdistance=0.8,
                    wedgeprops={'linewidth': 1, 'edgecolor': "white"})
    ax.legend(loc=(1.01, 0.45), labels=s_type_name_amount)
    ax.set_title("%s年度(%s～%s) の事業別売上ブレイクダウン" % (year, ym_start, ym_end))
    plt.tight_layout()

    img_data = StringIO.StringIO()
    plt.savefig(img_data, format='png', bbox_inches='tight')
    img_data.seek(0)
    plt.close()
    return img_data
