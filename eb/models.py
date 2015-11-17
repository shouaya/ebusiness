# coding: UTF-8
"""
Created on 2015/08/20

@author: Yang Wanjun
"""
import datetime

from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.core.exceptions import ObjectDoesNotExist

from utils import common, constants


class AbstractCompany(models.Model):
    name = models.CharField(blank=False, null=False, unique=True, max_length=30, verbose_name=u"会社名")
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
    birthday = models.DateField(blank=True, null=True, default=datetime.date.today(), verbose_name=u"生年月日")
    graduate_date = models.DateField(blank=True, null=True, verbose_name=u"卒業年月日")
    join_date = models.DateField(blank=True, null=True, default=datetime.date.today(), verbose_name=u"入社年月日")
    email = models.EmailField(blank=True, null=True, verbose_name=u"メールアドレス")
    private_email = models.EmailField(blank=True, null=True, verbose_name=u"個人メールアドレス")
    post_code = models.CharField(blank=True, null=True, max_length=7, verbose_name=u"郵便番号")
    address1 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"住所１")
    address2 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"住所２")
    nearest_station = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"最寄駅")
    years_in_japan = models.IntegerField(blank=True, null=True, verbose_name=u"在日年数")
    phone = models.CharField(blank=True, null=True, max_length=11, verbose_name=u"電話番号")
    is_married = models.CharField(blank=True, null=True, max_length=1,
                                  choices=constants.CHOICE_MARRIED, verbose_name=u"婚姻状況")
    section = models.ForeignKey('Section', blank=True, null=True, verbose_name=u"部署")
    company = models.ForeignKey('Company', blank=True, null=True, verbose_name=u"会社")
    japanese_description = models.TextField(blank=True, null=True, verbose_name=u"日本語能力の説明")
    certificate = models.TextField(blank=True, null=True, verbose_name=u"資格の説明")
    skill_description = models.TextField(blank=True, null=True, verbose_name=u"得意")
    comment = models.TextField(blank=True, null=True, verbose_name=u"備考")
    user = models.OneToOneField(User, blank=True, null=True)
    is_retired = models.BooleanField(blank=False, null=False, default=False, verbose_name=u"退職")

    class Meta:
        abstract = True


class PublicManager(models.Manager):

    def __init__(self, *args, **kwargs):
        super(PublicManager, self).__init__()
        self.args = args
        self.kwargs = kwargs

    def get_queryset(self):
        return super(PublicManager, self).get_queryset()

    def public_all(self):
        return self.get_queryset().filter(*self.args, **self.kwargs)

    def public_filter(self, *args, **kwargs):
        return self.public_all().filter(*args, **kwargs)


