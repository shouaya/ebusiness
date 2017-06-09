# coding: UTF-8
"""
Created on 2017/06/08

@author: Yang Wanjun
"""
import logging
import datetime

from django.core.management.base import CommandError
from .base_batch import BaseBatch
from eb import biz_batch
from utils import constants

logger = logging.getLogger(__name__)


class Command(BaseBatch):
    BATCH_NAME = constants.BATCH_SYNC_MEMBERS_COST
    BATCH_TITLE = u"社員コスト同期バッチ"
    MAIL_TITLE = u"【営業支援システム】社員コスト同期"

    def handle(self, *args, **options):
        year = options.get('year', None)
        month = options.get('month', None)
        username = options.get('username')
        if not year and not month:
            year = datetime.date.today().year
            month = datetime.date.today().month
        if not year or not month or month < 0 or month > 12 or len(str(year)) != 4:
            raise CommandError(u"{year: %s, month: %s}は正しい年月ではありません！" % (year, month))
        logger.info(u"%s年%s月のコスト同期を開始します。username: %s" % (year, month, username))
        biz_batch.batch_sync_members_cost(self.batch, year, month, username)

    def add_arguments(self, parser):
        parser.add_argument('year', nargs='?', type=int)
        parser.add_argument('month', nargs='?', type=int)
        super(Command, self).add_arguments(parser)
