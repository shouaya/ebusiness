# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('eb', '0002_projectactivity'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projectactivity',
            options={'ordering': ['project', 'open_date'], 'verbose_name': '\u6848\u4ef6\u6d3b\u52d5', 'verbose_name_plural': '\u6848\u4ef6\u6d3b\u52d5'},
        ),
        migrations.AddField(
            model_name='projectactivity',
            name='open_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 7, 10, 48, 17, 514000), verbose_name='\u958b\u50ac\u65e5\u6642'),
            preserve_default=True,
        ),
    ]
