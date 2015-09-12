# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('eb', '0005_auto_20150912_1856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 13, 0, 21, 47, 667728), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='client',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 13, 0, 21, 47, 667749), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='member',
            name='section',
            field=models.ForeignKey(verbose_name='\u90e8\u7f72', blank=True, to='eb.Section', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectactivity',
            name='open_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 13, 0, 21, 47, 670340), verbose_name='\u958b\u50ac\u65e5\u6642'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='salesperson',
            name='section',
            field=models.ForeignKey(verbose_name='\u90e8\u7f72', blank=True, to='eb.Section', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subcontractor',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 13, 0, 21, 47, 663730), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subcontractor',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 13, 0, 21, 47, 663756), auto_now=True),
            preserve_default=True,
        ),
    ]
