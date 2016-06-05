# coding: UTF-8
"""
Created on 2016/01/12

@author: Yang Wanjun
"""
import logging
import traceback

from django.core.management.base import BaseCommand

from eb.biz_logic.biz import sync_members

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = u'社員ＤＢから社員の情報を導入する。'

    def handle(self, *args, **options):
        try:
            message_list = sync_members()
            if message_list:
                for message in message_list:
                    logger.info(u"【%s】name: %s, birthday: %s, address: %s, %s" % message)
            else:
                logger.info(u"新入社員がいません。")
        except Exception as e:
            logger.error(traceback.format_exc())
