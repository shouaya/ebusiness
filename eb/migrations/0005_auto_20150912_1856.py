# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('eb', '0004_auto_20150912_1846'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='position',
            options={'ordering': ['pk'], 'verbose_name': '\u8077\u4f4d', 'verbose_name_plural': '\u8077\u4f4d'},
        ),
        migrations.AddField(
            model_name='section',
            name='description',
            field=models.CharField(max_length=200, null=True, verbose_name='\u6982\u8981', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='client',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 12, 18, 56, 46, 65462), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='client',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 12, 18, 56, 46, 65483), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectactivity',
            name='open_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 12, 18, 56, 46, 68061), verbose_name='\u958b\u50ac\u65e5\u6642'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subcontractor',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 12, 18, 56, 46, 61496), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subcontractor',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 12, 18, 56, 46, 61524), auto_now=True),
            preserve_default=True,
        ),
    ]
