# coding: UTF-8
"""
Created on 2017/01/24

@author: Yang Wanjun
"""
import logging
import traceback
from eb import biz_batch
from utils import constants
from base_batch import BaseBatch

logger = logging.getLogger(__name__)


class Command(BaseBatch):
    BATCH_NAME = constants.BATCH_SEND_ATTENDANCE_FORMAT
    BATCH_TITLE = u"出勤フォーマットの送付バッチ"
    MAIL_TITLE = u"【営業支援システム】出勤フォーマットの送付"

    def handle(self, *args, **options):
        biz_batch.send_attendance_format(self.batch)
