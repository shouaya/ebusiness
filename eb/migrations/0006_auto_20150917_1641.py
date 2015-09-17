# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('eb', '0005_auto_20150915_1900'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='certificate',
            field=models.TextField(null=True, verbose_name='\u8cc7\u683c\u306e\u8aac\u660e', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='comment',
            field=models.TextField(null=True, verbose_name='\u5099\u8003', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='country',
            field=models.CharField(max_length=20, null=True, verbose_name='\u56fd\u7c4d\u30fb\u5730\u57df', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='is_married',
            field=models.CharField(default=0, max_length=1, verbose_name='\u5a5a\u59fb\u72b6\u6cc1', choices=[(0, '\u672a\u5a5a'), (1, '\u65e2\u5a5a')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='japanese_description',
            field=models.TextField(null=True, verbose_name='\u65e5\u672c\u8a9e\u80fd\u529b\u306e\u8aac\u660e', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='nearest_station',
            field=models.CharField(max_length=15, null=True, verbose_name='\u6700\u5bc4\u99c5', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='sex',
            field=models.CharField(blank=True, max_length=1, null=True, verbose_name='\u6027\u5225', choices=[(1, '\u7537'), (2, '\u5973')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='salesperson',
            name='certificate',
            field=models.TextField(null=True, verbose_name='\u8cc7\u683c\u306e\u8aac\u660e', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='salesperson',
            name='comment',
            field=models.TextField(null=True, verbose_name='\u5099\u8003', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='salesperson',
            name='country',
            field=models.CharField(max_length=20, null=True, verbose_name='\u56fd\u7c4d\u30fb\u5730\u57df', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='salesperson',
            name='is_married',
            field=models.CharField(default=0, max_length=1, verbose_name='\u5a5a\u59fb\u72b6\u6cc1', choices=[(0, '\u672a\u5a5a'), (1, '\u65e2\u5a5a')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='salesperson',
            name='japanese_description',
            field=models.TextField(null=True, verbose_name='\u65e5\u672c\u8a9e\u80fd\u529b\u306e\u8aac\u660e', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='salesperson',
            name='nearest_station',
            field=models.CharField(max_length=15, null=True, verbose_name='\u6700\u5bc4\u99c5', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='salesperson',
            name='sex',
            field=models.CharField(blank=True, max_length=1, null=True, verbose_name='\u6027\u5225', choices=[(1, '\u7537'), (2, '\u5973')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='client',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 17, 16, 41, 22, 755000), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='client',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 17, 16, 41, 22, 755000), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectactivity',
            name='open_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 17, 16, 41, 22, 757000), verbose_name='\u958b\u50ac\u65e5\u6642'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectmember',
            name='role',
            field=models.IntegerField(default=1, verbose_name='\u5f79\u5272\u5206\u62c5', choices=[(1, 'OP\uff1a\uff75\uff8d\uff9f\uff9a\uff70\uff80\uff70'), (2, 'PG\uff1a\uff8c\uff9f\uff9b\uff78\uff9e\uff97\uff8f\uff70'), (3, 'SP\uff1a\uff7c\uff7d\uff83\uff91\uff8c\uff9f\uff9b\uff78\uff9e\uff97\uff8f\uff70'), (4, 'SE\uff1a.\uff7c\uff7d\uff83\uff91\uff74\uff9d\uff7c\uff9e\uff86\uff71'), (5, 'SL\uff1a\uff7b\uff8c\uff9e\uff98\uff70\uff80\uff9e\uff70'), (6, 'L\uff1a\uff98\uff70\uff80\uff9e\uff70'), (7, 'M\uff1a\uff8f\uff88\uff70\uff7c\uff9e\uff6c\uff70')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subcontractor',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 17, 16, 41, 22, 752000), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subcontractor',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 17, 16, 41, 22, 752000), auto_now=True),
            preserve_default=True,
        ),
    ]
