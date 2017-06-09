# coding: UTF-8
"""
Created on 2017/05/26

@author: Yang Wanjun
"""
import logging

from .base_batch import BaseBatch
from eb import biz_batch
from utils import constants

logger = logging.getLogger(__name__)


class Command(BaseBatch):
    BATCH_NAME = constants.BATCH_PUSH_NEW_MEMBER
    BATCH_TITLE = u"新入社員プッシュ通知"
    MAIL_TITLE = u"【営業支援システム】新入社員通知"

    def handle(self, *args, **options):
        username = options.get('username')

        logger.info(u"バッチ実行開始。username: %s" % username)
        biz_batch.batch_push_new_member(self.batch)
