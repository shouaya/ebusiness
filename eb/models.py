# coding: UTF-8
"""
Created on 2015/08/20

@author: Yang Wanjun
"""
import datetime

import common

from django.db import models


ProjectMemberStatus = ((1, u"提案中"), (2, u"作業中"), (3, u"作業終了"))
ReleaseMonthCount = ((3, u"三ヵ月以内"), (4, u"四ヶ月以内"), (5, u"五ヶ月以内"), (6, u"半年以内"))
DisplayCount = ((50, u"50件"), (100, u"100件"), (150, u"150件"), (200, u"200件"), (300, u"300件"))
SkillTime = ((0, u"未経験者可"), (1, u"１年以上"), (2, u"２年以上"), (3, u"３年以上"), (5, u"５年以上"), (10, u"１０年以上"))


class Company(models.Model):
    name = models.CharField(blank=False, null=False, max_length=30, verbose_name=u"会社名")
    release_month_count = models.IntegerField(blank=False, null=False, default=3,
                                              choices=ReleaseMonthCount, verbose_name=u"何か月確認",
                                              help_text=u"何か月以内のリリース状況を確認したいですか？")
    display_count = models.IntegerField(blank=False, null=False, default=50,
                                        choices=DisplayCount,
                                        verbose_name=u"１頁に表示するデータ件数")

    class Meta:
        verbose_name = verbose_name_plural = u"会社"

    def __unicode__(self):
        return self.name

    def get_working_count(self):
        now = datetime.date.today()
        return ProjectMember.objects.filter(end_date__gte=now, start_date__lte=now).count()

    def get_waiting_count(self):
        return self.member_set.count() - self.get_working_count()

    def get_release_members_by_month(self, date):
        date_first_day = datetime.date(date.year, date.month, 1)
        next_month = common.add_months(date, 1)
        date_next_month = datetime.date(next_month.year, next_month.month, 1)
        return ProjectMember.objects.filter(start_date__lte=datetime.date.today(),
                                            end_date__gte=date_first_day,
                                            end_date__lt=date_next_month)

    def get_release_current_month(self):
        return self.get_release_members_by_month(datetime.date.today())

    def get_release_next_month(self):
        next_month = common.add_months(datetime.date.today(), 1)
        return self.get_release_members_by_month(next_month)

    def get_release_next_2_month(self):
        next_2_month = common.add_months(datetime.date.today(), 2)
        return self.get_release_members_by_month(next_2_month)

    def get_project_count(self):
        return Project.objects.all().count()


class Section(models.Model):
    name = models.CharField(blank=False, null=False, max_length=30, verbose_name=u"部署名")
    company = models.ForeignKey(Company, blank=False, null=False, verbose_name=u"会社")

    class Meta:
        ordering = ['name']
        verbose_name = verbose_name_plural = u"部署"

    def __unicode__(self):
        return self.name


class Salesperson(models.Model):
    employee_id = models.CharField(blank=False, null=False, unique=True, max_length=30, verbose_name=u"社員ID")
    name = models.CharField(blank=False, null=False, max_length=30, verbose_name=u"名前")
    email = models.EmailField(blank=False, null=False, verbose_name=u"メールアドレス")
    phone = models.CharField(blank=True, null=True, max_length=11, verbose_name=u"電話番号")
    section = models.ForeignKey(Section, verbose_name=u"部署")
    company = models.ForeignKey(Company, blank=False, null=False, verbose_name=u"会社")

    class Meta:
        ordering = ['name']
        verbose_name = verbose_name_plural = u"営業員"

    def __unicode__(self):
        return self.name


class Member(models.Model):
    employee_id = models.CharField(blank=False, null=False, unique=True, max_length=30, verbose_name=u"社員ID")
    name = models.CharField(blank=False, null=False, max_length=30, verbose_name=u"名前")
    email = models.EmailField(blank=False, null=False, verbose_name=u"メールアドレス")
    phone = models.CharField(blank=True, null=True, max_length=11, verbose_name=u"電話番号")
    section = models.ForeignKey(Section, verbose_name=u"部署")
    company = models.ForeignKey(Company, blank=False, null=False, verbose_name=u"会社")
    salesperson = models.ForeignKey(Salesperson, blank=True, null=True, verbose_name=u"営業員")

    class Meta:
        ordering = ['name']
        verbose_name = verbose_name_plural = u"社員"

    def __unicode__(self):
        return self.name

    def get_project_end_date(self):
        # 稼働状態を取得する（待機・稼働中）
        now = datetime.datetime.now()
        projects = self.projectmember_set.filter(end_date__gt=now, start_date__lte=now)
        if projects.count() > 0:
            return projects[0].end_date
        else:
            return None

    def get_business_status(self):
        next_2_month = common.add_months(datetime.date.today(), 2)
        if self.projectmember_set.filter(status=1).count() > 0:
            return u"営業中"
        elif not self.get_project_end_date() \
                or self.get_project_end_date() < datetime.date(next_2_month.year, next_2_month.month, 1):
            return u"未提案"
        else:
            return u"-"


