# coding: UTF-8
"""
Created on 2017/01/20

@author: Yang Wanjun
"""
import logging
import traceback

from eb import biz_batch, biz
from utils import constants

from django.core.management.base import BaseCommand


class BaseBatch(BaseCommand):

    BATCH_NAME = ''
    BATCH_TITLE = ''
    MAIL_TITLE = ''

    def __init__(self, *args, **kwargs):
        super(BaseBatch, self).__init__(*args, **kwargs)
        name = self.__class__.BATCH_NAME
        self.batch = biz_batch.get_batch_manager(name)
        if not self.batch.id:
            self.batch.title = self.__class__.BATCH_TITLE
            self.batch.mail_title = self.__class__.MAIL_TITLE
            self.batch.save()

    def handle(self, *args, **options):
        pass

    def execute(self, *args, **options):
        logger = logging.getLogger(self.__module__)
        try:
            if self.batch.is_active:
                super(BaseBatch, self).execute(*args, **options)
            else:
                logger.error(u"%s が有効になっていません。" % (self.__class__.BATCH_TITLE,))
        except Exception as e:
            print e.message
            logger.error(traceback.format_exc())
