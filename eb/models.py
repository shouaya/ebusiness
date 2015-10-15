# coding: UTF-8
"""
Created on 2015/08/20

@author: Yang Wanjun
"""
import datetime

from django.db import models
from django.contrib.auth.models import User

from utils import common, constants


class AbstractCompany(models.Model):
    name = models.CharField(blank=False, null=False, max_length=30, verbose_name=u"会社名")
    japanese_spell = models.CharField(blank=True, null=True, max_length=30, verbose_name=u"フリカナ")
    found_date = models.DateField(blank=True, null=True, verbose_name=u"設立年月日")
    capital = models.BigIntegerField(blank=True, null=True, verbose_name=u"資本金")
    post_code = models.CharField(blank=True, null=True, max_length=7, verbose_name=u"郵便番号")
    address1 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"住所１")
    address2 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"住所２")
    tel = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"電話番号")
    fax = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"ファックス")

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name


class AbstractMember(models.Model):
    employee_id = models.CharField(blank=False, null=False, unique=True, max_length=30, verbose_name=u"社員ID")
    first_name = models.CharField(blank=False, null=False, max_length=30, verbose_name=u"姓")
    last_name = models.CharField(blank=False, null=False, max_length=30, verbose_name=u"名")
    first_name_ja = models.CharField(blank=True, null=True, max_length=30, verbose_name=u"姓(フリカナ)")
    last_name_ja = models.CharField(blank=True, null=True, max_length=30, verbose_name=u"名(フリカナ)")
    first_name_en = models.CharField(blank=True, null=True, max_length=30, verbose_name=u"姓(ローマ字)",
                                     help_text=u"先頭文字は大文字にしてください（例：Zhang）")
    last_name_en = models.CharField(blank=True, null=True, max_length=30, verbose_name=u"名(ローマ字)",
                                    help_text=u"漢字ごとに先頭文字は大文字にしてください（例：XiaoWang）")
    sex = models.CharField(blank=True, null=True, max_length=1, choices=constants.CHOICE_SEX, verbose_name=u"性別")
    country = models.CharField(blank=True, null=True, max_length=20, verbose_name=u"国籍・地域")
    birthday = models.DateField(blank=True, null=True, verbose_name=u"生年月日")
    graduate_date = models.DateField(blank=True, null=True, verbose_name=u"卒業年月日")
    degree = models.IntegerField(blank=True, null=True, choices=constants.CHOICE_DEGREE_TYPE, verbose_name=u"学歴")
    email = models.EmailField(blank=True, null=True, verbose_name=u"メールアドレス")
    post_code = models.CharField(blank=True, null=True, max_length=7, verbose_name=u"郵便番号")
    address1 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"住所１")
    address2 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"住所２")
    nearest_station = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"最寄駅")
    phone = models.CharField(blank=True, null=True, max_length=11, verbose_name=u"電話番号")
    is_married = models.CharField(blank=True, null=True, max_length=1,
                                  choices=constants.CHOICE_MARRIED, verbose_name=u"婚姻状況")
    member_type = models.IntegerField(default=0, choices=constants.CHOICE_MEMBER_TYPE, verbose_name=u"社員区分")
    section = models.ForeignKey('Section', blank=True, null=True, verbose_name=u"部署")
    company = models.ForeignKey('Company', blank=True, null=True, verbose_name=u"会社")
    japanese_description = models.TextField(blank=True, null=True, verbose_name=u"日本語能力の説明")
    certificate = models.TextField(blank=True, null=True, verbose_name=u"資格の説明")
    comment = models.TextField(blank=True, null=True, verbose_name=u"備考")
    user = models.OneToOneField(User, blank=True, null=True)

    class Meta:
        abstract = True


