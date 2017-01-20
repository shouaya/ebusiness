# coding: UTF-8
"""
Created on 2017/01/20

@author: Yang Wanjun
"""
import logging
import os
import traceback
from eb import biz_batch

from django.conf import settings
from django.core.management.base import BaseCommand
from django.template import Context, Template


class BaseBatch(BaseCommand):

    def handle(self, *args, **options):
        pass

    def get_batch_manager(self):
        name = self.get_batch_name()
        batch = biz_batch.get_batch_manager(name)
        if not batch.id:
            batch.title = self.__class__.BATCH_TITLE
            batch.mail_title = self.__class__.MAIL_TITLE
            batch.save()
        return batch

    def get_batch_name(self):
        return self.__class__.__module__
