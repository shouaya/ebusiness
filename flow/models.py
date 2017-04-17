# coding: UTF-8
"""
Created on 2017/04/17

@author: Yang Wanjun
"""
from __future__ import unicode_literals
import datetime

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from utils import constants

# Create your models here.


class PublicManager(models.Manager):

    # use_for_related_fields = True

    def __init__(self):
        super(PublicManager, self).__init__()

    def get_queryset(self):
        return super(PublicManager, self).get_queryset().filter(is_deleted=False)


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=u"作成日時")
    updated_date = models.DateTimeField(auto_now=True, verbose_name=u"更新日時")
    is_deleted = models.BooleanField(default=False, editable=False, verbose_name=u"削除フラグ")
    deleted_date = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=u"削除年月日")

    objects = PublicManager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_date = datetime.datetime.now()
        self.save()


class Workflow(BaseModel):
    name = models.CharField(max_length=50, verbose_name=u"名称")
    operation = models.CharField(max_length=2, choices=constants.CHOICE_WORKFLOW_OPERATION, verbose_name=u"操作")
    content_type = models.ForeignKey(ContentType)
    filed_name = models.CharField(max_length=50, verbose_name=u"フィールド")

    class Meta:
        verbose_name = verbose_name_plural = u"フロー定義"

    def __unicode__(self):
        return self.name


class Node(BaseModel):
    name = models.CharField(max_length=50, verbose_name=u"名称")
    workflow = models.ForeignKey(Workflow, verbose_name=u"ワークフロー")
    parent = models.ForeignKey('self', related_name='children', blank=True, null=True, verbose_name=u"親")
    resolve_user = models.ForeignKey(User, related_name='node_resolver_set', verbose_name=u"担当者")

    def __unicode__(self):
        return self.name


class Task(BaseModel):
    created_user = models.ForeignKey(User, verbose_name=u"作成者")
    workflow = models.ForeignKey(Workflow, verbose_name=u"ワークフロー")