class Company(AbstractCompany):

    class Meta:
        verbose_name = verbose_name_plural = u"会社"

    def get_all_members(self):
        return Member.objects.filter(member_type__lte=4)

    def get_working_members(self):
        now = datetime.date.today()
        return ProjectMember.objects.filter(end_date__gte=now, start_date__lte=now)

    def get_waiting_members(self):
        now = datetime.date.today()
        Member.objects.filter()
        query_set = Member.objects.raw("SELECT DISTINCT M.*"
                                       "  FROM eb_member M"
                                       " WHERE NOT EXISTS (SELECT 1 "
                                       "                     FROM eb_projectmember PM"
                                       "                    WHERE PM.MEMBER_ID = M.ID"
                                       "                      AND PM.START_DATE <= %s"
                                       "                      AND PM.END_DATE >= %s)"
                                       "   and M.member_type <= 4", [now, now])
        return list(query_set)

    def get_release_members_by_month(self, date):
        date_first_day = datetime.date(date.year, date.month, 1)
        next_month = common.add_months(date, 1)
        date_next_month = datetime.date(next_month.year, next_month.month, 1)
        return ProjectMember.objects.filter(end_date__gte=date_first_day,
                                            end_date__lt=date_next_month)

    def get_release_current_month(self):
        return self.get_release_members_by_month(datetime.date.today())

    def get_release_next_month(self):
        next_month = common.add_months(datetime.date.today(), 1)
        return self.get_release_members_by_month(next_month)

    def get_release_next_2_month(self):
        next_2_month = common.add_months(datetime.date.today(), 2)
        return self.get_release_members_by_month(next_2_month)

    def get_projects(self, status=0):
        """ステータスによって、該当する全ての案件を取得する。

        Arguments：
          status: 案件の状態

        Returns：
          案件のリスト

        Raises：
          なし
        """
        if status == 0:
            return Project.objects.all()
        else:
            return Project.objects.filter(status=status)

    def get_proposal_projects(self):
        """提案中の案件を取得する。

        Arguments：
          なし

        Returns：
          案件のリスト

        Raises：
          なし
        """
        return self.get_projects(1)

    def get_examination_projects(self):
        """予算審査中の案件を取得する。

        Arguments：
          なし

        Returns：
          案件のリスト

        Raises：
          なし
        """
        return self.get_projects(2)

    def get_confirmed_projects(self):
        """予算確定の案件を取得する。

        Arguments：
          なし

        Returns：
          案件のリスト

        Raises：
          なし
        """
        return self.get_projects(3)

    def get_working_projects(self):
        """実施中の案件を取得する。

        Arguments：
          なし

        Returns：
          案件のリスト

        Raises：
          なし
        """
        return self.get_projects(4)

    def get_finished_projects(self):
        """終了の案件を取得する。

        Arguments：
          なし

        Returns：
          案件のリスト

        Raises：
          なし
        """
        return self.get_projects(5)

    def get_master(self):
        # 代表取締役を取得する。
        members = Member.objects.filter(member_type=7)
        if members.count() == 1:
            return members[0]
        else:
            return None


class Subcontractor(AbstractCompany):
    president = models.CharField(blank=True, null=True, max_length=30, verbose_name=u"代表者名")
    employee_count = models.IntegerField(blank=True, null=True, verbose_name=u"従業員数")
    sale_amount = models.BigIntegerField(blank=True, null=True, verbose_name=u"売上高")
    payment_type = models.CharField(blank=True, null=True, max_length=2, verbose_name=u"支払方法")
    payment_day = models.CharField(blank=True, null=True, max_length=2, choices=constants.CHOICE_PAYMENT_DAY,
                                   verbose_name=u"支払日")
    comment = models.TextField(blank=True, null=True, verbose_name=u"備考")
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    updated_date = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['name']
        verbose_name = verbose_name_plural = u"協力会社"


class Section(models.Model):
    name = models.CharField(blank=False, null=False, max_length=30, verbose_name=u"部署名")
    description = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"概要")
    company = models.ForeignKey(Company, blank=False, null=False, verbose_name=u"会社")

    class Meta:
        ordering = ['name']
        verbose_name = verbose_name_plural = u"部署"

    def __unicode__(self):
        if not self.description:
            return self.name
        else:
            desc = self.description[:7] + "..." if len(self.description) > 10 else self.description
            return u"%s(%s)" % (self.name, desc)


class Salesperson(AbstractMember):

    class Meta:
        ordering = ['first_name', 'last_name']
        verbose_name = verbose_name_plural = u"営業員"

    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)