class ProjectStatus(models.Model):
    name = models.CharField(blank=False, null=False, max_length=10, verbose_name=u"状態")

    class Meta:
        verbose_name = verbose_name_plural = u"案件状態"

    def __unicode__(self):
        return self.name


class Client(models.Model):
    name = models.CharField(blank=False, null=False, max_length=30, verbose_name=u"会社名")

    class Meta:
        ordering = ['name']
        verbose_name = verbose_name_plural = u"取引先"

    def __unicode__(self):
        return self.name


class ClientMember(models.Model):
    name = models.CharField(blank=False, null=False, max_length=30, verbose_name=u"名前")
    email = models.EmailField(blank=False, null=False, verbose_name=u"メールアドレス")
    phone = models.CharField(blank=True, null=True, max_length=11, verbose_name=u"電話番号")
    client = models.ForeignKey(Client, blank=False, null=False, verbose_name=u"所属会社")

    class Meta:
        ordering = ['name']
        verbose_name = verbose_name_plural = u"お客様"

    def __unicode__(self):
        return "%s - %s" % (self.client.name, self.name)


class Skill(models.Model):
    name = models.CharField(blank=False, null=False, max_length=30, verbose_name=u"名称")

    class Meta:
        ordering = ['name']
        verbose_name = verbose_name_plural = u"スキル"

    def __unicode__(self):
        return self.name


class Project(models.Model):
    project_id = models.CharField(blank=False, null=False, max_length=30, verbose_name=u"案件ID")
    name = models.CharField(blank=False, null=False, max_length=50, verbose_name=u"案件名称")
    description = models.TextField(blank=True, null=True, verbose_name=u"案件概要")
    skills = models.ManyToManyField(Skill, through='ProjectSkill', blank=True, null=True, verbose_name=u"スキル要求")
    start_date = models.DateField(blank=True, null=True, verbose_name=u"開始日")
    end_date = models.DateField(blank=True, null=True, verbose_name=u"終了日")
    address = models.CharField(blank=True, null=True, max_length=255, verbose_name=u"作業場所")
    status = models.ForeignKey(ProjectStatus, null=False, verbose_name=u"ステータス")
    client = models.ForeignKey(Client, blank=True, null=True, verbose_name=u"会社")
    boss = models.ForeignKey(ClientMember, blank=True, null=True, related_name="boss_set", verbose_name=u"案件責任者")
    middleman = models.ForeignKey(ClientMember, blank=True, null=True,
                                  related_name="middleman_set", verbose_name=u"案件連絡者")
    salesperson = models.ForeignKey(Salesperson, blank=True, null=True, verbose_name=u"営業員")
    members = models.ManyToManyField(Member, through='ProjectMember', blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name = verbose_name_plural = u"案件"

    def __unicode__(self):
        return self.name

    def get_project_members(self):
        # 案件にアサイン人数を取得する。
        return self.projectmember_set.all()


class ProjectSkill(models.Model):
    project = models.ForeignKey(Project, verbose_name=u"案件")
    skill = models.ForeignKey(Skill, verbose_name=u"スキル")
    period = models.IntegerField(blank=True, null=True, choices=SkillTime, verbose_name=u"経験年数")
    description = models.TextField(blank=True, null=True, verbose_name=u"備考")

    class Meta:
        verbose_name = verbose_name_plural = u"案件のスキル要求"

    def __unicode__(self):
        return "%s - %s" % (self.project.name, self.skill.name)


class ProjectMember(models.Model):
    project = models.ForeignKey(Project, verbose_name=u'案件名称')
    member = models.ForeignKey(Member, verbose_name=u"名前")
    start_date = models.DateField(blank=True, null=True, verbose_name=u"開始日")
    end_date = models.DateField(blank=True, null=True, verbose_name=u"終了日")
    price = models.IntegerField(null=False, default=0, verbose_name=u"単価")
    status = models.IntegerField(null=False, default=1, choices=ProjectMemberStatus, verbose_name=u"ステータス")

    class Meta:
        verbose_name = verbose_name_plural = u"案件メンバー"

    def __unicode__(self):
        return "%s - %s" % (self.project.name, self.member.name)