# coding: UTF-8
"""
Created on 2015/08/20

@author: Yang Wanjun
"""
import datetime
import re
import urllib2
import xml.etree.ElementTree as ET

from django.db import models, connection
from django.contrib.auth.models import User, Group, Permission
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max, Min, Q, Sum
from django.utils import timezone


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
    birthday = models.DateField(blank=True, null=True, verbose_name=u"生年月日")
    graduate_date = models.DateField(blank=True, null=True, verbose_name=u"卒業年月日")
    join_date = models.DateField(blank=True, null=True, default=timezone.now, verbose_name=u"入社年月日")
    email = models.EmailField(blank=True, null=True, verbose_name=u"メールアドレス")
    private_email = models.EmailField(blank=True, null=True, verbose_name=u"個人メールアドレス")
    post_code = models.CharField(blank=True, null=True, max_length=7, verbose_name=u"郵便番号")
    address1 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"住所１")
    address2 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"住所２")
    lat = models.CharField(blank=True, null=True, max_length=25, verbose_name=u"緯度")
    lng = models.CharField(blank=True, null=True, max_length=25, verbose_name=u"経度")
    coordinate_update_date = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=u"座標更新日時")
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
    is_notify = models.BooleanField(default=False, verbose_name=u"メール通知")
    notify_type = models.IntegerField(blank=True, null=True, choices=constants.CHOICE_NOTIFY_TYPE, verbose_name=u"通知種類")
    is_retired = models.BooleanField(blank=False, null=False, default=False, verbose_name=u"退職")

    class Meta:
        abstract = True


class PublicManager(models.Manager):

    use_for_related_fields = True

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

    quotation_file = models.FileField(blank=True, null=True, upload_to="./quotation",
                                      verbose_name=u"見積書テンプレート")
    request_file = models.FileField(blank=True, null=True, upload_to="./request", verbose_name=u"請求書テンプレート")
    request_lump_file = models.FileField(blank=True, null=True, upload_to="./request",
                                         verbose_name=u"請求書テンプレート(一括)")
    order_file = models.FileField(blank=True, null=True, upload_to="./eb_order", verbose_name=u"註文書テンプレート",
                                  help_text=u"協力会社への註文書。")

    class Meta:
        verbose_name = verbose_name_plural = u"会社"

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

    def get_members_to_set_coordinate(self):
        now = datetime.datetime.now()
        last_week = now + datetime.timedelta(days=-7)
        # １週間前更新したレコード
        members = Member.objects.public_filter(Q(coordinate_update_date__lt=last_week) |
                                               Q(coordinate_update_date__isnull=True))
        members = members.filter(address1__isnull=False).exclude(address1__exact=u'')
        return members


