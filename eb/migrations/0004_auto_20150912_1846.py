# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('eb', '0003_auto_20150912_1704'),
    ]

    operations = [
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20, verbose_name='\u540d\u79f0')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': '\u8077\u4f4d',
                'verbose_name_plural': '\u8077\u4f4d',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PositionShip',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_part_time', models.BooleanField(default=False, verbose_name='\u517c\u4efb')),
                ('member', models.ForeignKey(verbose_name='\u793e\u54e1\u540d', to='eb.Member')),
                ('position', models.ForeignKey(verbose_name='\u8077\u4f4d', to='eb.Position')),
                ('section', models.ForeignKey(verbose_name='\u90e8\u7f72', to='eb.Section')),
            ],
            options={
                'verbose_name': '\u8077\u4f4d\u95a2\u4fc2',
                'verbose_name_plural': '\u8077\u4f4d\u95a2\u4fc2',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='member',
            name='position',
            field=models.ManyToManyField(to='eb.Position', verbose_name='\u8077\u4f4d', through='eb.PositionShip'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='project_leader',
            field=models.ForeignKey(related_name='pl_set', verbose_name='\uff30\uff2c', blank=True, to='eb.Member', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='project_manager',
            field=models.ForeignKey(related_name='pm_set', verbose_name='\uff30\uff2d', blank=True, to='eb.Member', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='client',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 12, 18, 46, 33, 741181), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='client',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 12, 18, 46, 33, 741205), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectactivity',
            name='open_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 12, 18, 46, 33, 743782), verbose_name='\u958b\u50ac\u65e5\u6642'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subcontractor',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 12, 18, 46, 33, 737249), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subcontractor',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 12, 18, 46, 33, 737279), auto_now=True),
            preserve_default=True,
        ),
    ]
