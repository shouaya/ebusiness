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

    def get_working_members(self):
        now = datetime.date.today()
        return ProjectMember.objects.filter(end_date__gte=now, start_date__lte=now)

    def get_waiting_members(self):
        now = datetime.date.today()
        query_set = Member.objects.raw("SELECT M.*"
                                       "  FROM EB_MEMBER M LEFT JOIN EB_PROJECTMEMBER PM ON M.ID = PM.MEMBER_ID"
                                       " WHERE PM.START_DATE IS NULL OR PM.END_DATE < %s", [now])
        return list(query_set)

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

    def get_skill_list(self):
        query_set = Member.objects.raw(u"SELECT DISTINCT S.*"
                                       u"  FROM EB_MEMBER M"
                                       u"  JOIN EB_PROJECTMEMBER PM ON M.ID = PM.MEMBER_ID"
                                       u"  JOIN EB_PROJECT P ON P.ID = PM.PROJECT_ID"
                                       u"  JOIN EB_PROJECTSKILL PS ON PS.PROJECT_ID = P.ID"
                                       u"  JOIN EB_SKILL S ON S.ID = PS.SKILL_ID"
                                       u" WHERE M.EMPLOYEE_ID = %s"
                                       u"   AND PM.END_DATE <= %s", [self.employee_id, datetime.date.today()])
        return list(query_set)

    def get_recommended_projects(self):
        skill_list = self.get_skill_list()
        skill_name_list = [str(skill.name) for skill in skill_list]
        query_set = Member.objects.raw(u"SELECT DISTINCT P.*"
                                       u"  FROM EB_MEMBER M"
                                       u"  JOIN EB_PROJECTMEMBER PM ON M.ID = PM.MEMBER_ID"
                                       u"  JOIN EB_PROJECT P ON P.ID = PM.PROJECT_ID"
                                       u"  JOIN EB_PROJECTSKILL PS ON PS.PROJECT_ID = P.ID"
                                       u"  JOIN EB_SKILL S ON S.ID = PS.SKILL_ID"
                                       u" WHERE S.NAME IN %s"
                                       u"   AND P.STATUS_ID <= 3" % (str(tuple(skill_name_list)),))
        return [project.pk for project in query_set]


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
    project_id = models.CharField(blank=False, null=False, unique=True, max_length=30, verbose_name=u"案件ID")
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

    def get_recommended_members(self):
        # 如果案件为提案状态则自动推荐待机中的人员及即将待机的人
        members = []

        if self.status.id != 1:
            return members

        dict_skills = {}
        for skill in self.skills.all():
            dict_skills[skill.name] = self.get_members_by_skill_name(skill.name)

        return dict_skills

    def get_members_by_skill_name(self, name):
        members = []
        if not name:
            return members

        next_2_month = common.add_months(datetime.date.today(), 2)
        last_day_a_month_later = datetime.date(next_2_month.year, next_2_month.month, 1)
        query_set = Member.objects.raw(u"SELECT DISTINCT m.* "
                                       u"  FROM EB_MEMBER m "
                                       u"  JOIN EB_PROJECTMEMBER pm ON m.ID = pm.MEMBER_ID "
                                       u"  JOIN EB_PROJECTSKILL ps ON ps.PROJECT_ID = pm.PROJECT_ID"
                                       u"  JOIN EB_SKILL s ON s.ID = ps.SKILL_ID"
                                       u" WHERE s.NAME = %s"
                                       u"   AND pm.END_DATE < %s"
                                       u"   AND pm.STATUS <> 1"
                                       u"   AND NOT EXISTS (SELECT 1 "
                                       u"                     FROM EB_PROJECTMEMBER pm2"
                                       u"                    WHERE pm2.START_DATE >= %s"
                                       u"                      AND pm2.MEMBER_ID = m.ID"
                                       u"                      AND pm2.PROJECT_ID = %s"
                                       u"                      AND pm2.STATUS = 1)"
                                       , [name, last_day_a_month_later, datetime.date.today(), self.pk])
        members = list(query_set)
        return members


class ProjectActivity(models.Model):
    project = models.ForeignKey(Project, verbose_name=u"案件")
    name = models.CharField(max_length=30, verbose_name=u"活動名称")
    open_date = models.DateTimeField(default=datetime.datetime.now(), verbose_name=u"開催日時")
    address = models.CharField(max_length=255, verbose_name=u"活動場所")
    content = models.TextField(verbose_name=u"活動内容")
    client_members = models.ManyToManyField(ClientMember, blank=True, null=True, verbose_name=u"参加しているお客様")
    members = models.ManyToManyField(Member, blank=True, null=True, verbose_name=u"参加している社員")
    salesperson = models.ManyToManyField(Salesperson, blank=True, null=True, verbose_name=u"参加している営業員")
    created_date = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ['project', 'open_date']
        verbose_name = verbose_name_plural = u"案件活動"

    def __unicode__(self):
        return "%s - %s" % (self.project.name, self.name)


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