class Company(AbstractCompany):

    bank_name = models.CharField(blank=True, null=True, max_length=20, verbose_name=u"銀行名称")
    branch_no = models.CharField(blank=True, null=True, max_length=3, verbose_name=u"支店番号")
    branch_name = models.CharField(blank=True, null=True, max_length=20, verbose_name=u"支店名称")
    account_type = models.CharField(blank=True, null=True, max_length=1, choices=constants.CHOICE_ACCOUNT_TYPE,
                                    verbose_name=u"預金種類")
    account_number = models.CharField(blank=True, null=True, max_length=7, verbose_name=u"口座番号")
    account_holder = models.CharField(blank=True, null=True, max_length=20, verbose_name=u"口座名義")

    class Meta:
        verbose_name = verbose_name_plural = u"会社"

    def get_all_members(self, user=None):
        if user:
            if user.is_superuser:
                return Member.objects.public_filter(section__is_on_sales=True)
            elif common.is_salesperson_director(user) and user.salesperson.section:
                salesperson_list = user.salesperson.section.salesperson_set.public_all()
                return Member.objects.public_filter(salesperson__in=salesperson_list, section__is_on_sales=True)
            elif common.is_salesperson(user):
                return Member.objects.public_filter(salesperson=user.salesperson, section__is_on_sales=True)
            else:
                return Member.objects.public_filter(pk=-1)
        return Member.objects.public_filter(section__is_on_sales=True)

    def get_working_members(self, user=None):
        now = datetime.date.today()
        if user:
            if user.is_superuser:
                # 管理員の場合全部見られる
                query_set = Member.objects.raw("select distinct m.*"
                                               "  from eb_member m"
                                               "  join eb_projectmember pm on pm.member_id = m.id"
                                               "  join eb_section s on s.id = m.section_id"
                                               " where pm.start_date <= %s"
                                               "   and pm.end_date >= %s"
                                               "   and pm.status = 2"
                                               "   and s.is_on_sales = 1"
                                               "   and m.is_retired = 0"
                                               "   and m.is_deleted = 0"
                                               "   and s.is_deleted = 0"
                                               "   and pm.is_deleted = 0", [now, now])
                return list(query_set)
            elif common.is_salesperson_director(user) and user.salesperson.section:
                # 営業部長の場合、部門内すべての社員が見られる
                salesperson_list = user.salesperson.section.salesperson_set.public_all()
                id_list = [str(salesperson.id) for salesperson in salesperson_list]
                query_set = Member.objects.raw("select distinct m.*"
                                               "  from eb_member m"
                                               "  join eb_projectmember pm on pm.member_id = m.id"
                                               "  join eb_section s on s.id = m.section_id"
                                               " where pm.start_date <= %s"
                                               "   and pm.end_date >= %s"
                                               "   and pm.status = 2"
                                               "   and s.is_on_sales = 1"
                                               "   and m.is_retired = 0"
                                               "   and m.is_deleted = 0"
                                               "   and s.is_deleted = 0"
                                               "   and pm.is_deleted = 0"
                                               "   and m.salesperson_id in (" + ",".join(id_list) + ")", [now, now])
                return list(query_set)
            elif common.is_salesperson(user):
                # 営業員の場合、担当している社員だけ見られる
                query_set = Member.objects.raw("select distinct m.*"
                                               "  from eb_member m"
                                               "  join eb_projectmember pm on pm.member_id = m.id"
                                               "  join eb_section s on s.id = m.section_id"
                                               " where pm.start_date <= %s"
                                               "   and pm.end_date >= %s"
                                               "   and pm.status = 2"
                                               "   and m.salesperson_id = %s"
                                               "   and m.is_retired = 0"
                                               "   and s.is_on_sales = 1"
                                               "   and m.is_deleted = 0"
                                               "   and s.is_deleted = 0"
                                               "   and pm.is_deleted = 0", [now, now, user.salesperson.id])
                return list(query_set)

        return []

    def get_waiting_members(self, user=None):
        now = datetime.date.today()
        if user:
            if user.is_superuser:
                # 管理員の場合全部見られる
                query_set = Member.objects.raw("select distinct m.*"
                                               "  from eb_member m"
                                               "  join eb_section s on s.id = m.section_id"
                                               " where not exists (select 1 "
                                               "                     from eb_projectmember pm"
                                               "                    where pm.member_id = m.id"
                                               "                      and pm.status = 2"
                                               "                      and pm.is_deleted = 0"
                                               "                      and pm.start_date <= %s"
                                               "                      and pm.end_date >= %s)"
                                               "   and s.is_on_sales = 1"
                                               "   and m.is_retired = 0"
                                               "   and m.is_deleted = 0"
                                               "   and s.is_deleted = 0", [now, now])
                return list(query_set)
            elif common.is_salesperson_director(user) and user.salesperson.section:
                # 営業部長の場合、部門内すべての社員が見られる
                salesperson_list = user.salesperson.section.salesperson_set.public_all()
                id_list = [str(salesperson.id) for salesperson in salesperson_list]
                query_set = Member.objects.raw("select distinct m.*"
                                               "  from eb_member m"
                                               "  join eb_section s on s.id = m.section_id"
                                               " where not exists (select 1 "
                                               "                     from eb_projectmember pm"
                                               "                    where pm.member_id = m.id"
                                               "                      and pm.status = 2"
                                               "                      and pm.is_deleted = 0"
                                               "                      and pm.start_date <= %s"
                                               "                      and pm.end_date >= %s)"
                                               "   and s.is_on_sales = 1"
                                               "   and m.is_retired = 0"
                                               "   and m.is_deleted = 0"
                                               "   and s.is_deleted = 0"
                                               "   and m.salesperson_id in (" + ",".join(id_list) + ")", [now, now])
                return list(query_set)
            elif common.is_salesperson(user):
                # 営業員の場合、担当している社員だけ見られる
                query_set = Member.objects.raw("select distinct m.*"
                                               "  from eb_member m"
                                               "  join eb_section s on s.id = m.section_id"
                                               " where not exists (select 1 "
                                               "                     from eb_projectmember pm"
                                               "                    where pm.member_id = m.id"
                                               "                      and pm.status = 2"
                                               "                      and pm.is_deleted = 0"
                                               "                      and pm.start_date <= %s"
                                               "                      and pm.end_date >= %s)"
                                               "   and m.salesperson_id = %s"
                                               "   and m.is_retired = 0"
                                               "   and m.is_deleted = 0"
                                               "   and s.is_deleted = 0"
                                               "   and s.is_on_sales = 1", [now, now, user.salesperson.id])
                return list(query_set)

        return []

    def get_release_members_by_month(self, date, user=None):
        date_first_day = datetime.date(date.year, date.month, 1)
        next_month = common.add_months(date, 1)
        date_next_month = datetime.date(next_month.year, next_month.month, 1)
        if user:
            if user.is_superuser:
                # 管理員の場合全部見られる
                query_set = Member.objects.raw("select distinct m.*"
                                               "  from eb_member m"
                                               "  join eb_section s on s.id = m.section_id and s.is_deleted = 0"
                                               "  join eb_projectmember pm on pm.member_id = m.id"
                                               " where pm.end_date >= %s"
                                               "   and pm.end_date < %s"
                                               "   and m.is_deleted = 0"
                                               "   and pm.is_deleted = 0", [date_first_day, date_next_month])
                return list(query_set)
            elif common.is_salesperson_director(user) and user.salesperson.section:
                # 営業部長の場合、部門内すべての社員が見られる
                salesperson_list = user.salesperson.section.salesperson_set.public_all()
                id_list = [str(salesperson.id) for salesperson in salesperson_list]
                query_set = Member.objects.raw("select distinct m.*"
                                               "  from eb_member m"
                                               "  join eb_section s on s.id = m.section_id and s.is_deleted = 0"
                                               "  join eb_projectmember pm on pm.member_id = m.id"
                                               " where pm.end_date >= %s"
                                               "   and pm.end_date < %s"
                                               "   and m.is_deleted = 0"
                                               "   and pm.is_deleted = 0"
                                               "   and m.salesperson_id in (" + ",".join(id_list) + ")",
                                               [date_first_day, date_next_month])
                return list(query_set)
            elif common.is_salesperson(user):
                # 営業員の場合、担当している社員だけ見られる
                query_set = Member.objects.raw("select distinct m.*"
                                               "  from eb_member m"
                                               "  join eb_section s on s.id = m.section_id and s.is_deleted = 0"
                                               "  join eb_projectmember pm on pm.member_id = m.id"
                                               " where pm.end_date >= %s"
                                               "   and pm.end_date < %s"
                                               "   and m.salesperson_id = %s"
                                               "   and m.is_deleted = 0"
                                               "   and pm.is_deleted = 0",
                                               [date_first_day, date_next_month, user.salesperson.id])
                return list(query_set)
        return []

    def get_release_current_month(self, user=None):
        return self.get_release_members_by_month(datetime.date.today(), user)

    def get_release_next_month(self, user=None):
        next_month = common.add_months(datetime.date.today(), 1)
        return self.get_release_members_by_month(next_month, user)

    def get_release_next_2_month(self, user=None):
        next_2_month = common.add_months(datetime.date.today(), 2)
        return self.get_release_members_by_month(next_2_month, user)

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
            return Project.objects.public_all()
        else:
            return Project.objects.public_filter(status=status)

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
        members = Salesperson.objects.public_filter(member_type=7)
        if members.count() == 1:
            return members[0]
        else:
            return None


