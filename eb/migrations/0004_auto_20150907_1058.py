# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('eb', '0003_auto_20150907_1048'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectactivity',
            name='client_members',
            field=models.ManyToManyField(to='eb.ClientMember', null=True, verbose_name='\u53c2\u52a0\u3057\u3066\u3044\u308b\u304a\u5ba2\u69d8', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectactivity',
            name='open_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 7, 10, 58, 16, 700000), verbose_name='\u958b\u50ac\u65e5\u6642'),
            preserve_default=True,
        ),
    ]