class Member(AbstractMember):
    salesperson = models.ForeignKey(Salesperson, blank=True, null=True, verbose_name=u"営業員")
    subcontractor = models.ForeignKey(Subcontractor, blank=True, null=True, verbose_name=u"協力会社")

    class Meta:
        ordering = ['first_name', 'last_name']
        verbose_name = verbose_name_plural = u"社員"

    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)

    def get_age(self):
        birthday = self.birthday
        today = datetime.date.today()
        years = today.year - birthday.year
        if today.month < birthday.month:
            years -= 1
        elif today.month == birthday.month:
            if today.day <= birthday.day:
                years -= 1
        return years

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
                                       u"  FROM eb_member M"
                                       u"  JOIN eb_projectmember PM ON M.ID = PM.MEMBER_ID"
                                       u"  JOIN eb_project P ON P.ID = PM.PROJECT_ID"
                                       u"  JOIN eb_projectskill PS ON PS.PROJECT_ID = P.ID"
                                       u"  JOIN eb_skill S ON S.ID = PS.SKILL_ID"
                                       u" WHERE M.EMPLOYEE_ID = %s"
                                       u"   AND PM.END_DATE <= %s", [self.employee_id, datetime.date.today()])
        return list(query_set)

    def get_recommended_projects(self):
        skill_list = self.get_skill_list()
        skill_id_list = [str(skill.pk) for skill in skill_list]
        if not skill_id_list:
            return []
        query_set = Member.objects.raw(u"SELECT DISTINCT P.*"
                                       u"  FROM eb_member M"
                                       u"  JOIN eb_projectmember PM ON M.ID = PM.MEMBER_ID"
                                       u"  JOIN eb_project P ON P.ID = PM.PROJECT_ID"
                                       u"  JOIN eb_projectskill PS ON PS.PROJECT_ID = P.ID"
                                       u"  JOIN eb_skill S ON S.ID = PS.SKILL_ID"
                                       u" WHERE S.ID IN (%s)"
                                       u"   AND P.STATUS <= 3" % (",".join(skill_id_list),))
        return [project.pk for project in query_set]

    def get_project_role_list(self):
        """かつてのプロジェクト中の役割担当を取得する。。

        Arguments：
          なし

        Returns：
          役割担当のリスト

        Raises：
          なし
        """
        project_member_list = self.projectmember_set.all()
        role_list = []
        for project_member in project_member_list:
            role = project_member.get_role_display().split(u"：")[0]
            if role not in role_list:
                role_list.append(role)
        return role_list

    def get_position_ship(self, is_min=False):
        """該当メンバーの職位を取得する。

        Arguments：
          なし

        Returns：
          Position のインスタンス

        Raises：
          なし
        """
        if is_min:
            positions = self.positionship_set.filter(is_part_time=False).order_by('-position')
        else:
            positions = self.positionship_set.filter(is_part_time=False)
        if positions.count() > 0:
            return positions[0]
        else:
            return None


class PositionShip(models.Model):
    member = models.ForeignKey(Member, verbose_name=u"社員名")
    position = models.IntegerField(blank=True, null=True, choices=constants.CHOICE_POSITION, verbose_name=u"職位")
    section = models.ForeignKey(Section, verbose_name=u"部署")
    is_part_time = models.BooleanField(default=False, verbose_name=u"兼任")

    class Meta:
        ordering = ['position']
        verbose_name = verbose_name_plural = u"職位"

    def __unicode__(self):
        return "%s - %s %s" % (self.get_position_display(), self.member.first_name, self.member.last_name)


class Client(AbstractCompany):
    president = models.CharField(blank=True, null=True, max_length=30, verbose_name=u"代表者名")
    employee_count = models.IntegerField(blank=True, null=True, verbose_name=u"従業員数")
    sale_amount = models.BigIntegerField(blank=True, null=True, verbose_name=u"売上高")
    undertaker = models.CharField(blank=True, null=True, max_length=30, verbose_name=u"担当者")
    undertaker_mail = models.EmailField(blank=True, null=True, verbose_name=u"担当者メール")
    payment_type = models.CharField(blank=True, null=True, max_length=2, verbose_name=u"支払方法")
    payment_day = models.CharField(blank=True, null=True, max_length=2,
                                   choices=constants.CHOICE_PAYMENT_DAY, verbose_name=u"支払日")
    remark = models.TextField(blank=True, null=True, verbose_name=u"評価")
    comment = models.TextField(blank=True, null=True, verbose_name=u"備考")
    salesperson = models.ForeignKey(Salesperson, blank=True, null=True, verbose_name=u"営業担当")
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    updated_date = models.DateTimeField(auto_now=True, editable=False)
    saletest_customer_id = models.IntegerField(blank=True, null=True, editable=False,
                                               help_text=u"売上ＤＢからデータを導入するために使う、売上ＤＢの顧客ＩＤ")
    request_file = models.FileField(blank=True, null=True, upload_to="./request", verbose_name=u"請求書テンプレート")

    class Meta:
        ordering = ['name']
        verbose_name = verbose_name_plural = u"取引先"