class Subcontractor(AbstractCompany):
    president = models.CharField(blank=True, null=True, max_length=30, verbose_name=u"代表者名")
    employee_count = models.IntegerField(blank=True, null=True, verbose_name=u"従業員数")
    sale_amount = models.BigIntegerField(blank=True, null=True, verbose_name=u"売上高")
    payment_month = models.CharField(blank=True, null=True, max_length=1, default='1',
                                     choices=constants.CHOICE_PAYMENT_MONTH, verbose_name=u"支払いサイト")
    payment_day = models.CharField(blank=True, null=True, max_length=2, choices=constants.CHOICE_PAYMENT_DAY,
                                   default='99', verbose_name=u"支払日")
    comment = models.TextField(blank=True, null=True, verbose_name=u"備考")
    is_deleted = models.BooleanField(default=False, editable=False, verbose_name=u"削除フラグ")
    deleted_date = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=u"削除年月日")

    objects = PublicManager(is_deleted=False)

    class Meta:
        ordering = ['name']
        verbose_name = verbose_name_plural = u"協力会社"

    def delete(self, using=None):
        self.is_deleted = True
        self.deleted_date = datetime.datetime.now()
        self.save()


class Section(models.Model):
    name = models.CharField(blank=False, null=False, max_length=30, verbose_name=u"部署名")
    description = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"概要")
    is_on_sales = models.BooleanField(blank=False, null=False, default=False, verbose_name=u"営業対象")
    company = models.ForeignKey(Company, blank=False, null=False, verbose_name=u"会社")
    is_deleted = models.BooleanField(default=False, editable=False, verbose_name=u"削除フラグ")
    deleted_date = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=u"削除年月日")

    objects = PublicManager(is_deleted=False)

    class Meta:
        ordering = ['name']
        verbose_name = verbose_name_plural = u"部署"

    def __unicode__(self):
        if not self.description:
            return self.name
        else:
            desc = self.description[:7] + "..." if len(self.description) > 10 else self.description
            return u"%s(%s)" % (self.name, desc)

    def delete(self, using=None):
        self.is_deleted = True
        self.deleted_date = datetime.datetime.now()
        self.save()


