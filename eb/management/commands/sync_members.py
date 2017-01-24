# coding: UTF-8
"""
Created on 2016/01/12

@author: Yang Wanjun
"""
import logging
import traceback

from .base_batch import BaseBatch
from eb import biz_batch
from utils import constants

logger = logging.getLogger(__name__)


class Command(BaseBatch):
    BATCH_NAME = constants.BATCH_SYNC_MEMBERS
    BATCH_TITLE = u"社員導入バッチ"
    MAIL_TITLE = u"【営業支援システム】社員導入"

    def handle(self, *args, **options):
        message_list = biz_batch.sync_members()
        if message_list:
            for message in message_list:
                logger.info(u"【%s】code: %s, name: %s, birthday: %s, address: %s, %s" % message)
        else:
            logger.info(u"新入社員がいません。")