class ClientMember(models.Model):
    name = models.CharField(max_length=30, verbose_name=u"名前")
    email = models.EmailField(blank=True, null=True, verbose_name=u"メールアドレス")
    phone = models.CharField(blank=True, null=True, max_length=11, verbose_name=u"電話番号")
    client = models.ForeignKey(Client, verbose_name=u"所属会社")

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


class OS(models.Model):
    name = models.CharField(max_length=15, verbose_name=u"名称")

    class Meta:
        ordering = ['name']
        verbose_name = verbose_name_plural = u"機種／OS"

    def __unicode__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(blank=False, null=False, max_length=50, verbose_name=u"案件名称")
    description = models.TextField(blank=True, null=True, verbose_name=u"案件概要")
    skills = models.ManyToManyField(Skill, through='ProjectSkill', blank=True, null=True, verbose_name=u"スキル要求")
    os = models.ManyToManyField(OS, blank=True, null=True, verbose_name=u"機種／OS")
    start_date = models.DateField(blank=True, null=True, verbose_name=u"開始日")
    end_date = models.DateField(blank=True, null=True, verbose_name=u"終了日")
    address = models.CharField(blank=True, null=True, max_length=255, verbose_name=u"作業場所")
    status = models.IntegerField(choices=constants.CHOICE_PROJECT_STATUS, verbose_name=u"ステータス")
    client = models.ForeignKey(Client, null=True, verbose_name=u"関連会社")
    boss = models.ForeignKey(ClientMember, blank=True, null=True, related_name="boss_set", verbose_name=u"案件責任者")
    middleman = models.ForeignKey(ClientMember, blank=True, null=True,
                                  related_name="middleman_set", verbose_name=u"案件連絡者")
    salesperson = models.ForeignKey(Salesperson, blank=True, null=True, verbose_name=u"営業員")
    members = models.ManyToManyField(Member, through='ProjectMember', blank=True, null=True)
    saletest_contract_id = models.IntegerField(blank=True, null=True, editable=False,
                                               help_text=u"売上ＤＢからデータを導入するために使う、売上ＤＢの契約ＩＤ")

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

        if self.status != 1:
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
                                       u"  FROM eb_member m "
                                       u"  JOIN eb_projectmember pm ON m.ID = pm.MEMBER_ID "
                                       u"  JOIN eb_projectskill ps ON ps.PROJECT_ID = pm.PROJECT_ID"
                                       u"  JOIN eb_skill s ON s.ID = ps.SKILL_ID"
                                       u" WHERE s.NAME = %s"
                                       u"   AND pm.END_DATE < %s"
                                       u"   AND pm.STATUS <> 1"
                                       u"   AND NOT EXISTS (SELECT 1 "
                                       u"                     FROM eb_projectmember pm2"
                                       u"                    WHERE pm2.START_DATE >= %s"
                                       u"                      AND pm2.MEMBER_ID = m.ID"
                                       u"                      AND pm2.PROJECT_ID = %s"
                                       u"                      AND pm2.STATUS = 1)"
                                       , [name, last_day_a_month_later, datetime.date.today(), self.pk])
        members = list(query_set)
        return members

    def get_project_members_current_month(self):
        now = datetime.date.today()
        first_day = datetime.date(now.year, now.month, 1)
        last_day = common.get_last_day_by_month(now)
        return self.projectmember_set.filter(start_date__lte=last_day, end_date__gte=first_day)

    def get_first_project_member(self):
        """営業企画書を出すとき、1つ目に表示するメンバー。

        Arguments：
          なし

        Returns：
          Member のインスタンス

        Raises：
          なし
        """
        now = datetime.date.today()
        first_day = datetime.date(now.year, now.month, 1)
        last_day = common.get_last_day_by_month(now)
        project_members = self.projectmember_set.filter(start_date__lte=last_day, end_date__gte=first_day, role=7)
        if project_members.count() == 0:
            project_members = self.projectmember_set.filter(start_date__lte=last_day, end_date__gte=first_day, role=6)
        if project_members.count() == 0:
            project_members = self.projectmember_set.filter(start_date__lte=last_day, end_date__gte=first_day)
        if project_members.count() > 0:
            return project_members[0]
        else:
            return None

    def get_working_project_members(self):
        now = datetime.date.today()
        first_day = datetime.date(now.year, now.month, 1)
        last_day = common.get_last_day_by_month(now)
        return self.projectmember_set.filter(start_date__lte=last_day, end_date__gte=first_day)


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
    period = models.IntegerField(blank=True, null=True, choices=constants.CHOICE_SKILL_TIME, verbose_name=u"経験年数")
    description = models.TextField(blank=True, null=True, verbose_name=u"備考")

    class Meta:
        verbose_name = verbose_name_plural = u"案件のスキル要求"

    def __unicode__(self):
        return "%s - %s" % (self.project.name, self.skill.name)