class Salesperson(AbstractMember):

    member_type = models.IntegerField(default=0, choices=constants.CHOICE_SALESPERSON_TYPE, verbose_name=u"社員区分")
    is_deleted = models.BooleanField(default=False, editable=False, verbose_name=u"削除フラグ")
    deleted_date = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=u"削除年月日")

    objects = PublicManager(is_deleted=False, is_retired=False, section__is_deleted=False)

    class Meta:
        ordering = ['first_name', 'last_name']
        verbose_name = verbose_name_plural = u"営業員"

    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)

    def delete(self, using=None):
        self.is_deleted = True
        self.deleted_date = datetime.datetime.now()
        self.save()


class Member(AbstractMember):
    member_type = models.IntegerField(default=0, choices=constants.CHOICE_MEMBER_TYPE, verbose_name=u"社員区分")
    salesperson = models.ForeignKey(Salesperson, blank=True, null=True, verbose_name=u"営業員")
    subcontractor = models.ForeignKey(Subcontractor, blank=True, null=True, verbose_name=u"協力会社")
    cost = models.IntegerField(null=False, default=0, verbose_name=u"コスト")
    is_deleted = models.BooleanField(default=False, editable=False, verbose_name=u"削除フラグ")
    deleted_date = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=u"削除年月日")

    objects = PublicManager(is_deleted=False, is_retired=False, section__is_deleted=False)

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
        projects = self.projectmember_set.public_filter(end_date__gt=now, start_date__lte=now, status=2)
        if projects.count() > 0:
            return projects[0].end_date
        else:
            return None

    def get_business_status(self):
        next_2_month = common.add_months(datetime.date.today(), 2)
        if self.projectmember_set.public_filter(status=1).count() > 0:
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
        project_member_list = self.projectmember_set.public_all()
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
            positions = self.positionship_set.public_filter(is_part_time=False).order_by('-position')
        else:
            positions = self.positionship_set.public_filter(is_part_time=False)
        if positions.count() > 0:
            return positions[0]
        else:
            return None

    def delete(self, using=None):
        self.is_deleted = True
        self.deleted_date = datetime.datetime.now()
        self.save()


class PositionShip(models.Model):
    member = models.ForeignKey(Member, verbose_name=u"社員名")
    position = models.IntegerField(blank=True, null=True, choices=constants.CHOICE_POSITION, verbose_name=u"職位")
    section = models.ForeignKey(Section, verbose_name=u"部署")
    is_part_time = models.BooleanField(default=False, verbose_name=u"兼任")
    is_deleted = models.BooleanField(default=False, editable=False, verbose_name=u"削除フラグ")
    deleted_date = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=u"削除年月日")

    objects = PublicManager(is_deleted=False, section__is_deleted=False)

    class Meta:
        ordering = ['position']
        verbose_name = verbose_name_plural = u"職位"

    def __unicode__(self):
        return "%s - %s %s" % (self.get_position_display(), self.member.first_name, self.member.last_name)

    def delete(self, using=None):
        self.is_deleted = True
        self.deleted_date = datetime.datetime.now()
        self.save()


class Client(AbstractCompany):
    president = models.CharField(blank=True, null=True, max_length=30, verbose_name=u"代表者名")
    employee_count = models.IntegerField(blank=True, null=True, verbose_name=u"従業員数")
    sale_amount = models.BigIntegerField(blank=True, null=True, verbose_name=u"売上高")
    undertaker = models.CharField(blank=True, null=True, max_length=30, verbose_name=u"担当者")
    undertaker_mail = models.EmailField(blank=True, null=True, verbose_name=u"担当者メール")
    payment_month = models.CharField(blank=True, null=True, max_length=1, default='1',
                                     choices=constants.CHOICE_PAYMENT_MONTH, verbose_name=u"支払いサイト")
    payment_day = models.CharField(blank=True, null=True, max_length=2, default='99',
                                   choices=constants.CHOICE_PAYMENT_DAY, verbose_name=u"支払日")
    remark = models.TextField(blank=True, null=True, verbose_name=u"評価")
    comment = models.TextField(blank=True, null=True, verbose_name=u"備考")
    salesperson = models.ForeignKey(Salesperson, blank=True, null=True, verbose_name=u"営業担当")
    request_file = models.FileField(blank=True, null=True, upload_to="./request", verbose_name=u"請求書テンプレート")
    is_deleted = models.BooleanField(default=False, editable=False, verbose_name=u"削除フラグ")
    deleted_date = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=u"削除年月日")

    objects = PublicManager(is_deleted=False)

    class Meta:
        ordering = ['name']
        verbose_name = verbose_name_plural = u"取引先"

    def get_pay_date(self, date=datetime.date.today()):
        """支払い期限日を取得する。

        Arguments：
          なし

        Returns：
          Date

        Raises：
          なし
        """
        months = int(self.payment_month) if self.payment_month else 1
        pay_month = common.add_months(date, months)
        if self.payment_day == '99' or not self.payment_day:
            return common.get_last_day_by_month(pay_month)
        else:
            pay_day = int(self.payment_day)
            return datetime.date(pay_month.year, pay_month.month, pay_day)

    def delete(self, using=None):
        self.is_deleted = True
        self.deleted_date = datetime.datetime.now()
        self.save()


