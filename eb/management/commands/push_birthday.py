# coding: UTF-8
"""
Created on 2017/05/29

@author: Yang Wanjun
"""
import logging

from .base_batch import BaseBatch
from eb import biz_batch
from utils import constants

logger = logging.getLogger(__name__)


class Command(BaseBatch):
    BATCH_NAME = constants.BATCH_PUSH_BIRTHDAY
    BATCH_TITLE = u"誕生日プッシュ通知"
    MAIL_TITLE = u"【営業支援システム】誕生日通知"

    def handle(self, *args, **options):
        biz_batch.batch_push_birthday(self.batch)