class BankInfo(models.Model):
    company = models.ForeignKey(Company, verbose_name=u"会社")
    bank_name = models.CharField(blank=False, null=False, max_length=20, verbose_name=u"銀行名称")
    branch_no = models.CharField(blank=False, null=False, max_length=3, verbose_name=u"支店番号")
    branch_name = models.CharField(blank=False, null=False, max_length=20, verbose_name=u"支店名称")
    account_type = models.CharField(blank=False, null=False, max_length=1, choices=constants.CHOICE_ACCOUNT_TYPE,
                                    verbose_name=u"預金種類")
    account_number = models.CharField(blank=False, null=False, max_length=7, verbose_name=u"口座番号")
    account_holder = models.CharField(blank=True, null=True, max_length=20, verbose_name=u"口座名義")
    is_deleted = models.BooleanField(default=False, editable=False, verbose_name=u"削除フラグ")
    deleted_date = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=u"削除年月日")

    objects = PublicManager(is_deleted=False)

    class Meta:
        unique_together = ('branch_no', 'account_number')
        verbose_name = verbose_name_plural = u"銀行口座"

    def __unicode__(self):
        return self.bank_name

    def delete(self, using=None):
        self.is_deleted = True
        self.deleted_date = datetime.datetime.now()
        self.save()


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

    def get_start_date(self):
        """
        協力社員のアサイン情報の一番古い日付を取得する。
        :return:
        """
        members = self.member_set.all()
        min_start_date = ProjectMember.objects.public_filter(member__in=members).aggregate(Min('start_date'))
        start_date = min_start_date.get('start_date__min')
        return start_date if start_date else datetime.date.today()

    def get_end_date(self):
        """
        協力社員のアサイン情報の一番最後日付を取得する。
        :return:
        """
        members = self.member_set.all()
        max_end_date = ProjectMember.objects.public_filter(member__in=members).aggregate(Max('end_date'))
        end_date = max_end_date.get('end_date__max')
        return end_date if end_date else datetime.date.today()

    def get_members_by_month(self, date):
        """
        指定月の協力社員情報を取得する
        :param date: 指定月
        :return:
        """
        first_day = common.get_first_day_by_month(date)
        last_day = common.get_last_day_by_month(first_day)
        members = self.member_set.filter(projectmember__start_date__lte=last_day,
                                         projectmember__end_date__gte=first_day)
        return members

    def get_year_month_order_finished(self):
        """
        月単位の註文情報を取得する。
        :return:
        """
        ret_value = []
        for year, month in common.get_year_month_list(self.get_start_date(), self.get_end_date()):
            first_day = datetime.date(int(year), int(month), 1)
            try:
                subcontractor_order = SubcontractorOrder.objects.get(subcontractor=self, year=year, month=month)
            except ObjectDoesNotExist:
                subcontractor_order = None
            members = self.get_members_by_month(first_day)
            bp_members = BpMemberOrderInfo.objects.public_filter(member__in=members, year=year, month=month)
            if members.count() > 0 and members.count() == bp_members.count():
                is_finished = True
            else:
                is_finished = False
            ret_value.append((year, month, subcontractor_order, is_finished))
        return ret_value

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
        return self.name

    def delete(self, using=None):
        self.is_deleted = True
        self.deleted_date = datetime.datetime.now()
        self.save()