class ClientMember(models.Model):
    name = models.CharField(max_length=30, verbose_name=u"名前")
    email = models.EmailField(blank=True, null=True, verbose_name=u"メールアドレス")
    phone = models.CharField(blank=True, null=True, max_length=11, verbose_name=u"電話番号")
    client = models.ForeignKey(Client, verbose_name=u"所属会社")
    is_deleted = models.BooleanField(default=False, editable=False, verbose_name=u"削除フラグ")
    deleted_date = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=u"削除年月日")

    objects = PublicManager(is_deleted=False, client__is_deleted=False)

    class Meta:
        ordering = ['name']
        verbose_name = verbose_name_plural = u"お客様"

    def __unicode__(self):
        return "%s - %s" % (self.client.name, self.name)

    def delete(self, using=None):
        self.is_deleted = True
        self.deleted_date = datetime.datetime.now()
        self.save()


class Skill(models.Model):
    name = models.CharField(blank=False, null=False, unique=True, max_length=30, verbose_name=u"名称")
    is_deleted = models.BooleanField(default=False, editable=False, verbose_name=u"削除フラグ")
    deleted_date = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=u"削除年月日")

    objects = PublicManager(is_deleted=False)

    class Meta:
        ordering = ['name']
        verbose_name = verbose_name_plural = u"スキル"

    def __unicode__(self):
        return self.name

    def delete(self, using=None):
        self.is_deleted = True
        self.deleted_date = datetime.datetime.now()
        self.save()


class OS(models.Model):
    name = models.CharField(max_length=15, unique=True, verbose_name=u"名称")
    is_deleted = models.BooleanField(default=False, editable=False, verbose_name=u"削除フラグ")
    deleted_date = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=u"削除年月日")

    objects = PublicManager(is_deleted=False)

    class Meta:
        ordering = ['name']
        verbose_name = verbose_name_plural = u"機種／OS"

    def __unicode__(self):
        return self.name

    def delete(self, using=None):
        self.is_deleted = True
        self.deleted_date = datetime.datetime.now()
        self.save()


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
    is_deleted = models.BooleanField(default=False, editable=False, verbose_name=u"削除フラグ")
    deleted_date = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=u"削除年月日")

    objects = PublicManager(is_deleted=False, client__is_deleted=False)

    class Meta:
        ordering = ['name']
        verbose_name = verbose_name_plural = u"案件"

    def __unicode__(self):
        return self.name

    def get_project_members(self):
        # 案件にアサイン人数を取得する。
        return self.projectmember_set.public_all()

    def get_recommended_members(self):
        # 如果案件为提案状态则自动推荐待机中的人员及即将待机的人
        members = []

        if self.status != 1:
            return members

        dict_skills = {}
        for skill in self.skills.public_all():
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

    def get_project_members_by_month(self, d=None):
        if not d:
            d = datetime.date.today()
        first_day = datetime.date(d.year, d.month, 1)
        last_day = common.get_last_day_by_month(d)
        return self.projectmember_set.public_filter(start_date__lte=last_day, end_date__gte=first_day)

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
        project_members = self.projectmember_set.public_filter(start_date__lte=last_day, end_date__gte=first_day, role=7)
        if project_members.count() == 0:
            project_members = self.projectmember_set.public_filter(start_date__lte=last_day, end_date__gte=first_day, role=6)
        if project_members.count() == 0:
            project_members = self.projectmember_set.public_filter(start_date__lte=last_day, end_date__gte=first_day)
        if project_members.count() > 0:
            return project_members[0]
        else:
            return None

    def get_working_project_members(self):
        now = datetime.date.today()
        first_day = datetime.date(now.year, now.month, 1)
        last_day = common.get_last_day_by_month(now)
        return self.projectmember_set.public_filter(start_date__lte=last_day, end_date__gte=first_day)

    def get_order_by_month(self, year=None, month=None):
        """指定年月の注文履歴を取得する。

        Arguments：
          year: 指定年
          month: 指定月

        Returns：
          ClientOrder のインスタンス

        Raises：
          なし
        """
        date = datetime.date.today()
        if not year and not month:
            year = str(date.year)
            month = str(date.month)
        try:
            return self.clientorder_set.get(year=year, month=month)
        except ObjectDoesNotExist:
            return None

    def get_expenses(self, year, month):
        """指定年月の清算リストを取得する。

        Arguments：
          year: 指定年
          month: 指定月

        Returns：
          MemberExpenses のインスタンス

        Raises：
          なし
        """
        return MemberExpenses.objects.public_filter(project_member__project=self,
                                             year=str(year),
                                             month=str(month)).order_by('category__name')

    def delete(self, using=None):
        self.is_deleted = True
        self.deleted_date = datetime.datetime.now()
        self.save()


def get_client_order_path(instance, filename):
    return u"./client_order/{0}/{1}{2}_{3}".format(instance.project.client.name,
                                                   instance.year, instance.month, filename)


