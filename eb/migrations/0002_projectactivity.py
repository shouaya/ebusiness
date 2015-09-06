# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectActivity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, verbose_name='\u6d3b\u52d5\u540d\u79f0')),
                ('address', models.CharField(max_length=255, verbose_name='\u6d3b\u52d5\u5834\u6240')),
                ('content', models.TextField(verbose_name='\u6d3b\u52d5\u5185\u5bb9')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('members', models.ManyToManyField(to='eb.Member', null=True, verbose_name='\u53c2\u52a0\u3057\u3066\u3044\u308b\u793e\u54e1', blank=True)),
                ('project', models.ForeignKey(verbose_name='\u6848\u4ef6', to='eb.Project')),
                ('salesperson', models.ManyToManyField(to='eb.Salesperson', null=True, verbose_name='\u53c2\u52a0\u3057\u3066\u3044\u308b\u55b6\u696d\u54e1', blank=True)),
            ],
            options={
                'ordering': ['project', 'created_date'],
                'verbose_name': '\u6848\u4ef6\u6d3b\u52d5',
                'verbose_name_plural': '\u6848\u4ef6\u6d3b\u52d5',
            },
            bases=(models.Model,),
        ),
    ]
