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