class ClientOrder(models.Model):
    project = models.ForeignKey(Project, verbose_name=u"案件")
    name = models.CharField(max_length=30, verbose_name=u"注文書名称")
    year = models.CharField(max_length=4, default=str(datetime.date.today().year),
                            choices=constants.CHOICE_ATTENDANCE_YEAR, verbose_name=u"対象年")
    month = models.CharField(max_length=2, choices=constants.CHOICE_ATTENDANCE_MONTH, verbose_name=u"対象月")
    order_no = models.CharField(max_length=20, verbose_name=u"注文番号")
    order_file = models.FileField(blank=True, null=True, upload_to=get_client_order_path, verbose_name=u"注文書")
    is_deleted = models.BooleanField(default=False, editable=False, verbose_name=u"削除フラグ")
    deleted_date = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=u"削除年月日")

    objects = PublicManager(is_deleted=False, project__is_deleted=False)

    class Meta:
        ordering = ['project', 'name', 'year', 'month']
        unique_together = ('project', 'year', 'month')
        verbose_name = verbose_name_plural = u"お客様注文書"

    def __unicode__(self):
        return self.name

    def delete(self, using=None):
        self.is_deleted = True
        self.deleted_date = datetime.datetime.now()
        self.save()


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
    is_deleted = models.BooleanField(default=False, editable=False, verbose_name=u"削除フラグ")
    deleted_date = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=u"削除年月日")

    objects = PublicManager(is_deleted=False, project__is_deleted=False)

    class Meta:
        ordering = ['project', 'open_date']
        verbose_name = verbose_name_plural = u"案件活動"

    def __unicode__(self):
        return "%s - %s" % (self.project.name, self.name)

    def delete(self, using=None):
        self.is_deleted = True
        self.deleted_date = datetime.datetime.now()
        self.save()


class ProjectSkill(models.Model):
    project = models.ForeignKey(Project, verbose_name=u"案件")
    skill = models.ForeignKey(Skill, verbose_name=u"スキル")
    period = models.IntegerField(blank=True, null=True, choices=constants.CHOICE_SKILL_TIME, verbose_name=u"経験年数")
    description = models.TextField(blank=True, null=True, verbose_name=u"備考")
    is_deleted = models.BooleanField(default=False, editable=False, verbose_name=u"削除フラグ")
    deleted_date = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=u"削除年月日")

    objects = PublicManager(is_deleted=False, project__is_deleted=False)

    class Meta:
        verbose_name = verbose_name_plural = u"案件のスキル要求"

    def __unicode__(self):
        return "%s - %s" % (self.project.name, self.skill.name)

    def delete(self, using=None):
        self.is_deleted = True
        self.deleted_date = datetime.datetime.now()
        self.save()


class ProjectStage(models.Model):
    name = models.CharField(max_length=15, unique=True, verbose_name=u"作業工程名称")
    is_deleted = models.BooleanField(default=False, editable=False, verbose_name=u"削除フラグ")
    deleted_date = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=u"削除年月日")

    objects = PublicManager(is_deleted=False)

    class Meta:
        verbose_name = verbose_name_plural = u"作業工程"

    def __unicode__(self):
        return self.name

    def delete(self, using=None):
        self.is_deleted = True
        self.deleted_date = datetime.datetime.now()
        self.save()