class Salesperson(AbstractMember):

    member_type = models.IntegerField(default=5, choices=constants.CHOICE_SALESPERSON_TYPE, verbose_name=u"社員区分")
    is_deleted = models.BooleanField(default=False, editable=False, verbose_name=u"削除フラグ")
    deleted_date = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=u"削除年月日")

    objects = PublicManager(is_deleted=False, is_retired=False, section__is_deleted=False)

    class Meta:
        ordering = ['first_name', 'last_name']
        verbose_name = verbose_name_plural = u"営業員"

    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)

    def get_all_members(self):
        if self.member_type == 0 and self.section:
            # 営業部長の場合、部門内すべての社員が見られる
            return Member.objects.public_filter(salesperson__in=self.get_under_salesperson())
        else:
            # 営業員の場合、担当している社員だけ見られる
            return Member.objects.public_filter(salesperson=self)

    def get_working_members(self):
        now = datetime.date.today()
        if self.member_type == 0 and self.section:
            # 営業部長の場合、部門内すべての社員が見られる
            return Member.objects.public_filter(projectmember__start_date__lte=now,
                                                projectmember__end_date__gte=now,
                                                projectmember__status=2,
                                                salesperson__in=self.get_under_salesperson())
        else:
            # 営業員の場合、担当している社員だけ見られる
            return Member.objects.public_filter(projectmember__start_date__lte=now,
                                                projectmember__end_date__gte=now,
                                                projectmember__status=2,
                                                salesperson=self)

    def get_waiting_members(self):
        if self.member_type == 0 and self.section:
            # 営業部長の場合、部門内すべての社員が見られる
            working_members = self.get_working_members()
            return self.get_all_members().exclude(pk__in=working_members)
        else:
            # 営業員の場合、担当している社員だけ見られる
            working_members = self.get_working_members()
            return self.get_all_members().exclude(pk__in=working_members)

    def get_under_salesperson(self):
        """部下の営業員を取得する、部下がない場合自分を返す。
        """
        if self.member_type == 0 and self.section:
            return self.section.salesperson_set.public_all()
        else:
            return [self]

    def get_notify_mail_list(self):
        if self.is_notify:
            if self.notify_type == 1:
                return [self.email]
            elif self.notify_type == 2:
                return [self.private_email]
            elif self.notify_type == 3:
                return [self.email, self.private_email]

        return []

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

    objects = PublicManager(is_deleted=False, is_retired=False)

    class Meta:
        ordering = ['first_name', 'last_name']
        verbose_name = verbose_name_plural = u"社員"

    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)

    def get_age(self):
        birthday = self.birthday
        if birthday:
            today = datetime.date.today()
            years = today.year - birthday.year
            if today.month < birthday.month:
                years -= 1
            elif today.month == birthday.month:
                if today.day <= birthday.day:
                    years -= 1
            return years
        else:
            return None

    def get_current_project_member(self):
        """現在実施中の案件アサイン情報を取得する
        """
        now = datetime.datetime.now()
        projects = self.projectmember_set.public_filter(end_date__gte=now, start_date__lte=now, status=2)
        if projects.count() > 0:
            return projects[0]
        else:
            return None

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

    def set_coordinate(self):
        if self.address1 and not self.lat and not self.lng:
            address = self.address1
            if self.address2:
                address += self.address2
            try:
                response = urllib2.urlopen("http://www.geocoding.jp/api/?q={0}".format(address.encode("utf8")))
                xml = response.read()
                tree = ET.XML(xml)
                lat = tree.find(".//coordinate/lat")
                lng = tree.find(".//coordinate/lng")
                if lat is not None and lng is not None:
                    self.lat = lat.text
                    self.lng = lng.text
                    self.save()
                    return True
                else:
                    return False
            except:
                return False
        return False

    def get_bp_member_info(self, date):
        """
        他者技術者の場合、注文の詳細情報を取得する。
        :param date 対象年月
        :return:
        """
        members = self.bpmemberorderinfo_set.filter(year=str(date.year), month="%02d" % (date.month,))
        if members.count() > 0:
            return members[0]
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

    objects = PublicManager(is_deleted=False)

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
    tax_rate = models.DecimalField(default=0.08, max_digits=3, decimal_places=2, choices=constants.CHOICE_TAX_RATE,
                                   verbose_name=u"税率")
    decimal_type = models.CharField(max_length=1, default='0', choices=constants.CHOICE_DECIMAL_TYPE,
                                    verbose_name=u"小数の処理区分")
    remark = models.TextField(blank=True, null=True, verbose_name=u"評価")
    comment = models.TextField(blank=True, null=True, verbose_name=u"備考")
    salesperson = models.ForeignKey(Salesperson, blank=True, null=True, verbose_name=u"営業担当")
    quotation_file = models.FileField(blank=True, null=True, upload_to="./quotation",
                                      verbose_name=u"見積書テンプレート")
    request_file = models.FileField(blank=True, null=True, upload_to="./request", verbose_name=u"請求書テンプレート",
                                    help_text=u"如果该项目为空，则使用EB自己的模板。")
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

    def get_turnover_month(self, date):
        """お客様の売上情報を取得する。

        Arguments：
          date: 指定する月

        Returns：
          Date

        Raises：
          なし
        """
        if not date:
            date = datetime.date.today()

        first_day = common.get_first_day_by_month(date)
        last_day = common.get_last_day_by_month(date)
        cost = ProjectMember.objects.public_filter(project__client=self,
                                                   start_date__lte=last_day,
                                                   end_date__gte=first_day)\
            .aggregate(cost=Sum('member__cost'))
        cost = cost.get('cost', 0) if cost.get('cost', 0) else 0

        amount = ProjectRequest.objects.filter(project__client=self,
                                               year='%04d' % (date.year,),
                                               month='%02d' % (date.month,))\
            .aggregate(amount=Sum('amount'))
        amount = amount.get('amount', 0) if amount.get('amount', 0) else 0

        profit = amount - cost
        return {'cost': cost, 'price': amount, 'profit': profit}

    def get_turnover_month_detail(self, date):
        """要員毎の売上情報を取得する。

        Arguments：
          date: 指定する月

        Returns：
          Date

        Raises：
          なし
        """
        first_day = common.get_first_day_by_month(date)
        last_day = common.get_last_day_by_month(date)

        cursor = connection.cursor()
        cursor.execute(u"select pm.project_id, p.name as project_name, m.employee_id"
                       u"     , concat(m.first_name, ' ', m.last_name) as member_name"
                       u"     , pm.start_date, pm.end_date"
                       u"     , pm.price as base_price"
                       u"     , ifnull(m.cost, 0) as cost"
                       u"     , ifnull(ma.price, 0) as total_price"
                       u"     , ifnull(ma.price, 0) - ifnull(m.cost, 0) as profit"
                       u"  from eb_projectmember pm"
                       u"  join eb_member m on m.id = pm.member_id"
                       u"  join eb_project p on p.id = pm.project_id"
                       u"  left join eb_memberattendance ma on ma.project_member_id = pm.id"
                       u"		 and ma.year = %s and ma.month = %s"
                       u" where p.client_id = %s"
                       u"   and pm.start_date <= %s"
                       u"   and pm.end_date >= %s"
                       u"   and pm.is_deleted = 0"
                       u"   and pm.status = 2"
                       u" order by p.name", [str(date.year), '%02d' % (date.month,), self.pk, last_day, first_day])
        members = []
        for project_id, project_name, employee_id, member_name, start_date, end_date, base_price, cost, total_price, profit \
                in cursor.fetchall():
            d = dict()
            d['project_id'] = project_id
            d['project_name'] = project_name
            d['employee_id'] = employee_id
            d['member_name'] = member_name
            d['start_date'] = start_date
            d['end_date'] = end_date
            d['base_price'] = base_price
            d['cost'] = cost
            d['total_price'] = total_price
            d['profit'] = profit
            members.append(d)
        return members

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
    skills = models.ManyToManyField(Skill, through='ProjectSkill', blank=True, verbose_name=u"スキル要求")
    os = models.ManyToManyField(OS, blank=True, verbose_name=u"機種／OS")
    start_date = models.DateField(blank=True, null=True, verbose_name=u"開始日")
    end_date = models.DateField(blank=True, null=True, verbose_name=u"終了日")
    address = models.CharField(blank=True, null=True, max_length=255, verbose_name=u"作業場所")
    status = models.IntegerField(choices=constants.CHOICE_PROJECT_STATUS, verbose_name=u"ステータス")
    attendance_type = models.CharField(max_length=1, default='1', choices=constants.CHOICE_ATTENDANCE_TYPE,
                                       verbose_name=u"出勤の計算区分")
    min_hours = models.DecimalField(max_digits=5, decimal_places=2, default=160, verbose_name=u"基準時間",
                                    help_text=u"该项目仅仅是作为项目中各人员时间的默认设置，计算时不会使用该值。")
    max_hours = models.DecimalField(max_digits=5, decimal_places=2, default=180, verbose_name=u"最大時間",
                                    help_text=u"该项目仅仅是作为项目中各人员时间的默认设置，计算时不会使用该值。")
    is_lump = models.BooleanField(default=False, verbose_name=u"一括フラグ")
    lump_amount = models.BigIntegerField(default=0, blank=True, null=True, verbose_name=u"一括金額")
    lump_comment = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"一括の備考",
                                    help_text=u"该项目会作为请求书中備考栏中的值。")
    client = models.ForeignKey(Client, null=True, verbose_name=u"関連会社")
    boss = models.ForeignKey(ClientMember, blank=True, null=True, related_name="boss_set", verbose_name=u"案件責任者")
    middleman = models.ForeignKey(ClientMember, blank=True, null=True,
                                  related_name="middleman_set", verbose_name=u"案件連絡者")
    salesperson = models.ForeignKey(Salesperson, blank=True, null=True, verbose_name=u"営業員")
    members = models.ManyToManyField(Member, through='ProjectMember', blank=True)
    insert_date = models.DateTimeField(blank=True, null=True, auto_now_add=True, editable=False,
                                       verbose_name=u"追加日時")
    update_date = models.DateTimeField(blank=True, null=True, auto_now=True, editable=False,
                                       verbose_name=u"更新日時")
    is_deleted = models.BooleanField(default=False, editable=False, verbose_name=u"削除フラグ")
    deleted_date = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=u"削除日時")

    objects = PublicManager(is_deleted=False, client__is_deleted=False)

    class Meta:
        ordering = ['name']
        unique_together = ('name', 'client')
        verbose_name = verbose_name_plural = u"案件"

    def __unicode__(self):
        return self.name

    def get_project_members(self):
        # 案件にアサイン人数を取得する。
        return self.projectmember_set.public_filter(is_deleted=False)

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

    def get_project_members_by_month(self, date=None, ym=None):
        if date:
            first_day = datetime.date(date.year, date.month, 1)
        elif ym:
            first_day = common.get_first_day_from_ym(ym)
        else:
            date = datetime.date.today()
            first_day = datetime.date(date.year, date.month, 1)
        last_day = common.get_last_day_by_month(first_day)
        return self.projectmember_set.public_filter(start_date__lte=last_day,
                                                    end_date__gte=first_day).exclude(status='1')

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

    def get_expenses(self, year, month, project_members):
        """指定年月の清算リストを取得する。

        Arguments：
          year: 指定年
          month: 指定月

        Returns：
          MemberExpenses のインスタンス

        Raises：
          なし
        """
        return MemberExpenses.objects.filter(project_member__project=self,
                                             year=str(year),
                                             month=str(month),
                                             project_member__in=project_members).order_by('category__name')

    def get_order_by_month(self, year, month):
        """指定年月の注文履歴を取得する。

        Arguments：
          year: 指定年
          month: 指定月

        Returns：
          ClientOrder のインスタンス

        Raises：
          なし
        """
        ym = year + month
        first_day = common.get_first_day_from_ym(ym)
        last_day = common.get_last_day_by_month(first_day)
        return self.clientorder_set.public_filter(start_date__lte=last_day, end_date__gte=first_day, is_deleted=False)

    def get_year_month_order_finished(self):
        """案件の月単位の註文書を取得する。

        Arguments：
          なし

        Returns：
          (対象年, 対処月, ClientOrder, 注文書数)

        Raises：
          なし
        """
        ret_value = []
        for year, month in common.get_year_month_list(self.start_date, self.end_date):
            client_orders = self.get_order_by_month(year, month)
            if client_orders:
                cnt = client_orders.count()
                project_members_month = self.get_project_members_by_month(ym=year + month)
                for client_order in client_orders:
                    ret_value.append((year, month, client_order, cnt, project_members_month))
            else:
                ret_value.append((year, month, None, 0, None))
        return ret_value

    def get_year_month_attendance_finished(self):
        """案件の月単位の勤怠入力状況を取得する。

        Arguments：
          なし

        Returns：
          (対象年月, True / False)

        Raises：
          なし
        """
        ret_value = []
        for year, month in common.get_year_month_list(self.start_date, self.end_date):
            first_day = datetime.date(int(year), int(month), 1)
            last_day = common.get_last_day_by_month(first_day)
            project_members = self.get_project_members_by_month(first_day)
            if project_members.count() == 0:
                ret_value.append((year + month, False))
            else:
                query_set = ProjectMember.objects.raw(u"select pm.* "
                                                      u"  from eb_projectmember pm"
                                                      u" where not exists (select 1 "
                                                      u"                     from eb_memberattendance ma"
                                                      u"				    where pm.id = ma.project_member_id"
                                                      u"                      and ma.year = %s"
                                                      u"                      and ma.month = %s"
                                                      u"					  and ma.is_deleted = 0)"
                                                      u"   and pm.end_date >= %s"
                                                      u"   and pm.start_date <= %s"
                                                      u"   and pm.project_id = %s"
                                                      u"   and pm.is_deleted = 0",
                                                      [year, month, first_day, last_day, self.pk])
                project_members = list(query_set)
                ret_value.append((year + month, False if len(project_members) > 0 else True))
        return ret_value

    def get_project_request(self, str_year, str_month):
        """請求番号を取得する。

        Arguments：
          str_year: 対象年
          str_month: 対象月

        Returns：
          "yyyymm001"の請求番号

        Raises：
          なし
        """
        if self.pk in (90, 64, 104):
            pass
        if self.projectrequest_set.filter(year=str_year, month=str_month).count() == 0:
            # 指定年月の請求番号がない場合、請求番号を発行する。
            max_request_no = ProjectRequest.objects.filter(year=str_year, month=str_month).aggregate(Max('request_no'))
            request_no = max_request_no.get('request_no__max')
            if request_no and re.match(r"^([0-9]{7}|[0-9]{7}-[0-9]{3})$", request_no):
                no = request_no[4:7]
                no = "%03d" % (int(no) + 1,)
                next_request = "%s%s%s" % (str_year[2:], str_month, no)
            else:
                next_request = "%s%s%s" % (str_year[2:], str_month, "001")
            project_request = ProjectRequest(project=self, year=str_year, month=str_month, request_no=next_request)
            return project_request
        else:
            # 存在する場合、そのまま使う、再発行はしません。
            project_request = self.projectrequest_set.filter(year=str_year, month=str_month)[0]
            return project_request

    def delete(self, using=None):
        self.is_deleted = True
        self.deleted_date = datetime.datetime.now()
        self.save()


