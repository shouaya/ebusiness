# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('eb', '0004_auto_20150914_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 15, 19, 0, 29, 968000), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='client',
            name='post_code',
            field=models.CharField(max_length=7, null=True, verbose_name='\u90f5\u4fbf\u756a\u53f7', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='client',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 15, 19, 0, 29, 968000), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='company',
            name='post_code',
            field=models.CharField(max_length=7, null=True, verbose_name='\u90f5\u4fbf\u756a\u53f7', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='member',
            name='post_code',
            field=models.CharField(max_length=7, null=True, verbose_name='\u90f5\u4fbf\u756a\u53f7', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectactivity',
            name='open_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 15, 19, 0, 29, 984000), verbose_name='\u958b\u50ac\u65e5\u6642'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='salesperson',
            name='post_code',
            field=models.CharField(max_length=7, null=True, verbose_name='\u90f5\u4fbf\u756a\u53f7', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subcontractor',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 15, 19, 0, 29, 968000), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subcontractor',
            name='post_code',
            field=models.CharField(max_length=7, null=True, verbose_name='\u90f5\u4fbf\u756a\u53f7', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subcontractor',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 15, 19, 0, 29, 968000), auto_now=True),
            preserve_default=True,
        ),
    ]
