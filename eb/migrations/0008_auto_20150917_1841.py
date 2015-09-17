# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('eb', '0007_auto_20150917_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 17, 18, 40, 38, 606000), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='client',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 17, 18, 40, 38, 606000), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='member',
            name='first_name_en',
            field=models.CharField(max_length=30, verbose_name='\u59d3(\u30ed\u30fc\u30de\u5b57)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='member',
            name='is_married',
            field=models.CharField(blank=True, max_length=1, null=True, verbose_name='\u5a5a\u59fb\u72b6\u6cc1', choices=[(b'', '------'), (b'0', '\u672a\u5a5a'), (b'1', '\u65e2\u5a5a')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='member',
            name='last_name_en',
            field=models.CharField(max_length=30, verbose_name='\u540d(\u30ed\u30fc\u30de\u5b57)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectactivity',
            name='open_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 17, 18, 40, 38, 608000), verbose_name='\u958b\u50ac\u65e5\u6642'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='salesperson',
            name='first_name_en',
            field=models.CharField(max_length=30, verbose_name='\u59d3(\u30ed\u30fc\u30de\u5b57)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='salesperson',
            name='is_married',
            field=models.CharField(blank=True, max_length=1, null=True, verbose_name='\u5a5a\u59fb\u72b6\u6cc1', choices=[(b'', '------'), (b'0', '\u672a\u5a5a'), (b'1', '\u65e2\u5a5a')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='salesperson',
            name='last_name_en',
            field=models.CharField(default=1, max_length=30, verbose_name='\u540d(\u30ed\u30fc\u30de\u5b57)'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='subcontractor',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 17, 18, 40, 38, 603000), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subcontractor',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 17, 18, 40, 38, 603000), auto_now=True),
            preserve_default=True,
        ),
    ]