def get_client_order_path(instance, filename):
    return u"./client_order/{0}/{1}{2}_{3}".format(instance.project.client.name,
                                                   instance.start_date.year, instance.start_date.month,
                                                   filename)


class ClientOrder(models.Model):
    projects = models.ManyToManyField(Project, verbose_name=u"案件")
    name = models.CharField(max_length=30, verbose_name=u"注文書名称")
    start_date = models.DateField(default=common.get_first_day_current_month(), verbose_name=u"開始日")
    end_date = models.DateField(default=common.get_last_day_current_month(), verbose_name=u"終了日")
    order_no = models.CharField(max_length=20, verbose_name=u"注文番号")
    order_date = models.DateField(blank=False, null=True, verbose_name=u"注文日")
    bank_info = models.ForeignKey(BankInfo, blank=False, null=True, verbose_name=u"振込先口座")
    order_file = models.FileField(blank=True, null=True, upload_to=get_client_order_path, verbose_name=u"注文書")
    member_comma_list = models.CommaSeparatedIntegerField(max_length=255, blank=True, null=True, editable=False,
                                                          verbose_name=u"メンバー主キーのリスト")
    is_deleted = models.BooleanField(default=False, editable=False, verbose_name=u"削除フラグ")
    deleted_date = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=u"削除年月日")

    objects = PublicManager(is_deleted=False, project__is_deleted=False)

    class Meta:
        ordering = ['name', 'start_date', 'end_date']
        verbose_name = verbose_name_plural = u"お客様注文書"

    def __unicode__(self):
        return self.name

    def delete(self, using=None):
        self.is_deleted = True
        self.deleted_date = datetime.datetime.now()
        self.save()


