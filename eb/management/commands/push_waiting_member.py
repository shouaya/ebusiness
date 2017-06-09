# coding: UTF-8
"""
Created on 2017/06/02

@author: Yang Wanjun
"""
import logging

from .base_batch import BaseBatch
from eb import biz_batch
from utils import constants

logger = logging.getLogger(__name__)


class Command(BaseBatch):
    BATCH_NAME = constants.BATCH_PUSH_WAITING_MEMBER
    BATCH_TITLE = u"待機社員プッシュ通知"
    MAIL_TITLE = u"【営業支援システム】待機メンバー通知"

    def handle(self, *args, **options):
        username = options.get('username')

        logger.info(u"バッチ実行開始。username: %s" % username)
        biz_batch.batch_push_waiting_member(self.batch)
