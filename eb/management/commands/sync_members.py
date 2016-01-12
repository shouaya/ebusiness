# coding: UTF-8
"""
Created on 2016/01/12

@author: Yang Wanjun
"""
import logging
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    args = '<target_id target_id ...>'
    help = u'社員ＤＢから社員の情報を導入する。'

    def handle(self, *args, **options):
        for target_id in args:
            logging.info('target_id: %s' % target_id)