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
            model_name='salesperson',
            name='address1',
            field=models.CharField(max_length=200, null=True, verbose_name='\u4f4f\u6240\uff11', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='salesperson',
            name='address2',
            field=models.CharField(max_length=200, null=True, verbose_name='\u4f4f\u6240\uff12', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='salesperson',
            name='birthday',
            field=models.DateField(null=True, verbose_name='\u751f\u5e74\u6708\u65e5', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='salesperson',
            name='degree',
            field=models.IntegerField(blank=True, null=True, verbose_name='\u5b66\u6b74', choices=[(1, '\u5c0f\u30fb\u4e2d\u5b66\u6821'), (2, '\u9ad8\u7b49\u5b66\u6821'), (3, '\u5c02\u9580\u5b66\u6821'), (4, '\u9ad8\u7b49\u5c02\u9580\u5b66\u6821'), (5, '\u77ed\u671f\u5927\u5b66'), (6, '\u5927\u5b66\u5b66\u90e8'), (7, '\u5927\u5b66\u5927\u5b66\u9662')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='salesperson',
            name='english_spell',
            field=models.CharField(max_length=30, null=True, verbose_name='\u30ed\u30fc\u30de\u5b57', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='salesperson',
            name='graduate_date',
            field=models.DateField(null=True, verbose_name='\u5352\u696d\u5e74\u6708\u65e5', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='salesperson',
            name='japanese_spell',
            field=models.CharField(max_length=30, null=True, verbose_name='\u30d5\u30ea\u30ab\u30ca', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='salesperson',
            name='member_type',
            field=models.IntegerField(default=0, verbose_name='\u793e\u54e1\u533a\u5206', choices=[(0, '\u6b63\u793e\u54e1'), (1, '\u5951\u7d04\u793e\u54e1'), (3, '\u6d3e\u9063\u793e\u54e1'), (4, '\u500b\u4eba\u4e8b\u696d\u6240')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='salesperson',
            name='post_code',
            field=models.CharField(max_length=8, null=True, verbose_name='\u90f5\u4fbf\u756a\u53f7', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='client',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 12, 17, 1, 19, 509681), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='client',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 12, 17, 1, 19, 509703), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectactivity',
            name='open_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 12, 17, 1, 19, 512196), verbose_name='\u958b\u50ac\u65e5\u6642'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='salesperson',
            name='company',
            field=models.ForeignKey(verbose_name='\u4f1a\u793e', blank=True, to='eb.Company', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subcontractor',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 12, 17, 1, 19, 506840), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subcontractor',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 12, 17, 1, 19, 506866), auto_now=True),
            preserve_default=True,
        ),
    ]
