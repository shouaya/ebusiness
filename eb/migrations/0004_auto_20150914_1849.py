# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('eb', '0003_auto_20150914_1305'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='positionship',
            options={'verbose_name': '\u8077\u4f4d', 'verbose_name_plural': '\u8077\u4f4d'},
        ),
        migrations.RemoveField(
            model_name='member',
            name='position',
        ),
        migrations.AlterField(
            model_name='client',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 14, 18, 49, 57, 71000), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='client',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 14, 18, 49, 57, 71000), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='positionship',
            name='position',
            field=models.IntegerField(blank=True, null=True, verbose_name='\u8077\u4f4d', choices=[(1, '\u4ee3\u8868\u53d6\u7de0\u5f79'), (2, '\u793e\u9577'), (3, '\u53d6\u7de0\u5f79'), (4, '\u90e8\u9577'), (5, '\u62c5\u5f53\u90e8\u9577'), (6, '\u8ab2\u9577'), (7, '\u62c5\u5f53\u8ab2\u9577')]),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='Position',
        ),
        migrations.AlterField(
            model_name='project',
            name='client',
            field=models.ForeignKey(verbose_name='\u95a2\u9023\u4f1a\u793e', blank=True, to='eb.Client', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectactivity',
            name='open_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 14, 18, 49, 57, 71000), verbose_name='\u958b\u50ac\u65e5\u6642'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subcontractor',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 14, 18, 49, 57, 71000), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subcontractor',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 14, 18, 49, 57, 71000), auto_now=True),
            preserve_default=True,
        ),
    ]
