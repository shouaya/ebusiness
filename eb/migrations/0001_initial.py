# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, verbose_name='\u4f1a\u793e\u540d')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': '\u53d6\u5f15\u5148',
                'verbose_name_plural': '\u53d6\u5f15\u5148',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClientMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, verbose_name='\u540d\u524d')),
                ('email', models.EmailField(max_length=75, verbose_name='\u30e1\u30fc\u30eb\u30a2\u30c9\u30ec\u30b9')),
                ('phone', models.CharField(max_length=11, null=True, verbose_name='\u96fb\u8a71\u756a\u53f7', blank=True)),
                ('client', models.ForeignKey(verbose_name='\u6240\u5c5e\u4f1a\u793e', to='eb.Client')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': '\u304a\u5ba2\u69d8',
                'verbose_name_plural': '\u304a\u5ba2\u69d8',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, verbose_name='\u4f1a\u793e\u540d')),
                ('release_month_count', models.IntegerField(default=3, help_text='\u4f55\u304b\u6708\u4ee5\u5185\u306e\u30ea\u30ea\u30fc\u30b9\u72b6\u6cc1\u3092\u78ba\u8a8d\u3057\u305f\u3044\u3067\u3059\u304b\uff1f', verbose_name='\u4f55\u304b\u6708\u78ba\u8a8d', choices=[(3, '\u4e09\u30f5\u6708\u4ee5\u5185'), (4, '\u56db\u30f6\u6708\u4ee5\u5185'), (5, '\u4e94\u30f6\u6708\u4ee5\u5185'), (6, '\u534a\u5e74\u4ee5\u5185')])),
                ('display_count', models.IntegerField(default=50, verbose_name='\uff11\u9801\u306b\u8868\u793a\u3059\u308b\u30c7\u30fc\u30bf\u4ef6\u6570', choices=[(50, '50\u4ef6'), (100, '100\u4ef6'), (150, '150\u4ef6'), (200, '200\u4ef6'), (300, '300\u4ef6')])),
            ],
            options={
                'verbose_name': '\u4f1a\u793e',
                'verbose_name_plural': '\u4f1a\u793e',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('employee_id', models.CharField(unique=True, max_length=30, verbose_name='\u793e\u54e1ID')),
                ('name', models.CharField(max_length=30, verbose_name='\u540d\u524d')),
                ('email', models.EmailField(max_length=75, verbose_name='\u30e1\u30fc\u30eb\u30a2\u30c9\u30ec\u30b9')),
                ('phone', models.CharField(max_length=11, null=True, verbose_name='\u96fb\u8a71\u756a\u53f7', blank=True)),
                ('company', models.ForeignKey(verbose_name='\u4f1a\u793e', to='eb.Company')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': '\u793e\u54e1',
                'verbose_name_plural': '\u793e\u54e1',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project_id', models.CharField(max_length=30, verbose_name='\u6848\u4ef6ID')),
                ('name', models.CharField(max_length=50, verbose_name='\u6848\u4ef6\u540d\u79f0')),
                ('description', models.TextField(null=True, verbose_name='\u6848\u4ef6\u6982\u8981', blank=True)),
                ('start_date', models.DateField(null=True, verbose_name='\u958b\u59cb\u65e5', blank=True)),
                ('end_date', models.DateField(null=True, verbose_name='\u7d42\u4e86\u65e5', blank=True)),
                ('address', models.CharField(max_length=255, null=True, verbose_name='\u4f5c\u696d\u5834\u6240', blank=True)),
                ('boss', models.ForeignKey(related_name='boss_set', verbose_name='\u6848\u4ef6\u8cac\u4efb\u8005', blank=True, to='eb.ClientMember', null=True)),
                ('client', models.ForeignKey(verbose_name='\u4f1a\u793e', blank=True, to='eb.Client', null=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': '\u6848\u4ef6',
                'verbose_name_plural': '\u6848\u4ef6',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField(null=True, verbose_name='\u958b\u59cb\u65e5', blank=True)),
                ('end_date', models.DateField(null=True, verbose_name='\u7d42\u4e86\u65e5', blank=True)),
                ('price', models.IntegerField(default=0, verbose_name='\u5358\u4fa1')),
                ('status', models.IntegerField(default=1, verbose_name='\u30b9\u30c6\u30fc\u30bf\u30b9', choices=[(1, '\u63d0\u6848\u4e2d'), (2, '\u4f5c\u696d\u4e2d'), (3, '\u4f5c\u696d\u7d42\u4e86')])),
                ('member', models.ForeignKey(verbose_name='\u540d\u524d', to='eb.Member')),
                ('project', models.ForeignKey(verbose_name='\u6848\u4ef6\u540d\u79f0', to='eb.Project')),
            ],
            options={
                'verbose_name': '\u6848\u4ef6\u30e1\u30f3\u30d0\u30fc',
                'verbose_name_plural': '\u6848\u4ef6\u30e1\u30f3\u30d0\u30fc',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectSkill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('period', models.IntegerField(blank=True, null=True, verbose_name='\u7d4c\u9a13\u5e74\u6570', choices=[(0, '\u672a\u7d4c\u9a13\u8005\u53ef'), (1, '\uff11\u5e74\u4ee5\u4e0a'), (2, '\uff12\u5e74\u4ee5\u4e0a'), (3, '\uff13\u5e74\u4ee5\u4e0a'), (5, '\uff15\u5e74\u4ee5\u4e0a'), (10, '\uff11\uff10\u5e74\u4ee5\u4e0a')])),
                ('description', models.TextField(null=True, verbose_name='\u5099\u8003', blank=True)),
                ('project', models.ForeignKey(verbose_name='\u6848\u4ef6', to='eb.Project')),
            ],
            options={
                'verbose_name': '\u6848\u4ef6\u306e\u30b9\u30ad\u30eb\u8981\u6c42',
                'verbose_name_plural': '\u6848\u4ef6\u306e\u30b9\u30ad\u30eb\u8981\u6c42',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=10, verbose_name='\u72b6\u614b')),
            ],
            options={
                'verbose_name': '\u6848\u4ef6\u72b6\u614b',
                'verbose_name_plural': '\u6848\u4ef6\u72b6\u614b',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Salesperson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('employee_id', models.CharField(unique=True, max_length=30, verbose_name='\u793e\u54e1ID')),
                ('name', models.CharField(max_length=30, verbose_name='\u540d\u524d')),
                ('email', models.EmailField(max_length=75, verbose_name='\u30e1\u30fc\u30eb\u30a2\u30c9\u30ec\u30b9')),
                ('phone', models.CharField(max_length=11, null=True, verbose_name='\u96fb\u8a71\u756a\u53f7', blank=True)),
                ('company', models.ForeignKey(verbose_name='\u4f1a\u793e', to='eb.Company')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': '\u55b6\u696d\u54e1',
                'verbose_name_plural': '\u55b6\u696d\u54e1',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, verbose_name='\u90e8\u7f72\u540d')),
                ('company', models.ForeignKey(verbose_name='\u4f1a\u793e', to='eb.Company')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': '\u90e8\u7f72',
                'verbose_name_plural': '\u90e8\u7f72',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, verbose_name='\u540d\u79f0')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': '\u30b9\u30ad\u30eb',
                'verbose_name_plural': '\u30b9\u30ad\u30eb',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='salesperson',
            name='section',
            field=models.ForeignKey(verbose_name='\u90e8\u7f72', to='eb.Section'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectskill',
            name='skill',
            field=models.ForeignKey(verbose_name='\u30b9\u30ad\u30eb', to='eb.Skill'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='members',
            field=models.ManyToManyField(to='eb.Member', null=True, through='eb.ProjectMember', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='middleman',
            field=models.ForeignKey(related_name='middleman_set', verbose_name='\u6848\u4ef6\u9023\u7d61\u8005', blank=True, to='eb.ClientMember', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='salesperson',
            field=models.ForeignKey(verbose_name='\u55b6\u696d\u54e1', blank=True, to='eb.Salesperson', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='skills',
            field=models.ManyToManyField(to='eb.Skill', null=True, verbose_name='\u30b9\u30ad\u30eb\u8981\u6c42', through='eb.ProjectSkill', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.ForeignKey(verbose_name='\u30b9\u30c6\u30fc\u30bf\u30b9', to='eb.ProjectStatus'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='salesperson',
            field=models.ForeignKey(verbose_name='\u55b6\u696d\u54e1', blank=True, to='eb.Salesperson', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='section',
            field=models.ForeignKey(verbose_name='\u90e8\u7f72', to='eb.Section'),
            preserve_default=True,
        ),
    ]