class ProjectRequest(models.Model):
    project = models.ForeignKey(Project, verbose_name=u"案件")
    year = models.CharField(max_length=4, default=str(datetime.date.today().year),
                            choices=constants.CHOICE_ATTENDANCE_YEAR, verbose_name=u"対象年")
    month = models.CharField(max_length=2, choices=constants.CHOICE_ATTENDANCE_MONTH, verbose_name=u"対象月")
    request_no = models.CharField(max_length=7, unique=True, verbose_name=u"請求番号")
    amount = models.IntegerField(default=0, verbose_name=u"請求金額")
    created_date = models.DateTimeField(null=True, auto_now_add=True, editable=False)
    updated_date = models.DateTimeField(null=True, auto_now=True, editable=False)

    class Meta:
        ordering = ['-request_no']
        unique_together = ('project', 'year', 'month')
        verbose_name = verbose_name_plural = u"案件請求情報"


class ProjectActivity(models.Model):
    project = models.ForeignKey(Project, verbose_name=u"案件")
    name = models.CharField(max_length=30, verbose_name=u"活動名称")
    open_date = models.DateTimeField(default=datetime.datetime.now(), verbose_name=u"開催日時")
    address = models.CharField(max_length=255, verbose_name=u"活動場所")
    content = models.TextField(verbose_name=u"活動内容")
    client_members = models.ManyToManyField(ClientMember, blank=True, verbose_name=u"参加しているお客様")
    members = models.ManyToManyField(Member, blank=True, verbose_name=u"参加している社員")
    salesperson = models.ManyToManyField(Salesperson, blank=True, verbose_name=u"参加している営業員")
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
    min_hours = models.DecimalField(max_digits=5, decimal_places=2, default=160, verbose_name=u"基準時間")
    max_hours = models.DecimalField(max_digits=5, decimal_places=2, default=180, verbose_name=u"最大時間")
    plus_per_hour = models.IntegerField(default=0, verbose_name=u"増（円）")
    minus_per_hour = models.IntegerField(default=0, verbose_name=u"減（円）")
    status = models.IntegerField(null=False, default=1,
                                 choices=constants.CHOICE_PROJECT_MEMBER_STATUS, verbose_name=u"ステータス")
    role = models.CharField(default="PG", max_length=2, choices=constants.CHOICE_PROJECT_ROLE, verbose_name=u"作業区分")
    stages = models.ManyToManyField(ProjectStage, blank=True, verbose_name=u"作業工程")
    is_deleted = models.BooleanField(default=False, editable=False, verbose_name=u"削除フラグ")
    deleted_date = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=u"削除年月日")

    objects = PublicManager(is_deleted=False, project__is_deleted=False, member__is_deleted=False)

    class Meta:
        verbose_name = verbose_name_plural = u"案件メンバー"

    def __unicode__(self):
        return self.member.__unicode__()

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

    # def delete(self, using=None):
    #     self.is_deleted = True
    #     self.deleted_date = datetime.datetime.now()
    #     self.save()


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

    # objects = PublicManager(is_deleted=False, project_member__is_deleted=False, category__is_deleted=False)

    class Meta:
        ordering = ['project_member', 'year', 'month']
        verbose_name = verbose_name_plural = u"清算リスト"

    def __unicode__(self):
        return u"%s %s %s" % (self.project_member, self.get_year_display(), self.get_month_display())

    # def delete(self, using=None):
    #     self.is_deleted = True
    #     self.deleted_date = datetime.datetime.now()
    #     self.save()


