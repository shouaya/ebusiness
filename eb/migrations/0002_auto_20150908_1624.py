# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('eb', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='address1',
            field=models.CharField(max_length=200, null=True, verbose_name='\u4f4f\u6240\uff11', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='client',
            name='address2',
            field=models.CharField(max_length=200, null=True, verbose_name='\u4f4f\u6240\uff12', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='client',
            name='capital',
            field=models.BigIntegerField(null=True, verbose_name='\u8cc7\u672c\u91d1', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='client',
            name='comment',
            field=models.TextField(null=True, verbose_name='\u5099\u8003', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='client',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 8, 16, 24, 14, 664000), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='client',
            name='employee_count',
            field=models.IntegerField(null=True, verbose_name='\u5f93\u696d\u54e1\u6570', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='client',
            name='fax',
            field=models.CharField(max_length=15, null=True, verbose_name='\u30d5\u30a1\u30c3\u30af\u30b9', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='client',
            name='found_date',
            field=models.DateField(null=True, verbose_name='\u8a2d\u7acb\u5e74\u6708\u65e5', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='client',
            name='japanese_spell',
            field=models.CharField(max_length=30, null=True, verbose_name='\u30d5\u30ea\u30ab\u30ca', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='client',
            name='payment_day',
            field=models.CharField(max_length=2, null=True, verbose_name='\u652f\u6255\u65e5', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='client',
            name='payment_type',
            field=models.CharField(max_length=2, null=True, verbose_name='\u652f\u6255\u65b9\u6cd5', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='client',
            name='post_code',
            field=models.CharField(max_length=8, null=True, verbose_name='\u90f5\u4fbf\u756a\u53f7', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='client',
            name='president',
            field=models.CharField(max_length=30, null=True, verbose_name='\u4ee3\u8868\u8005\u540d', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='client',
            name='sale_amount',
            field=models.BigIntegerField(null=True, verbose_name='\u58f2\u4e0a\u9ad8', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='client',
            name='tel',
            field=models.CharField(max_length=15, null=True, verbose_name='\u96fb\u8a71\u756a\u53f7', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='client',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 8, 16, 24, 14, 664000), auto_now=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='company',
            name='address',
            field=models.CharField(max_length=250, null=True, verbose_name='\u4f4f\u6240', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='company',
            name='post_code',
            field=models.CharField(max_length=8, null=True, verbose_name='\u90f5\u4fbf\u756a\u53f7', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='company',
            name='tel',
            field=models.CharField(max_length=15, null=True, verbose_name='\u96fb\u8a71\u756a\u53f7', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectactivity',
            name='open_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 8, 16, 24, 14, 666000), verbose_name='\u958b\u50ac\u65e5\u6642'),
            preserve_default=True,
        ),
    ]
