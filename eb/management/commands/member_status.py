# coding: UTF-8
"""
Created on 2017/01/20

@author: Yang Wanjun
"""
import logging
import traceback
from eb import biz_batch
from utils import constants
from base_batch import BaseBatch

logger = logging.getLogger(__name__)


class Command(BaseBatch):
    BATCH_NAME = constants.BATCH_MEMBER_STATUS
    BATCH_TITLE = u"社員稼働状況バッチ"
    MAIL_TITLE = u"【営業支援システム】社員稼働状況"

    def handle(self, *args, **options):
        status_list, summary = biz_batch.get_members_information()
        biz_batch.notify_member_status_mails(self.batch, status_list, summary)
