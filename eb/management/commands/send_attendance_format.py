# coding: UTF-8
"""
Created on 2017/01/24

@author: Yang Wanjun
"""
import logging
import datetime
from eb import biz_batch
from utils import constants
from base_batch import BaseBatch

logger = logging.getLogger(__name__)


class Command(BaseBatch):
    BATCH_NAME = constants.BATCH_SEND_ATTENDANCE_FORMAT
    BATCH_TITLE = u"出勤フォーマットの送付バッチ"
    MAIL_TITLE = u"【営業支援システム】出勤フォーマットの送付"

    def handle(self, *args, **options):
        ymd = options.get('ymd')
        date = datetime.datetime.strptime(ymd, '%Y%m%d')
        biz_batch.send_attendance_format(self.batch, date)

    def add_arguments(self, parser):
        date = datetime.date.today()
        parser.add_argument('--ymd', default=date.strftime('%Y%m%d'))
