# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('eb', '0002_auto_20150912_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='subcontractor',
            field=models.ForeignKey(verbose_name='\u5354\u529b\u4f1a\u793e', blank=True, to='eb.Subcontractor', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='client',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 12, 17, 4, 40, 802443), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='client',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 12, 17, 4, 40, 802469), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectactivity',
            name='open_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 12, 17, 4, 40, 804951), verbose_name='\u958b\u50ac\u65e5\u6642'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subcontractor',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 12, 17, 4, 40, 799615), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subcontractor',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 12, 17, 4, 40, 799639), auto_now=True),
            preserve_default=True,
        ),
    ]