class ProjectStage(models.Model):
    name = models.CharField(max_length=15, verbose_name=u"作業工程名称")

    class Meta:
        verbose_name = verbose_name_plural = u"作業工程"

    def __unicode__(self):
        return self.name


class ProjectMember(models.Model):
    project = models.ForeignKey(Project, verbose_name=u'案件名称')
    member = models.ForeignKey(Member, verbose_name=u"名前")
    start_date = models.DateField(blank=True, null=True, verbose_name=u"開始日")
    end_date = models.DateField(blank=True, null=True, verbose_name=u"終了日")
    price = models.IntegerField(null=False, default=0, verbose_name=u"単価")
    status = models.IntegerField(null=False, default=1,
                                 choices=constants.CHOICE_PROJECT_MEMBER_STATUS, verbose_name=u"ステータス")
    role = models.IntegerField(default=1, choices=constants.CHOICE_PROJECT_ROLE, verbose_name=u"作業区分")
    stages = models.ManyToManyField(ProjectStage, blank=True, null=True, verbose_name=u"作業工程")

    class Meta:
        verbose_name = verbose_name_plural = u"案件メンバー"

    def __unicode__(self):
        return "%s - %s %s" % (self.project.name, self.member.first_name, self.member.last_name)


class MemberAttendance(models.Model):
    project_member = models.ForeignKey(ProjectMember, verbose_name=u"要員")
    year = models.CharField(max_length=4, default=str(datetime.date.today().year), verbose_name=u"対象年")
    month = models.CharField(max_length=2, choices=constants.CHOICE_ATTENDANCE_MONTH, verbose_name=u"対象月")
    total_hours = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=u"合計時間")
    extra_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name=u"残業時間")

    class Meta:
        ordering = ['project_member', 'year', 'month']
        verbose_name = verbose_name_plural = u"勤務時間"

    def __unicode__(self):
        return u"%s %s年 %s" % (self.project_member, self.year, self.get_month_display())


class HistoryProject(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"案件名称")
    member = models.ForeignKey(Member, verbose_name=u"名前")
    location = models.CharField(max_length=20, blank=True, null=True, verbose_name=u"作業場所")
    description = models.TextField(blank=True, null=True, verbose_name=u"案件概要")
    start_date = models.DateField(blank=True, null=True, verbose_name=u"開始日")
    end_date = models.DateField(blank=True, null=True, verbose_name=u"終了日")
    os = models.ManyToManyField(OS, blank=True, null=True, verbose_name=u"機種／OS")
    role = models.IntegerField(default=1, choices=constants.CHOICE_PROJECT_ROLE, verbose_name=u"作業区分")
    stages = models.ManyToManyField(ProjectStage, blank=True, null=True, verbose_name=u"作業工程")

    class Meta:
        verbose_name = verbose_name_plural = u"以前やっていた案件"

    def __unicode__(self):
        return "%s - %s %s" % (self.name, self.member.first_name, self.member.last_name)