class MemberAttendance(models.Model):
    project_member = models.ForeignKey(ProjectMember, verbose_name=u"要員")
    year = models.CharField(max_length=4, default=str(datetime.date.today().year),
                            choices=constants.CHOICE_ATTENDANCE_YEAR, verbose_name=u"対象年")
    month = models.CharField(max_length=2, choices=constants.CHOICE_ATTENDANCE_MONTH, verbose_name=u"対象月")
    rate = models.DecimalField(max_digits=3, decimal_places=2, default=1, verbose_name=u"率")
    basic_price = models.IntegerField(default=0, editable=False, verbose_name=u"単価")
    total_hours = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=u"合計時間")
    extra_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name=u"残業時間")
    min_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0, editable=False, verbose_name=u"基準時間")
    max_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0, editable=False, verbose_name=u"最大時間")
    plus_per_hour = models.IntegerField(default=0, editable=False, verbose_name=u"増（円）")
    minus_per_hour = models.IntegerField(default=0, editable=False, verbose_name=u"減（円）")
    price = models.IntegerField(default=0, verbose_name=u"価格")
    comment = models.CharField(blank=True, null=True, max_length=50, verbose_name=u"備考")
    is_deleted = models.BooleanField(default=False, editable=False, verbose_name=u"削除フラグ")
    deleted_date = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=u"削除年月日")

    objects = PublicManager(is_deleted=False, project_member__is_deleted=False)

    class Meta:
        ordering = ['project_member', 'year', 'month']
        unique_together = ('project_member', 'year', 'month')
        verbose_name = verbose_name_plural = u"勤務時間"

    def __unicode__(self):
        return u"%s %s %s" % (self.project_member, self.get_year_display(), self.get_month_display())

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.pk is None:
            self.basic_price = self.project_member.price
            self.min_hours = self.project_member.min_hours
            self.max_hours = self.project_member.max_hours
            self.plus_per_hour = self.project_member.plus_per_hour
            self.minus_per_hour = self.project_member.minus_per_hour
        super(MemberAttendance, self).save(force_insert, force_update, using, update_fields)


