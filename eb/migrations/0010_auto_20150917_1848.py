# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('eb', '0009_auto_20150917_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 17, 18, 48, 14, 656000), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='client',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 17, 18, 48, 14, 656000), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='member',
            name='birthday',
            field=models.DateField(verbose_name='\u751f\u5e74\u6708\u65e5'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectactivity',
            name='open_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 17, 18, 48, 14, 658000), verbose_name='\u958b\u50ac\u65e5\u6642'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='salesperson',
            name='birthday',
            field=models.DateField(verbose_name='\u751f\u5e74\u6708\u65e5'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subcontractor',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 17, 18, 48, 14, 653000), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subcontractor',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 17, 18, 48, 14, 653000), auto_now=True),
            preserve_default=True,
        ),
    ]
