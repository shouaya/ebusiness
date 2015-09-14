# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('eb', '0002_auto_20150914_1256'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='project_leaders',
        ),
        migrations.RemoveField(
            model_name='project',
            name='project_manager',
        ),
        migrations.AddField(
            model_name='projectmember',
            name='role',
            field=models.IntegerField(default=1, verbose_name='\u5f79\u5272\u5206\u62c5', choices=[(1, '\uff30\uff27'), (2, '\uff33\uff25'), (3, '\uff22\uff33\uff25'), (4, '\uff30\uff2c'), (5, '\uff30\uff2d')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='client',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 14, 13, 5, 21, 117000), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='client',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 14, 13, 5, 21, 117000), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectactivity',
            name='open_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 14, 13, 5, 21, 117000), verbose_name='\u958b\u50ac\u65e5\u6642'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subcontractor',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 14, 13, 5, 21, 101000), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subcontractor',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 14, 13, 5, 21, 101000), auto_now=True),
            preserve_default=True,
        ),
    ]
