# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('eb', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='project_leader',
        ),
        migrations.AddField(
            model_name='project',
            name='project_leaders',
            field=models.ManyToManyField(related_name='pl_set', null=True, verbose_name='\uff30\uff2c', to='eb.Member', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='client',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 14, 12, 56, 56, 553000), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='client',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 14, 12, 56, 56, 553000), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='member',
            name='member_type',
            field=models.IntegerField(default=0, verbose_name='\u793e\u54e1\u533a\u5206', choices=[(0, '\u6b63\u793e\u54e1'), (1, '\u5951\u7d04\u793e\u54e1'), (3, '\u6d3e\u9063\u793e\u54e1'), (4, '\u500b\u4eba\u4e8b\u696d\u4e3b')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectactivity',
            name='open_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 14, 12, 56, 56, 556000), verbose_name='\u958b\u50ac\u65e5\u6642'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='salesperson',
            name='member_type',
            field=models.IntegerField(default=0, verbose_name='\u793e\u54e1\u533a\u5206', choices=[(0, '\u6b63\u793e\u54e1'), (1, '\u5951\u7d04\u793e\u54e1'), (3, '\u6d3e\u9063\u793e\u54e1'), (4, '\u500b\u4eba\u4e8b\u696d\u4e3b')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subcontractor',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 14, 12, 56, 56, 550000), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subcontractor',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 14, 12, 56, 56, 550000), auto_now=True),
            preserve_default=True,
        ),
    ]