class SubcontractorOrder(models.Model):
    subcontractor = models.ForeignKey(Subcontractor, verbose_name=u"協力会社")
    order_no = models.CharField(max_length=14, unique=True, verbose_name=u"注文番号")
    year = models.CharField(max_length=4, default=str(datetime.date.today().year),
                            choices=constants.CHOICE_ATTENDANCE_YEAR, verbose_name=u"対象年")
    month = models.CharField(max_length=2, choices=constants.CHOICE_ATTENDANCE_MONTH, verbose_name=u"対象月")
    created_date = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=u"追加日時")
    updated_date = models.DateTimeField(auto_now=True, editable=False, verbose_name=u"更新日時")
    is_deleted = models.BooleanField(default=False, editable=False, verbose_name=u"削除フラグ")
    deleted_date = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=u"削除日時")

    objects = PublicManager(is_deleted=False, subcontractor__is_deleted=False)

    def __unicode__(self):
        return self.order_no

    class Meta:
        unique_together = ('subcontractor', 'year', 'month')
        verbose_name = verbose_name_plural = u"ＢＰ註文書"

    def delete(self, using=None):
        self.is_deleted = True
        self.deleted_date = datetime.datetime.now()
        self.save()


class BpMemberOrderInfo(models.Model):
    member = models.ForeignKey(Member, verbose_name=u"協力社員")
    year = models.CharField(max_length=4, default=str(datetime.date.today().year),
                            choices=constants.CHOICE_ATTENDANCE_YEAR, verbose_name=u"対象年")
    month = models.CharField(max_length=2, choices=constants.CHOICE_ATTENDANCE_MONTH, verbose_name=u"対象月")
    min_hours = models.DecimalField(max_digits=5, decimal_places=2, default=160, verbose_name=u"基準時間")
    max_hours = models.DecimalField(max_digits=5, decimal_places=2, default=180, verbose_name=u"最大時間")
    plus_per_hour = models.IntegerField(default=0, verbose_name=u"増（円）")
    minus_per_hour = models.IntegerField(default=0, verbose_name=u"減（円）")
    cost = models.IntegerField(null=False, default=0, verbose_name=u"コスト")
    comment = models.CharField(blank=True, null=True, max_length=50, verbose_name=u"備考")
    is_deleted = models.BooleanField(default=False, editable=False, verbose_name=u"削除フラグ")
    deleted_date = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=u"削除年月日")

    objects = PublicManager(is_deleted=False, member__is_deleted=False)

    class Meta:
        unique_together = ('member', 'year', 'month')
        verbose_name = verbose_name_plural = u"協力社員の注文情報"

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

    objects = PublicManager(is_deleted=False, member__is_deleted=False)

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
    os = models.ManyToManyField(OS, blank=True, verbose_name=u"機種／OS")
    skill = models.ManyToManyField(Skill, blank=True, verbose_name=u"スキル要求")
    role = models.CharField(default="PG", max_length=2, choices=constants.CHOICE_PROJECT_ROLE, verbose_name=u"作業区分")
    stages = models.ManyToManyField(ProjectStage, blank=True, verbose_name=u"作業工程")
    is_deleted = models.BooleanField(default=False, editable=False, verbose_name=u"削除フラグ")
    deleted_date = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=u"削除年月日")

    objects = PublicManager(is_deleted=False, member__is_deleted=False)

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


class History(models.Model):
    start_datetime = models.DateTimeField(default=timezone.now, verbose_name=u"開始日時")
    end_datetime = models.DateTimeField(default=timezone.now, verbose_name=u"終了日時")
    location = models.CharField(max_length=2, choices=constants.CHOICE_DEV_LOCATION, verbose_name=u"作業場所")
    description = models.TextField(verbose_name=u"詳細")

    class Meta:
        ordering = ['-start_datetime']
        verbose_name = verbose_name_plural = u"開発履歴"

    def get_hours(self):
        td = self.end_datetime - self.start_datetime
        hours = td.seconds / 3600.0
        return round(hours, 1)


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