class ProjectMember(models.Model):
    project = models.ForeignKey(Project, verbose_name=u'案件名称')
    member = models.ForeignKey(Member, verbose_name=u"名前")
    start_date = models.DateField(blank=True, null=True, verbose_name=u"開始日")
    end_date = models.DateField(blank=True, null=True, verbose_name=u"終了日")
    price = models.IntegerField(default=0, verbose_name=u"単価")
    expenses = models.IntegerField(default=0, verbose_name=u"交通費")
    min_hours = models.DecimalField(max_digits=5, decimal_places=2, default=160, verbose_name=u"基準時間")
    max_hours = models.DecimalField(max_digits=5, decimal_places=2, default=180, verbose_name=u"最大時間")
    status = models.IntegerField(null=False, default=1,
                                 choices=constants.CHOICE_PROJECT_MEMBER_STATUS, verbose_name=u"ステータス")
    role = models.CharField(default="PG", max_length=2, choices=constants.CHOICE_PROJECT_ROLE, verbose_name=u"作業区分")
    stages = models.ManyToManyField(ProjectStage, blank=True, null=True, verbose_name=u"作業工程")
    is_deleted = models.BooleanField(default=False, editable=False, verbose_name=u"削除フラグ")
    deleted_date = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=u"削除年月日")

    objects = PublicManager(is_deleted=False, project__is_deleted=False, member__is_deleted=False,
                            member__section__is_deleted=False)

    class Meta:
        verbose_name = verbose_name_plural = u"案件メンバー"

    def __unicode__(self):
        return "%s - %s %s" % (self.project.name, self.member.first_name, self.member.last_name)

    def is_in_rd(self):
        if self.stages.public_filter(name=u"要件定義").count() > 0:
            return True
        else:
            return False

    def is_in_sa(self):
        if self.stages.public_filter(name=u"調査分析").count() > 0:
            return True
        else:
            return False

    def is_in_bd(self):
        if self.stages.public_filter(name=u"基本設計").count() > 0:
            return True
        else:
            return False

    def is_in_dd(self):
        if self.stages.public_filter(name=u"詳細設計").count() > 0:
            return True
        else:
            return False

    def is_in_pg(self):
        if self.stages.public_filter(name=u"開発製造").count() > 0:
            return True
        else:
            return False

    def is_in_pt(self):
        if self.stages.public_filter(name=u"単体試験").count() > 0:
            return True
        else:
            return False

    def is_in_it(self):
        if self.stages.public_filter(name=u"結合試験").count() > 0:
            return True
        else:
            return False

    def is_in_st(self):
        if self.stages.public_filter(name=u"総合試験").count() > 0:
            return True
        else:
            return False

    def is_in_maintain(self):
        if self.stages.public_filter(name=u"保守運用").count() > 0:
            return True
        else:
            return False

    def is_in_support(self):
        if self.stages.public_filter(name=u"サポート").count() > 0:
            return True
        else:
            return False

    def get_attendance(self, year, month):
        """指定された年月によって、該当するメンバーの勤怠情報を取得する。

        Arguments：
          year: 対象年
          month: 対象月

        Returns：
          MemberAttendanceのインスタンス、または None

        Raises：
          なし
        """
        try:
            return self.memberattendance_set.get(year=str(year), month="%02d" % (month,))
        except ObjectDoesNotExist:
            return None

    def delete(self, using=None):
        self.is_deleted = True
        self.deleted_date = datetime.datetime.now()
        self.save()


class ExpensesCategory(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"名称")
    is_deleted = models.BooleanField(default=False, editable=False, verbose_name=u"削除フラグ")
    deleted_date = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=u"削除年月日")

    objects = PublicManager(is_deleted=False)

    class Meta:
        verbose_name = verbose_name_plural = u"清算分類"

    def __unicode__(self):
        return self.name

    def delete(self, using=None):
        self.is_deleted = True
        self.deleted_date = datetime.datetime.now()
        self.save()


class MemberExpenses(models.Model):
    project_member = models.ForeignKey(ProjectMember, verbose_name=u"要員")
    year = models.CharField(max_length=4, default=str(datetime.date.today().year),
                            choices=constants.CHOICE_ATTENDANCE_YEAR, verbose_name=u"対象年")
    month = models.CharField(max_length=2, choices=constants.CHOICE_ATTENDANCE_MONTH, verbose_name=u"対象月")
    category = models.ForeignKey(ExpensesCategory, verbose_name=u"分類")
    price = models.IntegerField(default=0, verbose_name=u"価格")
    is_deleted = models.BooleanField(default=False, editable=False, verbose_name=u"削除フラグ")
    deleted_date = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=u"削除年月日")

    objects = PublicManager(is_deleted=False, project_member__is_deleted=False, category__is_deleted=False)

    class Meta:
        ordering = ['project_member', 'year', 'month']
        verbose_name = verbose_name_plural = u"清算リスト"

    def __unicode__(self):
        return u"%s %s %s" % (self.project_member, self.get_year_display(), self.get_month_display())

    def delete(self, using=None):
        self.is_deleted = True
        self.deleted_date = datetime.datetime.now()
        self.save()


class MemberAttendance(models.Model):
    project_member = models.ForeignKey(ProjectMember, verbose_name=u"要員")
    year = models.CharField(max_length=4, default=str(datetime.date.today().year),
                            choices=constants.CHOICE_ATTENDANCE_YEAR, verbose_name=u"対象年")
    month = models.CharField(max_length=2, choices=constants.CHOICE_ATTENDANCE_MONTH, verbose_name=u"対象月")
    rate = models.DecimalField(max_digits=3, decimal_places=2, default=1, verbose_name=u"率")
    total_hours = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=u"合計時間")
    extra_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name=u"残業時間")
    plus_per_hour = models.IntegerField(blank=True, null=True, verbose_name=u"増（円）")
    minus_per_hour = models.IntegerField(blank=True, null=True, verbose_name=u"減（円）")
    price = models.IntegerField(default=0, verbose_name=u"価格")
    comment = models.CharField(blank=True, null=True, max_length=50, verbose_name=u"備考")
    is_deleted = models.BooleanField(default=False, editable=False, verbose_name=u"削除フラグ")
    deleted_date = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=u"削除年月日")

    objects = PublicManager(is_deleted=False, project_member__is_deleted=False)

    class Meta:
        ordering = ['project_member', 'year', 'month']
        verbose_name = verbose_name_plural = u"勤務時間"

    def __unicode__(self):
        return u"%s %s %s" % (self.project_member, self.get_year_display(), self.get_month_display())

    def delete(self, using=None):
        self.is_deleted = True
        self.deleted_date = datetime.datetime.now()
        self.save()


