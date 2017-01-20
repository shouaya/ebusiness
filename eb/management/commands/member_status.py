# coding: UTF-8
"""
Created on 2017/01/20

@author: Yang Wanjun
"""
import logging
import os
import traceback
from eb import biz, biz_batch, models
from base_batch import BaseBatch

from django.conf import settings
from django.core.management.base import BaseCommand
from django.template import Context, Template


logger = logging.getLogger(__name__)


class Command(BaseBatch):
    BATCH_TITLE = u"社員稼働状況バッチ"
    MAIL_TITLE = u"【営業支援システム】社員稼働状況"

    def handle(self, *args, **options):
        status_list, summary = get_members_information()
        print str(summary)


def get_members_information():
    all_members = biz.get_sales_members()
    working_members = biz.get_working_members()
    waiting_members = biz.get_waiting_members()
    current_month_release = biz.get_release_current_month()
    next_month_release = biz.get_release_next_month()
    next_2_month_release = biz.get_release_next_2_month()

    summary = {'all_member_count': all_members.count(),
               'working_member_count': working_members.count(),
               'waiting_member_count': waiting_members.count(),
               'current_month_count': current_month_release.count(),
               'next_month_count': next_month_release.count(),
               'next_2_month_count': next_2_month_release.count(),
              }

    status_list = []
    for salesperson in models.Salesperson.objects.public_filter(user__isnull=False, member_type=5):
        d = dict()
        d['salesperson'] = salesperson
        d['all_member_count'] = biz.get_members_by_salesperson(all_members, salesperson.id).count()
        d['working_member_count'] = biz.get_members_by_salesperson(all_members, salesperson.id).count()
        d['waiting_member_count'] = biz.get_members_by_salesperson(all_members, salesperson.id).count()
        d['current_month_count'] = biz.get_members_by_salesperson(all_members, salesperson.id).count()
        d['next_month_count'] = biz.get_members_by_salesperson(all_members, salesperson.id).count()
        d['next_2_month_count'] = biz.get_members_by_salesperson(all_members, salesperson.id).count()
        status_list.append(d)

    return status_list, summary