class Degree(models.Model):
    member = models.ForeignKey(Member, verbose_name=u"社員")
    start_date = models.DateField(verbose_name=u"入学日")
    end_date = models.DateField(verbose_name=u"卒業日")
    description = models.CharField(blank=True, null=True, max_length=255, verbose_name=u"学校名称/学部/専門/学位")
    is_deleted = models.BooleanField(default=False, editable=False, verbose_name=u"削除フラグ")
    deleted_date = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=u"削除年月日")

    objects = PublicManager(is_deleted=False, member__is_deleted=False, member__section__is_deleted=False)

    class Meta:
        verbose_name = verbose_name_plural = u"学歴"

    def delete(self, using=None):
        self.is_deleted = True
        self.deleted_date = datetime.datetime.now()
        self.save()


class HistoryProject(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"案件名称")
    member = models.ForeignKey(Member, verbose_name=u"名前")
    location = models.CharField(max_length=20, blank=True, null=True, verbose_name=u"作業場所")
    description = models.TextField(blank=True, null=True, verbose_name=u"案件概要")
    start_date = models.DateField(blank=True, null=True, verbose_name=u"開始日")
    end_date = models.DateField(blank=True, null=True, verbose_name=u"終了日")
    os = models.ManyToManyField(OS, blank=True, null=True, verbose_name=u"機種／OS")
    skill = models.ManyToManyField(Skill, blank=True, null=True, verbose_name=u"スキル要求")
    role = models.CharField(default="PG", max_length=2, choices=constants.CHOICE_PROJECT_ROLE, verbose_name=u"作業区分")
    stages = models.ManyToManyField(ProjectStage, blank=True, null=True, verbose_name=u"作業工程")
    is_deleted = models.BooleanField(default=False, editable=False, verbose_name=u"削除フラグ")
    deleted_date = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=u"削除年月日")

    objects = PublicManager(is_deleted=False, member__is_deleted=False, member__section__is_deleted=False)

    class Meta:
        ordering = ['-start_date']
        verbose_name = verbose_name_plural = u"以前やっていた案件"

    def __unicode__(self):
        return "%s - %s %s" % (self.name, self.member.first_name, self.member.last_name)

    def is_in_rd(self):
        if self.stages.public_filter(name=u"要件定義").count() > 0:
            return True
        else:
            return False

    def is_in_sa(self):
        if self.stages.public_filter(name=u"調査分析").count() > 0:
            return True
        else:
            return False

    def is_in_bd(self):
        if self.stages.public_filter(name=u"基本設計").count() > 0:
            return True
        else:
            return False

    def is_in_dd(self):
        if self.stages.public_filter(name=u"詳細設計").count() > 0:
            return True
        else:
            return False

    def is_in_pg(self):
        if self.stages.public_filter(name=u"開発製造").count() > 0:
            return True
        else:
            return False

    def is_in_pt(self):
        if self.stages.public_filter(name=u"単体試験").count() > 0:
            return True
        else:
            return False

    def is_in_it(self):
        if self.stages.public_filter(name=u"結合試験").count() > 0:
            return True
        else:
            return False

    def is_in_st(self):
        if self.stages.public_filter(name=u"総合試験").count() > 0:
            return True
        else:
            return False

    def is_in_maintain(self):
        if self.stages.public_filter(name=u"保守運用").count() > 0:
            return True
        else:
            return False

    def is_in_support(self):
        if self.stages.public_filter(name=u"サポート").count() > 0:
            return True
        else:
            return False

    def delete(self, using=None):
        self.is_deleted = True
        self.deleted_date = datetime.datetime.now()
        self.save()


def create_group_salesperson():
    group_salesperson, created = Group.objects.get_or_create(name="Salesperson")
    if created:
        for codename in ('add_subcontractor', 'change_subcontractor',
                         'add_section', 'change_section',
                         'add_member', 'change_member',
                         'add_positionship', 'change_positionship',
                         'add_client', 'change_client',
                         'add_clientmember', 'change_clientmember',
                         'add_skill', 'change_skill', 'delete_skill',
                         'add_os', 'change_os', 'delete_os',
                         'add_project', 'change_project',
                         'add_projectactivity', 'change_projectactivity', 'delete_projectactivity',
                         'add_projectskill', 'change_projectskill',
                         'add_projectstage', 'change_projectstage',
                         'add_projectmember', 'change_projectmember', 'delete_projectmember',
                         'add_memberattendance', 'change_memberattendance', 'delete_memberattendance',
                         'add_historyproject', 'change_historyproject', 'delete_historyproject'):
            permission = Permission.objects.get(codename=codename)
            group_salesperson.permissions.add(permission)

    return group_salesperson