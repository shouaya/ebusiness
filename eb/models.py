# coding: UTF-8
"""
Created on 2015/08/20

@author: Yang Wanjun
"""
import datetime
import re
import urllib2
import logging
import traceback
import mimetypes

from email import encoders
from email.header import Header
from xml.etree import ElementTree

from django.db import models, connection
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models import Max, Min, Q, Sum, Prefetch, Subquery, OuterRef
from django.utils import timezone
from django.utils.encoding import smart_str
from django.template import Context, Template
from django.core.mail import EmailMultiAlternatives, get_connection, SafeMIMEText
from django.core.mail.message import MIMEBase
from django.conf import settings
from django.core.validators import validate_comma_separated_integer_list
# from django.contrib.contenttypes.models import ContentType
# from django.contrib.contenttypes.fields import GenericForeignKey


from utils import common, constants


class AbstractCompany(models.Model):
    name = models.CharField(blank=False, null=False, unique=True, max_length=30, verbose_name=u"会社名")
    japanese_spell = models.CharField(blank=True, null=True, max_length=30, verbose_name=u"フリカナ")
    president = models.CharField(blank=True, null=True, max_length=30, verbose_name=u"代表者名")
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
    email = models.EmailField(blank=True, null=True, verbose_name=u"会社メールアドレス")
    private_email = models.EmailField(blank=True, null=True, verbose_name=u"個人メールアドレス")
    post_code = models.CharField(blank=True, null=True, max_length=7, verbose_name=u"郵便番号",
                                 help_text=u"数値だけを入力してください、例：1230034")
    address1 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"住所１")
    address2 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"住所２")
    lat = models.CharField(blank=True, null=True, max_length=25, verbose_name=u"緯度")
    lng = models.CharField(blank=True, null=True, max_length=25, verbose_name=u"経度")
    coordinate_update_date = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=u"座標更新日時")
    nearest_station = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"最寄駅")
    years_in_japan = models.IntegerField(blank=True, null=True, verbose_name=u"在日年数")
    phone = models.CharField(blank=True, null=True, max_length=11, verbose_name=u"電話番号",
                             help_text=u"数値だけを入力してください、例：08012345678")
    is_married = models.CharField(blank=True, null=True, max_length=1,
                                  choices=constants.CHOICE_MARRIED, verbose_name=u"婚姻状況")
    company = models.ForeignKey('Company', blank=True, null=True, on_delete=models.PROTECT, verbose_name=u"会社")
    japanese_description = models.TextField(blank=True, null=True, verbose_name=u"日本語能力の説明")
    certificate = models.TextField(blank=True, null=True, verbose_name=u"資格の説明")
    skill_description = models.TextField(blank=True, null=True, verbose_name=u"得意")
    comment = models.TextField(blank=True, null=True, verbose_name=u"備考")
    notify_type = models.IntegerField(default=1, choices=constants.CHOICE_NOTIFY_TYPE, verbose_name=u"通知種類",
                                      help_text=u"メール通知時に利用する。EBのメールアドレスを設定すると、"
                                                u"通知のメールはEBのアドレスに送信する")
    is_retired = models.BooleanField(blank=False, null=False, default=False, verbose_name=u"退職")
    retired_date = models.DateField(blank=True, null=True, verbose_name=u"退職年月日")
    id_from_api = models.CharField(blank=True, null=True, unique=True, max_length=30,
                                   verbose_name=u"社員ID", help_text=u"データを導入するために、API側のID")
    eboa_user_id = models.CharField(blank=True, null=True, max_length=14, unique=True)
    created_date = models.DateTimeField(null=True, auto_now_add=True, editable=False, verbose_name=u"作成日時")
    updated_date = models.DateTimeField(null=True, auto_now=True, editable=False, verbose_name=u"更新日時")

    class Meta:
        abstract = True

    def get_notify_mail_list(self):
        if self.notify_type == 1:
            if self.email:
                return [self.email]
        elif self.notify_type == 2:
            if self.private_email:
                return [self.private_email]
        elif self.notify_type == 3:
            if self.email and self.private_email:
                return [self.email, self.private_email]
            elif self.email:
                return [self.email]
            elif self.private_email:
                return [self.private_email]
        return []


class PublicManager(models.Manager):

    # use_for_related_fields = True

    def __init__(self, *args, **kwargs):
        super(PublicManager, self).__init__()
        self.args = args
        self.kwargs = kwargs

    def get_queryset(self):
        return super(PublicManager, self).get_queryset().filter(is_deleted=False)

    def public_all(self):
        return self.get_queryset().filter(*self.args, **self.kwargs)

    def public_filter(self, *args, **kwargs):
        return self.public_all().filter(*args, **kwargs)


class Config(models.Model):
    group = models.CharField(max_length=50, blank=False, null=True, verbose_name=u"グループ")
    name = models.CharField(max_length=50, unique=True, verbose_name=u"設定名")
    value = models.CharField(max_length=2000, verbose_name=u"設定値")
    description = models.TextField(blank=True, null=True, verbose_name=u"説明")

    class Meta:
        ordering = ['group', 'name']
        verbose_name = verbose_name_plural = u"設定"
        db_table = 'mst_config'

    def __unicode__(self):
        return self.name

    @staticmethod
    def get(config_name, default_value=None, group_name=None):
        """システム設定を取得する。

        DBから値を取得する。

        :param config_name: 設定名
        :param default_value: デフォルト値
        :param group_name: グループ名
        :return:
        """
        try:
            c = Config.objects.get(name=config_name)
            return c.value
        except ObjectDoesNotExist:
            if default_value is not None:
                c = Config(group=group_name, name=config_name, value=default_value)
                c.save()
            return default_value

    @staticmethod
    def get_employment_period_comment():
        """社員の雇用期間コメントを取得する。

        :return:
        """
        default = u"（期間満了の１ヶ月前までに双方にいずれからも別段の意志表示がないときは、" \
                  u"同一条件をもってさらに３ヶ月継続するものとし、その後も同じとする。） "
        return Config.get(constants.CONFIG_EMPLOYMENT_PERIOD_COMMENT, default,
                          group_name=constants.CONFIG_GROUP_CONTRACT)

    @staticmethod
    def get_business_address():
        """就業の場所

        :return:
        """
        default = u"就業の場所（当社社内および雇用者が指定した場所）"
        return Config.get(constants.CONFIG_BUSINESS_ADDRESS, default, group_name=constants.CONFIG_GROUP_CONTRACT)

    @staticmethod
    def get_business_time():
        default = u"始業および終業時刻　午前　9時30分　～　午後　6時30分\n" \
                  u"休憩時間　　　　　　　正午～午後1時\n" \
                  u"就業時間の変更　　前記にかかわらず業務の都合または就業場所変更により\n" \
                  u"　　　　　　　　　　　　　始業および終業時刻の変更を行うことがある。\n" \
                  u"所定労働時間を越える労働の有無　有"
        return Config.get(constants.CONFIG_BUSINESS_TIME, default, group_name=constants.CONFIG_GROUP_CONTRACT)

    @staticmethod
    def get_business_other():
        default = u"就業の場所および業務の種類は、業務の都合により変更することがある。\n" \
                  u"出向、転勤、配置転換等の業務命令が発令されることがある。"
        return Config.get(constants.CONFIG_BUSINESS_OTHER, default, group_name=constants.CONFIG_GROUP_CONTRACT)

    @staticmethod
    def get_allowance_date_comment():
        """給与締め切り日及び支払日のコメントを取得する。

        :return:
        """
        default = u"1、締切日および支払日：毎月末日〆、翌月末日払\n" \
                  u"2、支払時の控除：所得税、雇用保険"
        return Config.get(constants.CONFIG_ALLOWANCE_DATE_COMMENT, default, group_name=constants.CONFIG_GROUP_CONTRACT)

    @staticmethod
    def get_allowance_change_comment():
        """昇給及び降給のコメントを取得する。

        :return:
        """
        default = u"会社の業績および社員個人の業績その他の状況を勘案し、昇給または降給を行うことがある。"
        return Config.get(constants.CONFIG_ALLOWANCE_CHANGE_COMMENT, default,
                          group_name=constants.CONFIG_GROUP_CONTRACT)

    @staticmethod
    def get_bonus_comment():
        default = u"賞与支給要件を満たした者に対し、賞与が年2回、計2ヵ月分。\n" \
                  u"ただし会社業績、本人業績、勤怠状況および将来への期待度により、変更の可能性がある。"
        return Config.get(constants.CONFIG_BONUS_COMMENT, default, group_name=constants.CONFIG_GROUP_CONTRACT)

    @staticmethod
    def get_holiday_comment():
        default = u"週休2日制（土・日・祝祭日休み）"
        return Config.get(constants.CONFIG_HOLIDAY_COMMENT, default, group_name=constants.CONFIG_GROUP_CONTRACT)

    @staticmethod
    def get_paid_vacation_comment():
        default = u"年次有給休暇：労働基準法の定めによる。"
        return Config.get(constants.CONFIG_PAID_VACATION_COMMENT, default, group_name=constants.CONFIG_GROUP_CONTRACT)

    @staticmethod
    def get_no_paid_vacation_comment():
        default = u"産前産後、育児・介護休業、生理休暇、その他就業規則に定めがあるときは当該休暇。"
        return Config.get(constants.CONFIG_NO_PAID_VACATION_COMMENT, default,
                          group_name=constants.CONFIG_GROUP_CONTRACT)

    @staticmethod
    def get_retire_comment():
        default = u"1、就業期間中、業務能力が著しく劣り、又は業務実績が著しく不良のとき、" \
                  u"会社の業務命令が従わないとき、減給、降職又は諭旨解雇とする。\n" \
                  u"2、自己都合退職の際は退職する30日前までに届け出ること。\n" \
                  u"3、解雇の事由および手続きは、就業規則の定めるところによる。"
        return Config.get(constants.CONFIG_RETIRE_COMMENT, default, group_name=constants.CONFIG_GROUP_CONTRACT)

    @staticmethod
    def get_contract_comment():
        default = u"上記以外の雇用条件については、就業規則の定めることによる。"
        return Config.get(constants.CONFIG_CONTRACT_COMMENT, default, group_name=constants.CONFIG_GROUP_CONTRACT)

    @staticmethod
    def get_bp_order_delivery_properties():
        """ＢＰ注文書の納入物件

        :return:
        """
        return Config.get(constants.CONFIG_BP_ORDER_DELIVERY_PROPERTIES, '', group_name=constants.CONFIG_GROUP_BP_ORDER)

    @staticmethod
    def get_bp_order_payment_condition():
        """ＢＰ注文書の支払条件

        :return:
        """
        return Config.get(constants.CONFIG_BP_ORDER_PAYMENT_CONDITION, '', group_name=constants.CONFIG_GROUP_BP_ORDER)

    @staticmethod
    def get_bp_order_contract_items():
        """ＢＰ注文書の契約条項

        :return:
        """
        return Config.get(constants.CONFIG_BP_ORDER_CONTRACT_ITEMS, '', group_name=constants.CONFIG_GROUP_BP_ORDER)

    @staticmethod
    def get_default_expenses_category():
        """出勤情報アップロード時、客先立替金を精算リストに追加するために、既定の分類を取得する

        :return:
        """
        expenses_id = Config.get(constants.CONFIG_DEFAULT_EXPENSES_ID)
        if expenses_id:
            try:
                expenses = ExpensesCategory.objects.get(pk=expenses_id)
            except (ObjectDoesNotExist, MultipleObjectsReturned):
                expenses = None
            return expenses
        else:
            return None

    @staticmethod
    def get_firebase_serverkey():
        return Config.get(constants.CONFIG_FIREBASE_SERVERKEY, '', group_name=constants.CONFIG_GROUP_SYSTEM)

    @staticmethod
    def get_gcm_url():
        return Config.get(constants.CONFIG_GCM_URL, 'https://fcm.googleapis.com/fcm/send',
                          group_name=constants.CONFIG_GROUP_SYSTEM)

    @staticmethod
    def get_bp_attendance_type():
        return Config.get(constants.CONFIG_BP_ATTENDANCE_TYPE, '2', group_name=constants.CONFIG_GROUP_SYSTEM)


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, auto_now=False, null=True, editable=False,
                                        verbose_name=u"作成日時")
    updated_date = models.DateTimeField(auto_now=True, null=True, editable=False, verbose_name=u"更新日時")
    is_deleted = models.BooleanField(default=False, editable=False, verbose_name=u"削除フラグ")
    deleted_date = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=u"削除年月日")

    objects = PublicManager(is_deleted=False)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_date = datetime.datetime.now()
        self.save()


class Company(AbstractCompany):
    payment_month = models.CharField(blank=True, null=True, max_length=1, default='1',
                                     choices=constants.CHOICE_PAYMENT_MONTH, verbose_name=u"支払いサイト",)
    payment_day = models.CharField(blank=True, null=True, max_length=2, default='99',
                                   choices=constants.CHOICE_PAYMENT_DAY, verbose_name=u"支払日")
    tax_rate = models.DecimalField(default=0.08, max_digits=3, decimal_places=2, choices=constants.CHOICE_TAX_RATE,
                                   verbose_name=u"税率")
    decimal_type = models.CharField(max_length=1, default='0', choices=constants.CHOICE_DECIMAL_TYPE,
                                    verbose_name=u"小数の処理区分")
    quotation_file = models.FileField(blank=True, null=True, upload_to="./quotation",
                                      verbose_name=u"見積書テンプレート")
    request_file = models.FileField(blank=True, null=True, upload_to="./request", verbose_name=u"請求書テンプレート")
    request_lump_file = models.FileField(blank=True, null=True, upload_to="./request",
                                         verbose_name=u"請求書テンプレート(一括)")
    order_file = models.FileField(blank=True, null=True, upload_to="./eb_order", verbose_name=u"註文書テンプレート",
                                  help_text=u"協力会社への註文書。")

    class Meta:
        verbose_name = verbose_name_plural = u"会社"
        permissions = (
            ('view_member_status_list', u"社員稼働状況リスト"),
            ('view_batch', u"バッチ参照"),
            ('execute_batch', u"バッチ実行"),
        )

    @staticmethod
    def get_projects(status=0):
        """ステータスによって、該当する全ての案件を取得する。

        :param status:
        :return:
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

    def get_pay_date(self, date=datetime.date.today()):
        """支払い期限日を取得する。

        :param date:
        :return:
        """
        months = int(self.payment_month) if self.payment_month else 1
        pay_month = common.add_months(date, months)
        if self.payment_day == '99' or not self.payment_day:
            return common.get_last_day_by_month(pay_month)
        else:
            pay_day = int(self.payment_day)
            last_day = common.get_last_day_by_month(pay_month)
            if last_day.day < pay_day:
                return last_day
            return datetime.date(pay_month.year, pay_month.month, pay_day)


class BankInfo(BaseModel):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, verbose_name=u"会社")
    bank_name = models.CharField(blank=False, null=False, max_length=20, verbose_name=u"銀行名称")
    branch_no = models.CharField(blank=False, null=False, max_length=3, verbose_name=u"支店番号")
    branch_name = models.CharField(blank=False, null=False, max_length=20, verbose_name=u"支店名称")
    account_type = models.CharField(blank=False, null=False, max_length=1, choices=constants.CHOICE_ACCOUNT_TYPE,
                                    verbose_name=u"預金種類")
    account_number = models.CharField(blank=False, null=False, max_length=7, verbose_name=u"口座番号")
    account_holder = models.CharField(blank=True, null=True, max_length=20, verbose_name=u"口座名義")

    class Meta:
        unique_together = ('branch_no', 'account_number')
        verbose_name = verbose_name_plural = u"銀行口座"

    def __unicode__(self):
        return self.bank_name


class Subcontractor(AbstractCompany):
    employee_count = models.IntegerField(blank=True, null=True, verbose_name=u"従業員数")
    sale_amount = models.BigIntegerField(blank=True, null=True, verbose_name=u"売上高")
    payment_month = models.CharField(blank=True, null=True, max_length=1, default='1',
                                     choices=constants.CHOICE_PAYMENT_MONTH, verbose_name=u"支払いサイト")
    payment_day = models.CharField(blank=True, null=True, max_length=2, choices=constants.CHOICE_PAYMENT_DAY,
                                   default='99', verbose_name=u"支払日")
    middleman = models.CharField(blank=True, null=True, max_length=30, verbose_name=u"連絡窓口担当者")
    comment = models.TextField(blank=True, null=True, verbose_name=u"備考")
    is_deleted = models.BooleanField(default=False, editable=False, verbose_name=u"削除フラグ")
    deleted_date = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=u"削除年月日")

    objects = PublicManager(is_deleted=False)

    class Meta:
        ordering = ['name']
        verbose_name = verbose_name_plural = u"協力会社"
        permissions = (
            ('view_subcontractor', u'協力会社参照'),
        )

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
        members = self.member_set.filter(
            projectmember__start_date__lte=last_day,
            projectmember__end_date__gte=first_day
        ).distinct()
        return members

    def get_year_month_order_finished(self):
        """
        月単位の註文情報を取得する。
        :return:
        """
        ret_value = []
        for year, month in common.get_year_month_list(self.get_start_date(), self.get_end_date()):
            first_day = datetime.date(int(year), int(month), 1)
            subcontractor_order = None
            members = self.get_members_by_month(first_day)
            bp_members = BpMemberOrderInfo.objects.public_filter(member__in=members, year=year, month=month)
            if members.count() > 0 and members.count() == bp_members.count():
                is_finished = True
            else:
                is_finished = False
            ret_value.append((year, month, subcontractor_order, is_finished))
        return ret_value

    def get_request_sections(self, year, month):
        """協力会社の請求書は事業部単位で作成されているので、指定年月の各部署を取得する
        
        :param year: 
        :param month: 
        :return: 
        """
        first_day = datetime.date(int(year), int(month), 1)
        members = self.get_members_by_month(first_day)
        organizations = []
        ret_list = []
        for member in members:
            section = member.get_section(first_day)
            division = section.get_root_section()
            if division not in organizations:
                try:
                    subcontractor_request = SubcontractorRequest.objects.get(
                        subcontractor=self,
                        section=division,
                        year=year,
                        month=month
                    )
                except (ObjectDoesNotExist, MultipleObjectsReturned):
                    subcontractor_request = None
                organizations.append(division)
                ret_list.append((division, subcontractor_request))
        return ret_list

    def get_members_by_month_and_section(self, year, month, section):
        """協力会社の請求書を作成時に、部署単位でメンバーを取得し、作成する。
        
        :param year: 
        :param month: 
        :param section: 
        :return: 
        """
        first_day = datetime.date(int(year), int(month), 1)
        attendance_set = MemberAttendance.objects.public_filter(
            year=year, month=month
        )
        members = self.get_members_by_month(first_day)
        section_pk_list = [s.pk for s in section.get_children()]
        section_pk_list.append(section.pk)
        ret_list = []
        for member in members:
            section = member.get_section(first_day)
            if section.pk in section_pk_list:
                ret_list.append(member)
        return ret_list

    def get_subcontractor_request(self, year, month, organization):
        """指定年月と事業部の請求書を取得する、存在しない場合は新規作成する。
        
        :param year: 
        :param month: 
        :param organization: 
        :return: 
        """
        organizations = organization.get_children()
        organizations.append(organization)
        request_list = SubcontractorRequest.objects.filter(
            subcontractor=self, year=year, month=month, section__in=organizations
        )
        if request_list.count() == 0:
            # 指定年月と事業部の請求書がない場合、請求番号を発行する。
            max_request_no = SubcontractorRequest.objects.filter(year=year, month=month).aggregate(Max('request_no'))
            request_no = max_request_no.get('request_no__max')
            if request_no and re.match(r"^([0-9]{7}|[0-9]{7}-[0-9]{3})$", request_no):
                no = request_no[4:7]
                no = "%03d" % (int(no) + 1,)
                next_request = "%s%s%s" % (year[2:], month, no)
            else:
                next_request = "%s%s%s" % (year[2:], month, "001")
            subcontractor_request = SubcontractorRequest(
                subcontractor=self, section=organization, year=year, month=month, request_no=next_request
            )
            return subcontractor_request
        else:
            # 存在する場合、そのまま使う、再発行はしません。
            return request_list[0]

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_date = datetime.datetime.now()
        self.save()


class SubcontractorBankInfo(BaseModel):
    subcontractor = models.ForeignKey(Subcontractor, on_delete=models.PROTECT, verbose_name=u"協力会社")
    bank_name = models.CharField(blank=False, null=False, max_length=20, verbose_name=u"銀行名称")
    branch_no = models.CharField(blank=False, null=False, max_length=3, verbose_name=u"支店番号")
    branch_name = models.CharField(blank=False, null=False, max_length=20, verbose_name=u"支店名称")
    account_type = models.CharField(blank=False, null=False, max_length=1, choices=constants.CHOICE_ACCOUNT_TYPE,
                                    verbose_name=u"預金種類")
    account_number = models.CharField(blank=False, null=False, max_length=7, verbose_name=u"口座番号")
    account_holder = models.CharField(blank=True, null=True, max_length=20, verbose_name=u"口座名義")

    class Meta:
        unique_together = ('branch_no', 'account_number')
        verbose_name = verbose_name_plural = u"協力会社銀行口座"

    def __unicode__(self):
        return self.bank_name


class SubcontractorMember(BaseModel):
    name = models.CharField(max_length=30, verbose_name=u"名前")
    email = models.EmailField(blank=False, null=True, verbose_name=u"メールアドレス")
    phone = models.CharField(blank=True, null=True, max_length=11, verbose_name=u"電話番号")
    member_type = models.CharField(max_length=2, choices=constants.CHOICE_CLIENT_MEMBER_TYPE, verbose_name=u"役割担当")
    subcontractor = models.ForeignKey(Subcontractor, on_delete=models.PROTECT, verbose_name=u"所属会社")

    class Meta:
        ordering = ['name']
        unique_together = ('name', 'subcontractor')
        verbose_name = verbose_name_plural = u"協力会社社員"

    def __unicode__(self):
        return "%s - %s" % (self.subcontractor.name, self.name)


class MailTemplate(BaseModel):
    mail_title = models.CharField(max_length=50, verbose_name=u"送信メールのタイトル")
    mail_body = models.TextField(blank=True, null=True, verbose_name=u"メール本文(Plain Text)")
    mail_html = models.TextField(blank=True, null=True, verbose_name=u"メール本文(HTML)")
    attachment1 = models.FileField(blank=True, null=True, upload_to="./attachment", verbose_name=u"添付ファイル１",
                                   help_text=u"メール送信時の添付ファイルその１。")
    attachment2 = models.FileField(blank=True, null=True, upload_to="./attachment", verbose_name=u"添付ファイル２",
                                   help_text=u"メール送信時の添付ファイルその２。")
    attachment3 = models.FileField(blank=True, null=True, upload_to="./attachment", verbose_name=u"添付ファイル３",
                                   help_text=u"メール送信時の添付ファイルその３。")
    description = models.TextField(blank=True, null=True, verbose_name=u"説明")

    class Meta:
        ordering = ['mail_title']
        verbose_name = verbose_name_plural = u"メールテンプレート"

    def __unicode__(self):
        return self.mail_title


class MailGroup(BaseModel):
    name = models.CharField(max_length=30, unique=True, verbose_name=u"名称")
    mail_template = models.ForeignKey(MailTemplate, blank=True, null=True, on_delete=models.PROTECT,
                                      verbose_name=u"メールテンプレート")

    class Meta:
        ordering = ['name']
        verbose_name = verbose_name_plural = u"メールグループ"

    def __unicode__(self):
        return self.name


class MailList(BaseModel):
    group = models.ForeignKey(MailGroup, on_delete=models.PROTECT, verbose_name=u"メールグループ")
    member = models.ForeignKey(SubcontractorMember, on_delete=models.PROTECT, verbose_name=u"メンバー")

    class Meta:
        ordering = ['group']
        unique_together = ('group', 'member')
        verbose_name = verbose_name_plural = u"メールリスト"

    def __unicode__(self):
        return unicode(self.member)


class Section(BaseModel):
    name = models.CharField(blank=False, null=False, max_length=30, verbose_name=u"部署名")
    description = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"概要")
    is_on_sales = models.BooleanField(blank=False, null=False, default=False, verbose_name=u"営業対象")
    parent = models.ForeignKey("self", related_name='children', blank=True, null=True, on_delete=models.PROTECT,
                               verbose_name=u"親組織")
    org_type = models.CharField(blank=False, null=False, max_length=2, choices=constants.CHOICE_ORG_TYPE,
                                verbose_name=u"組織類別")
    company = models.ForeignKey(Company, blank=False, null=False, on_delete=models.PROTECT, verbose_name=u"会社")

    class Meta:
        ordering = ['name']
        verbose_name = verbose_name_plural = u"部署"

    def __unicode__(self):
        return self.name

    def get_attendance_amount(self, ym):
        """対象年月の出勤売上を取得する。

        :param ym: 対象年月
        :return:
        """
        amount = MemberAttendance.objects.public_filter(year=ym[:4], month=ym[4:],
                                                        project_member__member__section=self)\
            .aggregate(amount=Sum('price'))
        return amount.get('amount', 0) if amount.get('amount', 0) else 0

    def get_expenses_amount(self, ym):
        amount = MemberExpenses.objects.public_filter(year=ym[:4], month=ym[4:],
                                                      project_member__member__section=self)\
            .aggregate(amount=Sum('price'))
        return amount.get('amount', 0) if amount.get('amount', 0) else 0

    def get_cost_amount(self, ym):
        pass

    def get_chief(self):
        """部門長、課長を取得する

        :return:
        """
        query_set = Member.objects.public_filter(positionship__section=self,
                                                 positionship__position__in=[3, 4, 6])
        return query_set

    def get_chief2(self):
        """担当部長、担当課長を取得する

        :return:
        """
        query_set = Member.objects.public_filter(positionship__section=self,
                                                 positionship__position__in=[5, 7])
        return query_set

    def get_attendance_statistician(self):
        """勤務情報の統計者を取得する。

        :return:
        """
        query_set = Member.objects.public_filter(positionship__section=self,
                                                 positionship__position=11)
        return query_set

    def get_children(self):
        children = []
        for org in self.children.filter(is_deleted=False):
            children.append(org)
            children.extend(list(org.get_children()))
        return children

    def get_root_section(self):
        """事業部を取得する。
        
        :return: 
        """
        if self.parent:
            return self.parent.get_root_section()
        else:
            return self

    def get_members_period(self):
        """当該部署に所属メンバーを取得する、子部署も含む。

        :return:
        """
        today = timezone.now().date()
        all_children = self.get_children()
        org_pk_list = [org.pk for org in all_children]
        org_pk_list.append(self.pk)
        projectmember_set = ProjectMember.objects.filter(start_date__lte=today,
                                                         end_date__gte=today)
        org_period_list = MemberSectionPeriod.objects.filter(
            Q(division__in=org_pk_list) |
            Q(section__in=org_pk_list) |
            Q(subsection__in=org_pk_list),
            Q(end_date__gte=today) | Q(end_date__isnull=True),
            start_date__lte=today,
            member__is_retired=False,
            member__is_deleted=False
        ).select_related('member').prefetch_related(
            Prefetch('member__projectmember_set', queryset=projectmember_set, to_attr='current_projectmember_set'),
        )
        return org_period_list


class SalesOffReason(BaseModel):
    name = models.CharField(blank=False, null=False, max_length=50, verbose_name=u"理由")

    class Meta:
        verbose_name = verbose_name_plural = u"営業対象外理由"
        db_table = 'mst_salesofreason'

    def __unicode__(self):
        return self.name


class Salesperson(AbstractMember):

    user = models.OneToOneField(User, blank=True, null=True)
    section = models.ForeignKey('Section', blank=False, null=True, on_delete=models.PROTECT, verbose_name=u"部署")
    member_type = models.IntegerField(default=5, choices=constants.CHOICE_SALESPERSON_TYPE, verbose_name=u"社員区分")
    is_deleted = models.BooleanField(default=False, editable=False, verbose_name=u"削除フラグ")
    deleted_date = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=u"削除年月日")

    objects = PublicManager(is_deleted=False, is_retired=False, section__is_deleted=False)

    class Meta:
        ordering = ['first_name', 'last_name']
        verbose_name = verbose_name_plural = u"営業員"

    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)

    def get_on_sales_members(self):
        """該当営業員の営業対象のメンバーを取得する

        :return: MemberのQueryset
        """
        today = datetime.date.today()
        members = get_on_sales_members().filter((Q(membersalespersonperiod__start_date__lte=today) &
                                                 Q(membersalespersonperiod__end_date__isnull=True)) |
                                                (Q(membersalespersonperiod__start_date__lte=today) &
                                                 Q(membersalespersonperiod__end_date__gte=today)),
                                                membersalespersonperiod__is_deleted=False,
                                                membersalespersonperiod__salesperson=self)
        return members

    def get_off_sales_members(self):
        """該当営業員の営業対象のメンバーを取得する

        :return: MemberのQueryset
        """
        today = datetime.date.today()
        members = get_off_sales_members().filter((Q(membersalespersonperiod__start_date__lte=today) &
                                                  Q(membersalespersonperiod__end_date__isnull=True)) |
                                                 (Q(membersalespersonperiod__start_date__lte=today) &
                                                  Q(membersalespersonperiod__end_date__gte=today)),
                                                 membersalespersonperiod__is_deleted=False,
                                                 membersalespersonperiod__salesperson=self)
        return members

    def get_working_members(self):
        """現在稼働中のメンバーを取得する

        :return: MemberのQueryset
        """
        today = datetime.date.today()
        members = get_working_members().filter((Q(membersalespersonperiod__start_date__lte=today) &
                                                Q(membersalespersonperiod__end_date__isnull=True)) |
                                               (Q(membersalespersonperiod__start_date__lte=today) &
                                                Q(membersalespersonperiod__end_date__gte=today)),
                                               membersalespersonperiod__is_deleted=False,
                                               membersalespersonperiod__salesperson=self)
        return members

    def get_waiting_members(self):
        """現在待機中のメンバーを取得する

        :return: MemberのQueryset
        """
        today = datetime.date.today()
        members = get_waiting_members().filter((Q(membersalespersonperiod__start_date__lte=today) &
                                                Q(membersalespersonperiod__end_date__isnull=True)) |
                                               (Q(membersalespersonperiod__start_date__lte=today) &
                                                Q(membersalespersonperiod__end_date__gte=today)),
                                               membersalespersonperiod__is_deleted=False,
                                               membersalespersonperiod__salesperson=self)
        return members

    def get_release_current_month(self):
        """今月にリリースするメンバーを取得する

        :return: ProjectMemberのQueryset
        """
        today = datetime.date.today()
        project_members = get_release_current_month()
        query_set = project_members.filter((Q(member__membersalespersonperiod__start_date__lte=today) &
                                            Q(member__membersalespersonperiod__end_date__isnull=True)) |
                                           (Q(member__membersalespersonperiod__start_date__lte=today) &
                                            Q(member__membersalespersonperiod__end_date__gte=today)),
                                           member__membersalespersonperiod__is_deleted=False,
                                           member__membersalespersonperiod__salesperson=self)
        return query_set

    def get_release_next_month(self):
        """来月にリリースするメンバーを取得する

        :return: ProjectMemberのQueryset
        """
        today = datetime.date.today()
        project_members = get_release_next_month()
        query_set = project_members.filter((Q(member__membersalespersonperiod__start_date__lte=today) &
                                            Q(member__membersalespersonperiod__end_date__isnull=True)) |
                                           (Q(member__membersalespersonperiod__start_date__lte=today) &
                                            Q(member__membersalespersonperiod__end_date__gte=today)),
                                           member__membersalespersonperiod__is_deleted=False,
                                           member__membersalespersonperiod__salesperson=self)
        return query_set

    def get_release_next_2_month(self):
        """再来月にリリースするメンバーを取得する

        :return: ProjectMemberのQueryset
        """
        today = datetime.date.today()
        project_members = get_release_next_2_month()
        query_set = project_members.filter((Q(member__membersalespersonperiod__start_date__lte=today) &
                                            Q(member__membersalespersonperiod__end_date__isnull=True)) |
                                           (Q(member__membersalespersonperiod__start_date__lte=today) &
                                            Q(member__membersalespersonperiod__end_date__gte=today)),
                                           member__membersalespersonperiod__is_deleted=False,
                                           member__membersalespersonperiod__salesperson=self)
        return query_set

    def get_warning_projects(self):
        today = datetime.date.today()
        query_set = self.project_set.filter(status=4).extra(select={
            'num_working': "select count(*) "
                           "  from eb_projectmember pm "
                           " where pm.project_id = eb_project.id "
                           "   and pm.start_date <= '%s' "
                           "   and pm.end_date >= '%s' " % (today, today)
        })
        return query_set

    def get_under_salesperson(self):
        """部下の営業員を取得する、部下がない場合自分を返す。
        """
        if self.member_type == 0 and self.section:
            return self.section.salesperson_set.public_all()
        else:
            return [self]

    def get_attendance_amount(self, ym):
        """対象年月の出勤売上を取得する。

        :param ym: 対象年月
        :return:
        """
        amount = MemberAttendance.objects.public_filter(year=ym[:4], month=ym[4:],
                                                        project_member__member__salesperson=self)\
            .aggregate(amount=Sum('price'))
        return amount.get('amount', 0) if amount.get('amount', 0) else 0

    def get_expenses_amount(self, ym):
        amount = MemberExpenses.objects.public_filter(year=ym[:4], month=ym[4:],
                                                      project_member__member__salesperson=self)\
            .aggregate(amount=Sum('price'))
        return amount.get('amount', 0) if amount.get('amount', 0) else 0

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_date = datetime.datetime.now()
        self.save()


class Member(AbstractMember):
    user = models.OneToOneField(User, blank=True, null=True)
    member_type = models.IntegerField(default=0, choices=constants.CHOICE_MEMBER_TYPE, verbose_name=u"社員区分")
    section = models.ForeignKey('Section', blank=True, null=True, verbose_name=u"部署", on_delete=models.PROTECT,
                                help_text=u"開発メンバーなど営業必要な方はしたの「社員の部署期間」のほうで設定してください、"
                                          u"ここで設定できるのは管理部、総務部などの営業対象外のかたです。")
    ranking = models.CharField(blank=True, null=True, max_length=2, choices=constants.CHOICE_MEMBER_RANK,
                               verbose_name=u"ランク")
    salesperson = models.ForeignKey(Salesperson, blank=True, null=True, on_delete=models.PROTECT, verbose_name=u"営業員")
    is_individual_pay = models.BooleanField(default=False, verbose_name=u"個別精算")
    subcontractor = models.ForeignKey(Subcontractor, blank=True, null=True, on_delete=models.PROTECT,
                                      verbose_name=u"協力会社")
    is_on_sales = models.BooleanField(blank=False, null=False, default=True, verbose_name=u"営業対象")
    is_unofficial = models.BooleanField(default=False, verbose_name=u"内定")
    sales_off_reason = models.ForeignKey(SalesOffReason, blank=True, null=True, on_delete=models.PROTECT,
                                         verbose_name=u"営業対象外理由")
    cost = models.IntegerField(null=False, default=0, verbose_name=u"コスト")
    is_deleted = models.BooleanField(default=False, editable=False, verbose_name=u"削除フラグ")
    deleted_date = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=u"削除年月日")

    objects = PublicManager(is_deleted=False, is_retired=False)

    class Meta:
        ordering = ['first_name', 'last_name']
        verbose_name = verbose_name_plural = u"社員"
        permissions = (
            ('view_member', u'社員参照'),
            ('view_member_cost', u"社員コスト参照"),
            ('view_bp_cost', u"ＢＰコスト参照"),
        )

    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)

    def is_deletable(self):
        # get all the related object
        for rel in self._meta.get_fields():
            try:
                # check if there is a relationship with at least one related object
                related = rel.related_model.objects.filter(**{rel.field.name: self})
                if related.exists():
                    # if there is return a Tuple of flag = False the related_model object
                    return False, related
            except AttributeError:  # an attribute error for field occurs when checking for AutoField
                pass  # just pass as we dont need to check for AutoField
        return True, None

    def get_resume_name(self):
        """履歴書の氏名を取得する。

        :return: 名(ローマ字)が定義すれば、その頭文字を取得し、姓と一緒に返す。
        """
        if self.last_name_en:
            lst = re.findall(r"[A-Z]", str(self.last_name_en))
            last_name = "".join(lst)
        else:
            last_name = self.last_name
        return u"%s %s" % (self.first_name, last_name)

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

    def get_section(self, date=None):
        """部署を取得する。

        :param date:
        :return:
        """
        if not date:
            date = datetime.date.today()
        results = self.membersectionperiod_set.filter((Q(start_date__lte=date) & Q(end_date__isnull=True)) |
                                                      (Q(start_date__lte=date) & Q(end_date__gte=date)))
        if results.count() > 0:
            return results[0].subsection or results[0].section or results[0].division
        return self.section

    def get_salesperson(self, date=None):
        """営業員を取得する。

        :param date:
        :return:
        """
        if not date:
            date = datetime.date.today()
        results = self.membersalespersonperiod_set.filter((Q(start_date__lte=date) & Q(end_date__isnull=True)) |
                                                          (Q(start_date__lte=date) & Q(end_date__gte=date)),
                                                          is_deleted=False)
        if results.count() > 0:
            return results[0].salesperson
        return None

    def get_current_project_member(self):
        """現在実施中の案件アサイン情報を取得する
        """
        now = datetime.datetime.now()
        projects = self.projectmember_set.public_filter(end_date__gte=now, start_date__lte=now,
                                                        status=2, is_deleted=False)
        if projects.count() > 0:
            return projects[0]
        else:
            return None

    def get_current_end_project_member(self):
        """今月リリースのアサイン情報を取得する。

        :return:
        """
        first_day = common.get_first_day_current_month()
        last_day = common.get_last_day_by_month(first_day)
        project_members = self.projectmember_set.public_filter(end_date__gte=first_day,
                                                               end_date__lte=last_day,
                                                               status=2,
                                                               is_deleted=False)
        return project_members[0] if project_members.count() > 0 else None

    def get_next_start_project_member(self):
        """来月からのアサイン情報を取得する。

        :return:
        """
        next_month = common.add_months(datetime.date.today(), 1)
        first_day = common.get_first_day_by_month(next_month)
        last_day = common.get_last_day_by_month(first_day)
        project_members = self.projectmember_set.public_filter(start_date__gte=first_day,
                                                               start_date__lte=last_day,
                                                               status=2,
                                                               is_deleted=False)
        return project_members[0] if project_members.count() > 0 else None

    def get_project_end_date(self):
        # 稼働状態を取得する（待機・稼働中）
        if self.pk == 787:
            pass
        now = datetime.datetime.now()
        projects = self.projectmember_set.public_filter(end_date__gte=now, start_date__lte=now,
                                                        status=2, is_deleted=False)
        if projects.count() > 0:
            return projects[0].end_date
        else:
            return None

    def get_business_status(self):
        """営業状態を取得する

        planning_countとlast_end_dateはget_sales_membersにより取得されている

        :return:
        """
        next_2_month = common.add_months(datetime.date.today(), 2)
        if hasattr(self, 'planning_count'):
            if self.planning_count > 0:
                return u"営業中"
            if self.last_end_date and self.last_end_date >= next_2_month:
                return u"-"
            else:
                return u"未提案"
        else:
            return u"-"

    def get_skill_list(self):
        query_set = Member.objects.raw(u"SELECT DISTINCT S.*"
                                       u"  FROM eb_member M"
                                       u"  JOIN eb_projectmember PM ON M.ID = PM.MEMBER_ID"
                                       u"  JOIN eb_project P ON P.ID = PM.PROJECT_ID"
                                       u"  JOIN eb_projectskill PS ON PS.PROJECT_ID = P.ID"
                                       u"  JOIN mst_skill S ON S.ID = PS.SKILL_ID"
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
                                       u"  JOIN mst_skill S ON S.ID = PS.SKILL_ID"
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
        """該当メンバーの職位を取得する

        :param is_min:
        :return:
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
                tree = ElementTree.XML(xml)
                lat = tree.find(".//coordinate/lat")
                lng = tree.find(".//coordinate/lng")
                if lat is not None and lng is not None:
                    self.lat = lat.text
                    self.lng = lng.text
                    self.save()
                    return True
                else:
                    return False
            except Exception as e:
                logger = logging.getLogger(constants.LOG_EB_SALES)
                logger.error(e.message)
                logger.error(traceback.format_exc())
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

    def get_project_by_month(self, year, month):
        ym = '%s%02d' % (year, int(month))
        first_day = common.get_first_day_from_ym(ym)
        last_day = common.get_last_day_by_month(first_day)
        project_member_set = self.projectmember_set.public_filter(start_date__lte=last_day, 
                                                                  end_date__gte=first_day,
                                                                  is_deleted=False)
        if project_member_set.count() > 0:
            return project_member_set[0].project
        else:
            return None

    def get_cost(self, date):
        """コストを取得する

        :return:
        """
        contract = self.get_contract(date)
        if contract:
            return contract.get_cost()
        else:
            return 0

    def get_latest_contract(self):
        """最新の契約情報を取得する

        :return:
        """
        today = datetime.date.today()
        return self.get_contract(today)

    def get_current_contract(self):
        return self.get_contract(datetime.date.today())

    def get_contract(self, date):
        """指定日付の契約情報を取得する。

        :param date 対象年月
        :return:
        """
        contract = None
        last_day = common.get_last_day_by_month(date)
        contract_list = self.contract_set.filter(
            employment_date__lte=last_day
        ).exclude(status='04').order_by('-employment_date', '-contract_no')
        bp_contract_list = self.bpcontract_set.filter(
            start_date__lte=last_day,
            is_deleted=False,
        ).order_by('-start_date')
        if bp_contract_list.count() > 0:
            contract = bp_contract_list[0]
        else:
            if contract_list.count() > 0:
                contract = contract_list[0]
        return contract

    def is_belong_to(self, user, date):
        if user.is_superuser:
            return True
        first_day = common.get_first_day_by_month(date)
        last_day = common.get_last_day_by_month(date)
        if hasattr(user, 'member'):
            with connection.cursor() as cursor:
                cursor.execute("select distinct boss.id boss_id"
                               "     , ps.position"
                               "  from eb_positionship ps"
                               "  join eb_membersectionperiod msp on (   msp.section_id = ps.section_id "
                               "                                      or msp.division_id = ps.section_id"
                               "                                      or msp.subsection_id = ps.section_id)"
                               "  join eb_member m on m.id = msp.member_id"
                               "  join eb_member boss on boss.id = ps.member_id"
                               " where m.is_deleted = 0"
                               "   and ps.is_deleted = 0"
                               "   and msp.is_deleted = 0"
                               "   and msp.start_date <= %s"
                               "   and (msp.end_date >= %s or msp.end_date is null)"
                               "   and ps.position in (3, 4, 5, 6, 7)"
                               "   and m.id = %s"
                               "   and boss.id = %s", [last_day, first_day, self.pk, user.member.pk])
                records = cursor.fetchall()
            if len(records) > 0:
                return True
            else:
                return False
        elif hasattr(user, 'salesperson'):
            # 営業員ログインの場合
            with connection.cursor() as cursor:
                cursor.execute("select count(*)"
                               "  from eb_member m"
                               "  join eb_membersalespersonperiod msp on msp.member_id = m.id"
                               "  join eb_salesperson s on s.id = msp.salesperson_id"
                               " where m.is_deleted = 0"
                               "   and s.is_deleted = 0"
                               "   and msp.is_deleted = 0"
                               "   and msp.start_date <= %s"
                               "   and (msp.end_date >= %s or msp.end_date is null)"
                               "   and m.id = %s"
                               "   and msp.salesperson_id = %s", [last_day, first_day, self.pk, user.salesperson.pk])
                records = cursor.fetchall()
            if records[0][0] > 0:
                return True
            else:
                return False
        else:
            return False

    @classmethod
    def get_max_api_id(cls):
        with connection.cursor() as cursor:
            cursor.execute('select max(id_from_api) from eb_member')
            records = cursor.fetchall()
        if len(records) > 0:
            return "%04d" % (int(records[0][0]) + 1)
        else:
            return "0001"

    def get_current_month_bp_order(self):
        today = datetime.date.today()
        queryset = BpMemberOrder.objects.public_filter(project_member__member=self,
                                                       year=today.year,
                                                       month="%02d" % today.month)
        return queryset

    def get_next_month_bp_order(self):
        next_month = common.add_months(datetime.date.today(), 1)
        queryset = BpMemberOrder.objects.public_filter(project_member__member=self,
                                                       year=next_month.year,
                                                       month="%02d" % next_month.month)
        return queryset

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_date = datetime.datetime.now()
        self.save()


class V_Contract(models.Model):
    member = models.ForeignKey(Member, db_column='member_id', verbose_name=u"社員テーブル主キー")
    employee_id = models.CharField(max_length=30, verbose_name=u"給料王ＩＤ")
    id = models.BigIntegerField(db_column='ID', primary_key=True)
    code = models.CharField(max_length=2000, blank=True, null=True)
    codeid = models.CharField(db_column='codeID', max_length=2000, blank=True, null=True)
    contract_date = models.DateTimeField(db_column='CONTRACT_DATE')
    contract_no = models.CharField(db_column='CONTRACT_NO', max_length=100, blank=True, null=True)
    employer_type = models.CharField(db_column='EMPLOYER_TYPE', max_length=100, blank=True, null=True)
    employment_date = models.DateTimeField(db_column='EMPLOYMENT_DATE')
    employment_period_en = models.DateTimeField(db_column='EMPLOYMENT_PERIOD_EN')
    employment_period = models.CharField(db_column='EMPLOYMENT_PERIOD', max_length=1000, blank=True, null=True)
    business_addr = models.CharField(db_column='BUSINESS_ADDR', max_length=100, blank=True, null=True)
    business_type = models.CharField(db_column='BUSINESS_TYPE', max_length=100, blank=True, null=True)
    business_other = models.CharField(db_column='BUSINESS_OTHER', max_length=1000, blank=True, null=True)
    business_time = models.CharField(db_column='BUSINESS_TIME', max_length=1000, blank=True, null=True)
    allowance_base = models.DecimalField(db_column='ALLOWANCE_BASE', max_digits=13, decimal_places=0,
                                         blank=True, null=True)
    allowance_base_memo = models.CharField(db_column='ALLOWANCE_BASE_MEMO', max_length=1000, blank=True, null=True)
    pay_site = models.DecimalField(db_column='PAY_SITE', max_digits=13, decimal_places=0, blank=True, null=True)
    pay_site_memo = models.CharField(db_column='PAY_SITE_MEMO', max_length=1000, blank=True, null=True)
    pay_position = models.DecimalField(db_column='PAY_POSITION', max_digits=13, decimal_places=0, blank=True, null=True)
    pay_position_memo = models.CharField(db_column='PAY_POSITION_MEMO', max_length=1000, blank=True, null=True)
    pay_duties = models.DecimalField(db_column='PAY_DUTIES', max_digits=13, decimal_places=0, blank=True, null=True)
    pay_duties_memo = models.CharField(db_column='PAY_DUTIES_MEMO', max_length=1000, blank=True, null=True)
    pay_diligence = models.DecimalField(db_column='PAY_DILIGENCE', max_digits=13, decimal_places=0,
                                        blank=True, null=True)
    pay_safety = models.DecimalField(db_column='PAY_SAFETY', max_digits=13, decimal_places=0, blank=True, null=True)
    pay_qual = models.DecimalField(db_column='PAY_QUAL', max_digits=13, decimal_places=0, blank=True, null=True)
    pay_qual_memo = models.CharField(db_column='PAY_QUAL_MEMO', max_length=1000, blank=True, null=True)
    pay_commute = models.DecimalField(db_column='PAY_COMMUTE', max_digits=13, decimal_places=0, blank=True, null=True,
                                      verbose_name=u"交通費")
    pay_commute_memo = models.CharField(db_column='PAY_COMMUTE_MEMO', max_length=1000, blank=True, null=True)
    pay_overtime = models.CharField(db_column='PAY_OVERTIME', max_length=100, blank=True, null=True)
    pay_absence = models.CharField(db_column='PAY_ABSENCE', max_length=100, blank=True, null=True)
    endowment_insurance = models.CharField(db_column='ENDOWMENT_INSURANCE', max_length=100, blank=True, null=True,
                                           verbose_name=u"社会保険加入有無",
                                           help_text=u"1:加入しない、2:加入する")
    allowance_date = models.CharField(db_column='ALLOWANCE_DATE', max_length=1000, blank=True, null=True)
    allowance_change = models.CharField(db_column='ALLOWANCE_CHANGE', max_length=1000, blank=True, null=True)
    bonus = models.CharField(db_column='BONUS', max_length=1000, blank=True, null=True)
    holiday = models.CharField(db_column='HOLIDAY', max_length=1000, blank=True, null=True)
    paid_vacation = models.CharField(db_column='PAID_VACATION', max_length=1000, blank=True, null=True)
    not_paid_vacation = models.CharField(db_column='NOT_PAID_VACATION', max_length=1000, blank=True, null=True)
    about_discharge = models.CharField(db_column='ABOUT_DISCHARGE', max_length=1000, blank=True, null=True)
    memo = models.CharField(db_column='MEMO', max_length=1000, blank=True, null=True)
    cost = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'v_contract'
        verbose_name = verbose_name_plural = u"社員契約情報"


class MemberSectionPeriod(BaseModel):
    member = models.ForeignKey(Member, on_delete=models.PROTECT, verbose_name=u"社員名")
    division = models.ForeignKey(Section, on_delete=models.PROTECT, blank=True, null=True,
                                 related_name='memberdivisionperiod_set',
                                 verbose_name=u"事業部")
    section = models.ForeignKey(Section, blank=True, null=True, on_delete=models.PROTECT, verbose_name=u"部署")
    subsection = models.ForeignKey(Section, blank=True, null=True, on_delete=models.PROTECT,
                                   related_name='membersubsectionperiod_set',
                                   verbose_name=u"課・グループ")
    start_date = models.DateField(verbose_name=u"開始日")
    end_date = models.DateField(blank=True, null=True, verbose_name=u"終了日")

    class Meta:
        ordering = ['start_date']
        verbose_name = verbose_name_plural = u"社員の部署期間"

    def __unicode__(self):
        f = u"%s - %s(%s〜%s)"
        if self.division:
            organization = unicode(self.division)
        elif self.section:
            organization = unicode(self.section)
        else:
            organization = unicode(self.subsection)
        return f % (self.member.__unicode__(), organization, self.start_date, self.end_date)


class MemberSalespersonPeriod(BaseModel):
    member = models.ForeignKey(Member, on_delete=models.PROTECT, verbose_name=u"社員名")
    salesperson = models.ForeignKey(Salesperson, on_delete=models.PROTECT, verbose_name=u"営業員")
    start_date = models.DateField(verbose_name=u"開始日")
    end_date = models.DateField(blank=True, null=True, verbose_name=u"終了日")

    class Meta:
        ordering = ['start_date']
        verbose_name = verbose_name_plural = u"社員の営業員期間"

    def __unicode__(self):
        f = u"%s - %s(%s〜%s)"
        return f % (self.member.__unicode__(), self.salesperson.__unicode__(), self.start_date, self.end_date)


class MemberSalesOffPeriod(BaseModel):
    member = models.ForeignKey(Member, on_delete=models.PROTECT, verbose_name=u"社員名")
    sales_off_reason = models.ForeignKey(SalesOffReason, on_delete=models.PROTECT, verbose_name=u"営業対象外理由")
    start_date = models.DateField(verbose_name=u"開始日")
    end_date = models.DateField(blank=True, null=True, verbose_name=u"終了日")

    class Meta:
        ordering = ['start_date']
        verbose_name = verbose_name_plural = u"社員の営業対象外期間"

    def __unicode__(self):
        f = u"%s - %s(%s〜%s)"
        return f % (unicode(self.member), unicode(self.sales_off_reason), self.start_date, self.end_date)


class PositionShip(BaseModel):
    member = models.ForeignKey(Member, on_delete=models.PROTECT, verbose_name=u"社員名")
    position = models.IntegerField(blank=True, null=True, choices=constants.CHOICE_POSITION, verbose_name=u"職位")
    section = models.ForeignKey(Section, on_delete=models.PROTECT, verbose_name=u"所属")
    is_part_time = models.BooleanField(default=False, verbose_name=u"兼任")

    class Meta:
        ordering = ['position']
        verbose_name = verbose_name_plural = u"職位"

    def __unicode__(self):
        return "%s - %s %s" % (self.get_position_display(), self.member.first_name, self.member.last_name)


class Client(AbstractCompany):
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
    salesperson = models.ForeignKey(Salesperson, blank=True, null=True, on_delete=models.PROTECT, verbose_name=u"営業担当")
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

        :param date:
        :return:
        """
        months = int(self.payment_month) if self.payment_month else 1
        pay_month = common.add_months(date, months)
        if self.payment_day == '99' or not self.payment_day:
            return common.get_last_day_by_month(pay_month)
        else:
            pay_day = int(self.payment_day)
            last_day = common.get_last_day_by_month(pay_month)
            if last_day.day < pay_day:
                return last_day
            return datetime.date(pay_month.year, pay_month.month, pay_day)

    def get_attendance_amount(self, ym):
        """対象年月の出勤売上を取得する。

        :param ym: 対象年月
        :return:
        """
        amount = MemberAttendance.objects.public_filter(year=ym[:4], month=ym[4:],
                                                        project_member__project__client=self)\
            .aggregate(amount=Sum('price'))
        return amount.get('amount', 0) if amount.get('amount', 0) else 0

    def get_expenses_amount(self, ym):
        amount = MemberExpenses.objects.public_filter(year=ym[:4], month=ym[4:],
                                                      project_member__project__client=self)\
            .aggregate(amount=Sum('price'))
        return amount.get('amount', 0) if amount.get('amount', 0) else 0

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_date = datetime.datetime.now()
        self.save()


class ClientMember(BaseModel):
    name = models.CharField(max_length=30, verbose_name=u"名前")
    email = models.EmailField(blank=True, null=True, verbose_name=u"メールアドレス")
    phone = models.CharField(blank=True, null=True, max_length=11, verbose_name=u"電話番号")
    client = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name=u"所属会社")

    class Meta:
        ordering = ['name']
        verbose_name = verbose_name_plural = u"お客様"

    def __unicode__(self):
        return "%s - %s" % (self.client.name, self.name)


class Skill(BaseModel):
    name = models.CharField(blank=False, null=False, unique=True, max_length=30, verbose_name=u"名称")

    class Meta:
        ordering = ['name']
        verbose_name = verbose_name_plural = u"スキル"
        db_table = 'mst_skill'

    def __unicode__(self):
        return self.name


class OS(BaseModel):
    name = models.CharField(max_length=15, unique=True, verbose_name=u"名称")

    class Meta:
        ordering = ['name']
        verbose_name = verbose_name_plural = u"機種／OS"
        db_table = 'mst_os'

    def __unicode__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(blank=False, null=False, max_length=50, verbose_name=u"案件名称")
    description = models.TextField(blank=True, null=True, verbose_name=u"案件概要")
    business_type = models.CharField(blank=False, null=True, max_length=2,
                                     choices=constants.CHOICE_PROJECT_BUSINESS_TYPE,
                                     verbose_name=u"事業分類",
                                     help_text=u"必ず入力してください、質問があったら 沈さん にお問い合わせください。")
    skills = models.ManyToManyField(Skill, through='ProjectSkill', blank=True, verbose_name=u"スキル要求")
    os = models.ManyToManyField(OS, blank=True, verbose_name=u"機種／OS")
    start_date = models.DateField(blank=True, null=True, verbose_name=u"開始日")
    end_date = models.DateField(blank=True, null=True, verbose_name=u"終了日",
                                help_text=u"もし設定した終了日は一番最後の案件メンバーの終了日より以前の日付だったら、"
                                          u"自動的に最後のメンバーの終了日に設定する。")
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
    is_hourly_pay = models.BooleanField(default=False, verbose_name=u"時給",
                                        help_text=u"选中后将会无视人员的单价与增减等信息，计算请求时会将总时间乘以时薪。")
    is_reserve = models.BooleanField(default=False, verbose_name=u"待機案件フラグ",
                                     help_text=u"バーチャル案件です、コストなどを算出ために非稼働メンバーを"
                                               u"この案件にアサインすればいい。")
    client = models.ForeignKey(Client, null=True, on_delete=models.PROTECT, verbose_name=u"関連会社")
    boss = models.ForeignKey(ClientMember, blank=True, null=True, related_name="boss_set", on_delete=models.PROTECT,
                             verbose_name=u"案件責任者")
    middleman = models.ForeignKey(ClientMember, blank=True, null=True, on_delete=models.PROTECT,
                                  related_name="middleman_set", verbose_name=u"案件連絡者")
    salesperson = models.ForeignKey(Salesperson, blank=True, null=True, on_delete=models.PROTECT, verbose_name=u"営業員")
    department = models.ForeignKey(Section, blank=True, null=True, verbose_name=u"所属部署", on_delete=models.PROTECT,
                                   help_text=u"一括案件で、メンバーアサインしていない場合を設定する。")
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
        permissions = (
            ('view_project', u'案件参照'),
        )

    def __unicode__(self):
        return self.name

    def get_project_members(self):
        """案件の現在アサイン中のメンバーを取得する。

        :return:
        """
        today = datetime.date.today()
        return self.projectmember_set.public_filter(start_date__lte=today,
                                                    end_date__gte=today)

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
                                       u"  JOIN mst_skill s ON s.ID = ps.SKILL_ID"
                                       u" WHERE s.NAME = %s"
                                       u"   AND pm.END_DATE < %s"
                                       u"   AND pm.STATUS <> 1"
                                       u"   AND NOT EXISTS (SELECT 1 "
                                       u"                     FROM eb_projectmember pm2"
                                       u"                    WHERE pm2.START_DATE >= %s"
                                       u"                      AND pm2.MEMBER_ID = m.ID"
                                       u"                      AND pm2.PROJECT_ID = %s"
                                       u"                      AND pm2.STATUS = 1)", [name,
                                                                                      last_day_a_month_later,
                                                                                      datetime.date.today(),
                                                                                      self.pk]
                                       )
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
                                                    end_date__gte=first_day,
                                                    is_deleted=False).exclude(status='1')

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
        project_members = self.projectmember_set.public_filter(start_date__lte=last_day, end_date__gte=first_day,
                                                               role=7, is_deleted=False)
        if project_members.count() == 0:
            project_members = self.projectmember_set.public_filter(start_date__lte=last_day, end_date__gte=first_day,
                                                                   role=6, is_deleted=False)
        if project_members.count() == 0:
            project_members = self.projectmember_set.public_filter(start_date__lte=last_day, end_date__gte=first_day,
                                                                   is_deleted=False)
        if project_members.count() > 0:
            return project_members[0]
        else:
            return None

    def get_working_project_members(self):
        now = datetime.date.today()
        first_day = datetime.date(now.year, now.month, 1)
        last_day = common.get_last_day_by_month(now)
        return self.projectmember_set.public_filter(start_date__lte=last_day, end_date__gte=first_day,
                                                    is_deleted=False)

    def get_expenses(self, year, month, project_members):
        """指定年月の清算リストを取得する。

        :param year:
        :param month:
        :param project_members:
        :return:
        """
        return MemberExpenses.objects.public_filter(project_member__project=self,
                                                    year=str(year),
                                                    month=str(month),
                                                    project_member__in=project_members).order_by('category__name')

    def get_order_by_month(self, year, month):
        """指定年月の注文履歴を取得する。

        :param year:
        :param month:
        :return:
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
                old_project_request = self.get_project_request(year, month)
                for client_order in client_orders:
                    project_request = self.get_project_request(year, month, client_order)
                    if project_request and not project_request.pk:
                        project_request = old_project_request
                    if project_request and not project_request.pk:
                        project_request = None
                    ret_value.append((year, month, client_order, cnt, project_members_month, project_request))
            else:
                ret_value.append((year, month, None, 0, None, None))
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

    def get_project_request(self, str_year, str_month, client_order=None):
        """請求番号を取得する。

        :param str_year:
        :param str_month:
        :param client_order:
        :return:
        """
        if self.projectrequest_set.filter(year=str_year, month=str_month, client_order=client_order).count() == 0:
            # 指定年月の請求番号がない場合、請求番号を発行する。
            max_request_no = ProjectRequest.objects.filter(year=str_year, month=str_month).aggregate(Max('request_no'))
            request_no = max_request_no.get('request_no__max')
            if request_no and re.match(r"^([0-9]{7}|[0-9]{7}-[0-9]{3})$", request_no):
                no = request_no[4:7]
                no = "%03d" % (int(no) + 1,)
                next_request = "%s%s%s" % (str_year[2:], str_month, no)
            else:
                next_request = "%s%s%s" % (str_year[2:], str_month, "001")
            project_request = ProjectRequest(project=self, client_order=client_order,
                                             year=str_year, month=str_month, request_no=next_request)
            return project_request
        else:
            # 存在する場合、そのまま使う、再発行はしません。
            project_request = self.projectrequest_set.filter(year=str_year, month=str_month,
                                                             client_order=client_order)[0]
            return project_request

    def can_end_project(self):
        """案件が終了できるかどうかを判断する。

        案件メンバーの一人でも終了日は本日以降でしたら、終了はできません。

        :return:
        """
        today = datetime.date.today()
        project_members = self.projectmember_set.all()
        for project_member in project_members:
            if project_member.end_date >= today:
                return False
        return True

    @property
    def all_price_lump(self):
        """一括案件の税込売上を取得する。

        :return:
        """
        return self.lump_amount + self.lump_amount * self.client.tax_rate

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_date = datetime.datetime.now()
        self.save()


def get_client_order_path(instance, filename):
    return u"./client_order/{0}/{1}{2}_{3}".format(instance.project.client.name,
                                                   instance.start_date.year, instance.start_date.month,
                                                   filename)


class ClientOrder(BaseModel):
    projects = models.ManyToManyField(Project, verbose_name=u"案件")
    name = models.CharField(max_length=50, verbose_name=u"注文書名称")
    start_date = models.DateField(default=timezone.now, verbose_name=u"開始日")
    end_date = models.DateField(default=timezone.now, verbose_name=u"終了日")
    order_no = models.CharField(max_length=20, verbose_name=u"注文番号")
    order_date = models.DateField(blank=False, null=True, verbose_name=u"注文日")
    bank_info = models.ForeignKey(BankInfo, blank=False, null=True, on_delete=models.PROTECT, verbose_name=u"振込先口座")
    order_file = models.FileField(blank=True, null=True, upload_to=get_client_order_path, verbose_name=u"注文書")
    member_comma_list = models.CharField(max_length=255, blank=True, null=True, editable=False,
                                         verbose_name=u"メンバー主キーのリスト",
                                         validators=[validate_comma_separated_integer_list])

    class Meta:
        ordering = ['name', 'start_date', 'end_date']
        verbose_name = verbose_name_plural = u"お客様注文書"

    def __unicode__(self):
        return self.name


class ProjectRequest(models.Model):
    project = models.ForeignKey(Project, on_delete=models.PROTECT, verbose_name=u"案件")
    client_order = models.ForeignKey(ClientOrder, blank=True, null=True, on_delete=models.PROTECT, verbose_name=u"注文書")
    year = models.CharField(max_length=4, default=str(datetime.date.today().year),
                            choices=constants.CHOICE_ATTENDANCE_YEAR, verbose_name=u"対象年")
    month = models.CharField(max_length=2, choices=constants.CHOICE_ATTENDANCE_MONTH, verbose_name=u"対象月")
    request_no = models.CharField(max_length=7, unique=True, verbose_name=u"請求番号")
    request_name = models.CharField(max_length=50, blank=True, null=True, verbose_name=u"請求名称")
    amount = models.IntegerField(default=0, verbose_name=u"請求金額（税込）")
    turnover_amount = models.IntegerField(default=0, verbose_name=u"売上金額（基本単価＋残業料）（税抜き）")
    tax_amount = models.IntegerField(default=0, verbose_name=u"税金")
    expenses_amount = models.IntegerField(default=0, verbose_name=u"精算金額")
    filename = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"請求書ファイル名")
    created_user = models.ForeignKey(User, related_name='created_requests', null=True, on_delete=models.PROTECT,
                                     editable=False, verbose_name=u"作成者")
    created_date = models.DateTimeField(null=True, auto_now_add=True, editable=False, verbose_name=u"作成日時")
    updated_user = models.ForeignKey(User, related_name='updated_requests', null=True, on_delete=models.PROTECT,
                                     editable=False, verbose_name=u"更新者")
    updated_date = models.DateTimeField(null=True, auto_now=True, editable=False, verbose_name=u"更新日時")

    class Meta:
        ordering = ['-request_no']
        unique_together = ('project', 'client_order', 'year', 'month')
        verbose_name = verbose_name_plural = u"案件請求情報"
        permissions = (
            ('generate_request', u"請求書作成"),
            ('view_turnover', u"売上情報参照")
        )

    def __unicode__(self):
        return u"%s-%s" % (self.request_no, self.project.name)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, other_data=None):
        super(ProjectRequest, self).save(force_insert, force_update, using, update_fields)
        # 請求書作成時、請求に関する全ての情報を履歴として保存する。
        if other_data:
            data = other_data
            # 既存のデータを全部消す。
            if hasattr(self, "projectrequestheading"):
                self.projectrequestheading.delete()
            self.projectrequestdetail_set.all().delete()
            bank = data['EXTRA']['BANK']
            date = datetime.datetime(int(self.year), int(self.month), 1, tzinfo=common.get_tz_utc())
            date = common.get_last_day_by_month(date)
            heading = ProjectRequestHeading(project_request=self,
                                            is_lump=self.project.is_lump,
                                            lump_amount=self.project.lump_amount,
                                            lump_comment=self.project.lump_comment,
                                            is_hourly_pay=self.project.is_hourly_pay,
                                            client=self.project.client,
                                            client_post_code=data['DETAIL']['CLIENT_POST_CODE'],
                                            client_address=data['DETAIL']['CLIENT_ADDRESS'],
                                            client_tel=data['DETAIL']['CLIENT_TEL'],
                                            client_name=data['DETAIL']['CLIENT_COMPANY_NAME'],
                                            tax_rate=self.project.client.tax_rate,
                                            decimal_type=self.project.client.decimal_type,
                                            work_period_start=data['EXTRA']['WORK_PERIOD_START'],
                                            work_period_end=data['EXTRA']['WORK_PERIOD_END'],
                                            remit_date=data['EXTRA']['REMIT_DATE'],
                                            publish_date=data['EXTRA']['PUBLISH_DATE'],
                                            company_post_code=data['DETAIL']['POST_CODE'],
                                            company_address=data['DETAIL']['ADDRESS'],
                                            company_name=data['DETAIL']['COMPANY_NAME'],
                                            company_tel=data['DETAIL']['TEL'],
                                            company_master=data['DETAIL']['MASTER'],
                                            bank=data['EXTRA']['BANK'],
                                            bank_name=bank.bank_name,
                                            branch_no=bank.branch_no,
                                            branch_name=bank.branch_name,
                                            account_type=bank.account_type,
                                            account_number=bank.account_number,
                                            account_holder=bank.account_holder)
            heading.save()
            for i, item in enumerate(data['MEMBERS']):
                project_member = item["EXTRA_PROJECT_MEMBER"]
                ym = data['EXTRA']['YM']
                cost = project_member.member.get_cost(date)
                detail = ProjectRequestDetail(project_request=self,
                                              project_member=project_member,
                                              member_section=project_member.member.get_section(date),
                                              member_type=project_member.member.member_type,
                                              salesperson=project_member.member.get_salesperson(date),
                                              subcontractor=project_member.member.subcontractor,
                                              cost=cost,
                                              no=str(i + 1),
                                              hourly_pay=project_member.hourly_pay if project_member.hourly_pay else 0,
                                              basic_price=project_member.price,
                                              min_hours=project_member.min_hours,
                                              max_hours=project_member.max_hours,
                                              total_hours=item['ITEM_WORK_HOURS'] if item['ITEM_WORK_HOURS'] else 0,
                                              extra_hours=item['ITEM_EXTRA_HOURS']if item['ITEM_EXTRA_HOURS'] else 0,
                                              rate=item['ITEM_RATE'],
                                              plus_per_hour=project_member.plus_per_hour,
                                              minus_per_hour=project_member.minus_per_hour,
                                              total_price=item['ITEM_AMOUNT_TOTAL'],
                                              expenses_price=project_member.get_expenses_amount(ym[:4], int(ym[4:])),
                                              comment=item['ITEM_COMMENT'])
                detail.save()


class ProjectRequestHeading(models.Model):
    project_request = models.OneToOneField(ProjectRequest, verbose_name=u"請求書")
    is_lump = models.BooleanField(default=False, verbose_name=u"一括フラグ")
    lump_amount = models.BigIntegerField(default=0, blank=True, null=True, verbose_name=u"一括金額")
    lump_comment = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"一括の備考")
    is_hourly_pay = models.BooleanField(default=False, verbose_name=u"時給")
    client = models.ForeignKey(Client, null=True, on_delete=models.PROTECT, verbose_name=u"関連会社")
    client_post_code = models.CharField(blank=True, null=True, max_length=8, verbose_name=u"お客様郵便番号")
    client_address = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"お客様住所１")
    client_tel = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"お客様電話番号")
    client_name = models.CharField(blank=True, null=True, max_length=30, verbose_name=u"お客様会社名")
    tax_rate = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=2, verbose_name=u"税率")
    decimal_type = models.CharField(blank=True, null=True, max_length=1, choices=constants.CHOICE_DECIMAL_TYPE,
                                    verbose_name=u"小数の処理区分")
    work_period_start = models.DateField(blank=True, null=True, verbose_name=u"作業期間＿開始")
    work_period_end = models.DateField(blank=True, null=True, verbose_name=u"作業期間＿終了")
    remit_date = models.DateField(blank=True, null=True, verbose_name=u"お支払い期限")
    publish_date = models.DateField(blank=True, null=True, verbose_name=u"発行日")
    company_post_code = models.CharField(blank=True, null=True, max_length=8, verbose_name=u"本社郵便番号")
    company_address = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"本社住所")
    company_name = models.CharField(blank=True, null=True, max_length=30, verbose_name=u"会社名")
    company_tel = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"お客様電話番号")
    company_master = models.CharField(blank=True, null=True, max_length=30, verbose_name=u"代表取締役")
    bank = models.ForeignKey(BankInfo, blank=True, null=True, on_delete=models.PROTECT, verbose_name=u"口座")
    bank_name = models.CharField(blank=True, null=True, max_length=20, verbose_name=u"銀行名称")
    branch_no = models.CharField(blank=True, null=True, max_length=3, verbose_name=u"支店番号")
    branch_name = models.CharField(blank=True, null=True, max_length=20, verbose_name=u"支店名称")
    account_type = models.CharField(blank=True, null=True, max_length=1, choices=constants.CHOICE_ACCOUNT_TYPE,
                                    verbose_name=u"預金種類")
    account_number = models.CharField(blank=True, null=True, max_length=7, verbose_name=u"口座番号")
    account_holder = models.CharField(blank=True, null=True, max_length=20, verbose_name=u"口座名義")

    class Meta:
        ordering = ['-project_request__request_no']
        verbose_name = verbose_name_plural = u"案件請求見出し"


class ProjectRequestDetail(models.Model):
    project_request = models.ForeignKey(ProjectRequest, on_delete=models.PROTECT, verbose_name=u"請求書")
    project_member = models.ForeignKey('ProjectMember', on_delete=models.PROTECT, verbose_name=u"メンバー")
    member_section = models.ForeignKey(Section, verbose_name=u"部署")
    member_type = models.IntegerField(default=0, choices=constants.CHOICE_MEMBER_TYPE, verbose_name=u"社員区分")
    salesperson = models.ForeignKey(Salesperson, blank=True, null=True, on_delete=models.PROTECT, verbose_name=u"営業員")
    subcontractor = models.ForeignKey(Subcontractor, blank=True, null=True, on_delete=models.PROTECT,
                                      verbose_name=u"協力会社")
    salary = models.IntegerField(default=0, verbose_name=u"給料")
    cost = models.IntegerField(default=0, verbose_name=u"コスト")
    no = models.IntegerField(verbose_name=u"番号")
    hourly_pay = models.IntegerField(default=0, verbose_name=u"時給")
    basic_price = models.IntegerField(default=0, verbose_name=u"単価")
    min_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name=u"基準時間")
    max_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name=u"最大時間")
    total_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name=u"合計時間")
    extra_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name=u"残業時間")
    rate = models.DecimalField(max_digits=3, decimal_places=2, default=1, verbose_name=u"率")
    plus_per_hour = models.IntegerField(default=0, editable=False, verbose_name=u"増（円）")
    minus_per_hour = models.IntegerField(default=0, editable=False, verbose_name=u"減（円）")
    total_price = models.IntegerField(default=0, verbose_name=u"売上（基本単価＋残業料）（税抜き）")
    expenses_price = models.IntegerField(default=0, verbose_name=u"精算金額")
    comment = models.CharField(blank=True, null=True, max_length=50, verbose_name=u"備考")

    class Meta:
        ordering = ['-project_request__request_no', 'no']
        unique_together = ('project_request', 'no')
        verbose_name = verbose_name_plural = u"案件請求明細"

    def __unicode__(self):
        f = u"%s %s%sの請求明細"
        return f % (self.project_member,
                    self.project_request.get_year_display(),
                    self.project_request.get_month_display())

    def get_tax_price(self):
        """税金を計算する。
        """
        if not hasattr(self.project_request, 'projectrequestheading'):
            return 0

        tax_rate = self.project_request.projectrequestheading.tax_rate
        # decimal_type = self.project_request.projectrequestheading.decimal_type
        if tax_rate is None:
            return 0
        # if decimal_type == '0':
        #     # 四捨五入
        #     return int(round(self.total_price * tax_rate))
        # else:
        #     # 切り捨て
        #     return int(self.total_price * tax_rate)
        return round(self.total_price * tax_rate, 1)

    def get_all_price(self):
        """合計を計算する（税込、精算含む）
        """
        return int(self.total_price) + self.get_tax_price() + int(self.expenses_price)


class ProjectActivity(models.Model):
    project = models.ForeignKey(Project, on_delete=models.PROTECT, verbose_name=u"案件")
    name = models.CharField(max_length=30, verbose_name=u"活動名称")
    open_date = models.DateTimeField(default=timezone.now, verbose_name=u"開催日時")
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

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_date = datetime.datetime.now()
        self.save()


class ProjectSkill(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.PROTECT, verbose_name=u"案件")
    skill = models.ForeignKey(Skill, on_delete=models.PROTECT, verbose_name=u"スキル")
    period = models.IntegerField(blank=True, null=True, choices=constants.CHOICE_SKILL_TIME, verbose_name=u"経験年数")
    description = models.TextField(blank=True, null=True, verbose_name=u"備考")

    class Meta:
        verbose_name = verbose_name_plural = u"案件のスキル要求"

    def __unicode__(self):
        return "%s - %s" % (self.project.name, self.skill.name)


class ProjectStage(BaseModel):
    name = models.CharField(max_length=15, unique=True, verbose_name=u"作業工程名称")

    class Meta:
        verbose_name = verbose_name_plural = u"作業工程"
        db_table = 'mst_project_stage'

    def __unicode__(self):
        return self.name


class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.PROTECT, verbose_name=u'案件名称')
    member = models.ForeignKey(Member, on_delete=models.PROTECT, verbose_name=u"名前")
    start_date = models.DateField(blank=False, null=True, verbose_name=u"開始日")
    end_date = models.DateField(blank=False, null=True, verbose_name=u"終了日")
    price = models.IntegerField(default=0, verbose_name=u"単価")
    min_hours = models.DecimalField(max_digits=5, decimal_places=2, default=160, verbose_name=u"基準時間")
    max_hours = models.DecimalField(max_digits=5, decimal_places=2, default=180, verbose_name=u"最大時間")
    plus_per_hour = models.IntegerField(default=0, verbose_name=u"増（円）")
    minus_per_hour = models.IntegerField(default=0, verbose_name=u"減（円）")
    hourly_pay = models.IntegerField(blank=True, null=True, verbose_name=u"時給")
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

    def is_in_past(self):
        if self.end_date < datetime.date.today():
            return True
        else:
            return False

    def get_attendance(self, year, month):
        """指定された年月によって、該当するメンバーの勤怠情報を取得する。

        :param year: 対象年
        :param month: 対象月
        :return: MemberAttendanceのインスタンス、または None
        """
        try:
            return self.memberattendance_set.get(year=str(year), month="%02d" % (int(month),), is_deleted=False)
        except ObjectDoesNotExist:
            return None

    def get_attendance_amount(self, year, month):
        """メンバーの売上を取得する。

        :param year: 対象年
        :param month: 対象月
        :return:
        """
        attendance = self.get_attendance(year, month)
        if attendance:
            return attendance.price
        else:
            return 0

    def get_expenses_amount(self, year, month):
        """メンバーの清算を取得する。

        :param year:
        :param month:
        :return:
        """
        expense = self.memberexpenses_set.public_filter(year=str(year),
                                                        month="%02d" % (month,),
                                                        is_deleted=False).aggregate(price=Sum('price'))
        return expense.get('price') if expense.get('price') else 0

    def get_cost_amount(self, year, month):
        cost = self.member.cost
        attendance = self.get_attendance(year, month)
        if attendance:
            return cost + int(attendance.extra_hours * 2000)
        else:
            return cost

    def get_attendance_dict(self, year, month):
        """指定された年月の出勤情報を取得する。

        :param year: 対象年
        :param month: 対象月
        :return:
        """
        attendance = self.get_attendance(year, month)
        d = dict()
        # 勤務時間
        d['ITEM_WORK_HOURS'] = attendance.total_hours if attendance else u""

        if self.project.is_hourly_pay:
            # 基本金額
            d['ITEM_AMOUNT_BASIC'] = 0
            # 残業時間
            d['ITEM_EXTRA_HOURS'] = 0
            # 率
            d['ITEM_RATE'] = 1
            # 減（円）
            d['ITEM_MINUS_PER_HOUR'] = 0
            # 増（円）
            d['ITEM_PLUS_PER_HOUR'] = 0
            # 基本金額＋残業金額
            d['ITEM_AMOUNT_TOTAL'] = attendance.price if attendance else 0
        else:
            # 基本金額
            d['ITEM_AMOUNT_BASIC'] = self.price if attendance else u""
            # 残業時間
            d['ITEM_EXTRA_HOURS'] = attendance.extra_hours if attendance else u""
            # 率
            d['ITEM_RATE'] = attendance.rate if attendance and attendance.rate else 1
            # 減（円）
            if self.minus_per_hour is None:
                d['ITEM_MINUS_PER_HOUR'] = (self.price / self.min_hours) if attendance else u""
            else:
                d['ITEM_MINUS_PER_HOUR'] = self.minus_per_hour
            # 増（円）
            if self.plus_per_hour is None:
                d['ITEM_PLUS_PER_HOUR'] = (self.price / self.max_hours) if attendance else u""
            else:
                d['ITEM_PLUS_PER_HOUR'] = self.plus_per_hour

            if attendance and attendance.extra_hours > 0:
                d['ITEM_AMOUNT_EXTRA'] = attendance.extra_hours * d['ITEM_PLUS_PER_HOUR']
                d['ITEM_PLUS_PER_HOUR2'] = d['ITEM_PLUS_PER_HOUR']
                d['ITEM_MINUS_PER_HOUR2'] = u""
            elif attendance and attendance.extra_hours < 0:
                d['ITEM_AMOUNT_EXTRA'] = attendance.extra_hours * d['ITEM_MINUS_PER_HOUR']
                d['ITEM_PLUS_PER_HOUR2'] = u""
                d['ITEM_MINUS_PER_HOUR2'] = d['ITEM_MINUS_PER_HOUR']
            else:
                d['ITEM_AMOUNT_EXTRA'] = 0
                d['ITEM_PLUS_PER_HOUR2'] = u""
                d['ITEM_MINUS_PER_HOUR2'] = u""
            # 基本金額＋残業金額
            d['ITEM_AMOUNT_TOTAL'] = attendance.price if attendance else self.price
        # 備考
        d['ITEM_COMMENT'] = attendance.comment if attendance and attendance.comment else u""
        d['ITEM_OTHER'] = u""

        return d

    def get_bp_member_orders(self):
        if not self.start_date or not self.end_date:
            return [(None, None, None)]
        orders = []
        max_months = self.end_date.year * 12 + self.end_date.month
        min_months = self.start_date.year * 12 + self.start_date.month
        today = datetime.date.today()
        next_month = common.add_months(today, 1)
        max_date = next_month \
            if self.end_date and next_month.strftime('%Y%m') <= self.end_date.strftime('%Y%m') else today
        for i in range(max_months - min_months, -1, -1):
            date = common.add_months(self.start_date, i)
            if (max_date.year * 12 + max_date.month) < (date.year * 12 + date.month):
                # 来月以降だったら、表示する必要ないので、スキップする。
                continue
            try:
                order = BpMemberOrder.objects.get(project_member=self, year=date.year, month='%02d' % date.month)
            except (ObjectDoesNotExist, MultipleObjectsReturned):
                order = None
            days = common.get_business_days(date.year, date.month)
            orders.append((date.year, date.month, len(days), order))
        return orders

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_date = datetime.datetime.now()
        self.save()


class SubcontractorRequest(models.Model):
    subcontractor = models.ForeignKey(Subcontractor, on_delete=models.PROTECT, verbose_name=u"協力会社")
    section = models.ForeignKey(Section, on_delete=models.PROTECT, verbose_name=u"部署")
    year = models.CharField(max_length=4, default=str(datetime.date.today().year),
                            choices=constants.CHOICE_ATTENDANCE_YEAR, verbose_name=u"対象年")
    month = models.CharField(max_length=2, choices=constants.CHOICE_ATTENDANCE_MONTH, verbose_name=u"対象月")
    request_no = models.CharField(max_length=7, unique=True, verbose_name=u"請求番号")
    request_name = models.CharField(max_length=50, blank=True, null=True, verbose_name=u"請求名称")
    amount = models.IntegerField(default=0, verbose_name=u"請求金額（税込）")
    turnover_amount = models.IntegerField(default=0, verbose_name=u"売上金額（基本単価＋残業料）（税抜き）")
    tax_amount = models.IntegerField(default=0, verbose_name=u"税金")
    expenses_amount = models.IntegerField(default=0, verbose_name=u"精算金額")
    filename = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"請求書ファイル名")
    created_user = models.ForeignKey(User, related_name='created_subcontractor_requests', null=True,
                                     on_delete=models.PROTECT, editable=False, verbose_name=u"作成者")
    created_date = models.DateTimeField(null=True, auto_now_add=True, editable=False, verbose_name=u"作成日時")
    updated_user = models.ForeignKey(User, related_name='updated_subcontractor_requests', null=True,
                                     on_delete=models.PROTECT, editable=False, verbose_name=u"更新者")
    updated_date = models.DateTimeField(null=True, auto_now=True, editable=False, verbose_name=u"更新日時")

    class Meta:
        ordering = ['-request_no']
        unique_together = ('subcontractor', 'section', 'year', 'month')
        verbose_name = verbose_name_plural = u"協力会社請求情報"

    def __unicode__(self):
        return u"%s-%s" % (self.request_no, unicode(self.subcontractor))

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, other_data=None):
        super(SubcontractorRequest, self).save(force_insert, force_update, using, update_fields)
        # 請求書作成時、請求に関する全ての情報を履歴として保存する。
        if other_data:
            data = other_data
            # 既存のデータを全部消す。
            if hasattr(self, "subcontractorrequestheading"):
                self.subcontractorrequestheading.delete()
            self.subcontractorrequestdetail_set.all().delete()
            bank = data['EXTRA']['BANK']
            date = datetime.datetime(int(self.year), int(self.month), 1, tzinfo=common.get_tz_utc())
            date = common.get_last_day_by_month(date)
            company = data['EXTRA']['COMPANY']
            heading = SubcontractorRequestHeading(
                subcontractor_request=self,
                is_lump=False,
                lump_amount=0,
                lump_comment=0,
                is_hourly_pay=False,
                client=company,
                client_post_code=data['DETAIL']['CLIENT_POST_CODE'],
                client_address=data['DETAIL']['CLIENT_ADDRESS'],
                client_tel=data['DETAIL']['CLIENT_TEL'],
                client_name=data['DETAIL']['CLIENT_COMPANY_NAME'],
                tax_rate=company.tax_rate,
                decimal_type=company.decimal_type,
                work_period_start=data['EXTRA']['WORK_PERIOD_START'],
                work_period_end=data['EXTRA']['WORK_PERIOD_END'],
                remit_date=data['EXTRA']['REMIT_DATE'],
                publish_date=data['EXTRA']['PUBLISH_DATE'],
                company_post_code=data['DETAIL']['POST_CODE'],
                company_address=data['DETAIL']['ADDRESS'],
                company_name=data['DETAIL']['COMPANY_NAME'],
                company_tel=data['DETAIL']['TEL'],
                company_master=data['DETAIL']['MASTER'],
                bank=data['EXTRA']['BANK'],
                bank_name=bank.bank_name if bank else '',
                branch_no=bank.branch_no if bank else '',
                branch_name=bank.branch_name if bank else '',
                account_type=bank.account_type if bank else '',
                account_number=bank.account_number if bank else '',
                account_holder=bank.account_holder if bank else ''
            )
            heading.save()
            for i, item in enumerate(data['MEMBERS']):
                project_member = item["EXTRA_PROJECT_MEMBER"]
                ym = data['EXTRA']['YM']
                contract = project_member.member.get_contract(date)
                detail = SubcontractorRequestDetail(subcontractor_request=self)
                detail.project_member = project_member
                detail.member_section = project_member.member.get_section(date)
                detail.member_type = 4
                detail.salesperson = project_member.member.get_salesperson(date)
                detail.subcontractor = self.subcontractor
                detail.cost = 0
                detail.no = str(i + 1)
                detail.hourly_pay = contract.allowance_base if contract.is_hourly_pay else 0
                detail.basic_price = contract.allowance_base
                detail.min_hours = contract.allowance_time_min
                detail.max_hours = contract.allowance_time_max
                detail.total_hours = item['ITEM_WORK_HOURS'] if item['ITEM_WORK_HOURS'] else 0
                detail.extra_hours = item['ITEM_EXTRA_HOURS'] if item['ITEM_EXTRA_HOURS'] else 0
                detail.rate = item['ITEM_RATE']
                detail.plus_per_hour = contract.allowance_overtime
                detail.minus_per_hour = contract.allowance_absenteeism
                detail.total_price = item['ITEM_AMOUNT_TOTAL']
                detail.expenses_price = project_member.get_expenses_amount(ym[:4], int(ym[4:]))
                detail.comment = item['ITEM_COMMENT']
                # detail = SubcontractorRequestDetail(
                #     subcontractor_request=self,
                #     project_member=project_member,
                #     member_section=project_member.member.get_section(date),
                #     member_type=4,
                #     salesperson=project_member.member.get_salesperson(date),
                #     subcontractor=contract.company,
                #     cost=0,
                #     no=str(i + 1),
                #     hourly_pay=contract.allowance_base if contract.is_hourly_pay else 0,
                #     basic_price=contract.allowance_base,
                #     min_hours=contract.allowance_time_min,
                #     max_hours=contract.allowance_time_max,
                #     total_hours=item['ITEM_WORK_HOURS'] if item['ITEM_WORK_HOURS'] else 0,
                #     extra_hours=item['ITEM_EXTRA_HOURS'] if item['ITEM_EXTRA_HOURS'] else 0,
                #     rate=item['ITEM_RATE'],
                #     plus_per_hour=contract.allowance_overtime,
                #     minus_per_hour=contract.allowance_absenteeism,
                #     total_price=item['ITEM_AMOUNT_TOTAL'],
                #     expenses_price=project_member.get_expenses_amount(ym[:4], int(ym[4:])),
                #     comment=item['ITEM_COMMENT']
                # )
                detail.save()


class SubcontractorRequestHeading(models.Model):
    subcontractor_request = models.OneToOneField(SubcontractorRequest, verbose_name=u"請求書")
    is_lump = models.BooleanField(default=False, verbose_name=u"一括フラグ")
    lump_amount = models.BigIntegerField(default=0, blank=True, null=True, verbose_name=u"一括金額")
    lump_comment = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"一括の備考")
    is_hourly_pay = models.BooleanField(default=False, verbose_name=u"時給")
    client = models.ForeignKey(Company, null=True, on_delete=models.PROTECT, verbose_name=u"関連会社")
    client_post_code = models.CharField(blank=True, null=True, max_length=8, verbose_name=u"お客様郵便番号")
    client_address = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"お客様住所１")
    client_tel = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"お客様電話番号")
    client_name = models.CharField(blank=True, null=True, max_length=30, verbose_name=u"お客様会社名")
    tax_rate = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=2, verbose_name=u"税率")
    decimal_type = models.CharField(blank=True, null=True, max_length=1, choices=constants.CHOICE_DECIMAL_TYPE,
                                    verbose_name=u"小数の処理区分")
    work_period_start = models.DateField(blank=True, null=True, verbose_name=u"作業期間＿開始")
    work_period_end = models.DateField(blank=True, null=True, verbose_name=u"作業期間＿終了")
    remit_date = models.DateField(blank=True, null=True, verbose_name=u"お支払い期限")
    publish_date = models.DateField(blank=True, null=True, verbose_name=u"発行日")
    company_post_code = models.CharField(blank=True, null=True, max_length=8, verbose_name=u"本社郵便番号")
    company_address = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"本社住所")
    company_name = models.CharField(blank=True, null=True, max_length=30, verbose_name=u"会社名")
    company_tel = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"お客様電話番号")
    company_master = models.CharField(blank=True, null=True, max_length=30, verbose_name=u"代表取締役")
    bank = models.ForeignKey(SubcontractorBankInfo, blank=True, null=True, on_delete=models.PROTECT, verbose_name=u"口座")
    bank_name = models.CharField(blank=True, null=True, max_length=20, verbose_name=u"銀行名称")
    branch_no = models.CharField(blank=True, null=True, max_length=3, verbose_name=u"支店番号")
    branch_name = models.CharField(blank=True, null=True, max_length=20, verbose_name=u"支店名称")
    account_type = models.CharField(blank=True, null=True, max_length=1, choices=constants.CHOICE_ACCOUNT_TYPE,
                                    verbose_name=u"預金種類")
    account_number = models.CharField(blank=True, null=True, max_length=7, verbose_name=u"口座番号")
    account_holder = models.CharField(blank=True, null=True, max_length=20, verbose_name=u"口座名義")

    class Meta:
        ordering = ['-subcontractor_request__request_no']
        verbose_name = verbose_name_plural = u"協力会社請求見出し"


class SubcontractorRequestDetail(models.Model):
    subcontractor_request = models.ForeignKey(SubcontractorRequest, on_delete=models.PROTECT, verbose_name=u"請求書")
    project_member = models.ForeignKey('ProjectMember', on_delete=models.PROTECT, verbose_name=u"メンバー")
    member_section = models.ForeignKey(Section, verbose_name=u"部署")
    member_type = models.IntegerField(default=4, choices=constants.CHOICE_MEMBER_TYPE, verbose_name=u"社員区分")
    salesperson = models.ForeignKey(Salesperson, blank=True, null=True, on_delete=models.PROTECT,
                                    verbose_name=u"営業員")
    subcontractor = models.ForeignKey(Subcontractor, blank=True, null=True, on_delete=models.PROTECT,
                                      verbose_name=u"協力会社")
    salary = models.IntegerField(default=0, verbose_name=u"給料")
    cost = models.IntegerField(default=0, verbose_name=u"コスト")
    no = models.IntegerField(verbose_name=u"番号")
    hourly_pay = models.IntegerField(default=0, verbose_name=u"時給")
    basic_price = models.IntegerField(default=0, verbose_name=u"単価")
    min_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name=u"基準時間")
    max_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name=u"最大時間")
    total_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name=u"合計時間")
    extra_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name=u"残業時間")
    rate = models.DecimalField(max_digits=3, decimal_places=2, default=1, verbose_name=u"率")
    plus_per_hour = models.IntegerField(default=0, editable=False, verbose_name=u"増（円）")
    minus_per_hour = models.IntegerField(default=0, editable=False, verbose_name=u"減（円）")
    total_price = models.IntegerField(default=0, verbose_name=u"売上（基本単価＋残業料）（税抜き）")
    expenses_price = models.IntegerField(default=0, verbose_name=u"精算金額")
    comment = models.CharField(blank=True, null=True, max_length=50, verbose_name=u"備考")

    class Meta:
        ordering = ['-subcontractor_request__request_no', 'no']
        unique_together = ('subcontractor_request', 'no')
        verbose_name = verbose_name_plural = u"協力会社請求明細"

    def __unicode__(self):
        f = u"%s %s%sの請求明細"
        return f % (self.project_member,
                    self.subcontractor_request.get_year_display(),
                    self.subcontractor_request.get_month_display())

    def get_tax_price(self):
        """税金を計算する。
        """
        if not hasattr(self.subcontractor_request, 'subcontractorrequestheading'):
            return 0

        tax_rate = self.subcontractor_request.subcontractorrequestheading.tax_rate
        # decimal_type = self.project_request.subcontractorrequestheading.decimal_type
        if tax_rate is None:
            return 0
        # if decimal_type == '0':
        #     # 四捨五入
        #     return int(round(self.total_price * tax_rate))
        # else:
        #     # 切り捨て
        #     return int(self.total_price * tax_rate)
        return round(self.total_price * tax_rate, 1)

    def get_all_price(self):
        """合計を計算する（税込、精算含む）
        """
        return int(self.total_price) + self.get_tax_price() + int(self.expenses_price)


# class ProjectMemberPrice(BaseModel):
#     project_member = models.ForeignKey(ProjectMember, verbose_name=u"案件メンバー")
#     start_date = models.DateField(verbose_name=u"開始日")
#     end_date = models.DateField(blank=True, null=True, verbose_name=u"終了日")
#     is_hourly_pay = models.BooleanField(default=False, verbose_name=u"時給")
#     price = models.IntegerField(default=0, verbose_name=u"単価")
#     min_hours = models.DecimalField(max_digits=5, decimal_places=2, default=160, verbose_name=u"基準時間")
#     max_hours = models.DecimalField(max_digits=5, decimal_places=2, default=180, verbose_name=u"最大時間")
#     plus_per_hour = models.IntegerField(default=0, verbose_name=u"増（円）")
#     minus_per_hour = models.IntegerField(default=0, verbose_name=u"減（円）")
#
#     class Meta:
#         verbose_name = verbose_name_plural = u"案件メンバー単価"
#
#     def __unicode__(self):
#         return u"%s(%s)" % (unicode(self.project_member), self.start_date)


class ExpensesCategory(BaseModel):
    name = models.CharField(max_length=50, unique=True, verbose_name=u"名称")

    class Meta:
        verbose_name = verbose_name_plural = u"精算分類"
        db_table = 'mst_expenses_category'

    def __unicode__(self):
        return self.name


class EmployeeExpenses(BaseModel):
    member = models.ForeignKey(Member, on_delete=models.PROTECT, verbose_name=u"社員")
    year = models.CharField(max_length=4, default=str(datetime.date.today().year),
                            choices=constants.CHOICE_ATTENDANCE_YEAR, verbose_name=u"対象年")
    month = models.CharField(max_length=2, choices=constants.CHOICE_ATTENDANCE_MONTH, verbose_name=u"対象月")
    advance_amount = models.IntegerField(default=0, verbose_name=u"管理職立替金額")

    class Meta:
        unique_together = ('member', 'year', 'month')
        verbose_name = verbose_name_plural = u"社員精算リスト"

    def __unicode__(self):
        return u"%s %s %s" % (self.member, self.get_year_display(), self.get_month_display())


class MemberExpenses(BaseModel):
    project_member = models.ForeignKey(ProjectMember, on_delete=models.PROTECT, verbose_name=u"要員")
    year = models.CharField(max_length=4, default=str(datetime.date.today().year),
                            choices=constants.CHOICE_ATTENDANCE_YEAR, verbose_name=u"対象年")
    month = models.CharField(max_length=2, choices=constants.CHOICE_ATTENDANCE_MONTH, verbose_name=u"対象月")
    category = models.ForeignKey(ExpensesCategory, on_delete=models.PROTECT, verbose_name=u"分類")
    price = models.IntegerField(default=0, verbose_name=u"金額")

    objects = PublicManager(is_deleted=False, project_member__is_deleted=False, category__is_deleted=False)

    class Meta:
        ordering = ['project_member', 'year', 'month']
        verbose_name = verbose_name_plural = u"精算リスト"

    def __unicode__(self):
        return u"%s %s %s" % (self.project_member, self.get_year_display(), self.get_month_display())


class MemberAttendance(BaseModel):
    project_member = models.ForeignKey(ProjectMember, on_delete=models.PROTECT, verbose_name=u"メンバー")
    year = models.CharField(max_length=4, default=str(datetime.date.today().year),
                            choices=constants.CHOICE_ATTENDANCE_YEAR, verbose_name=u"対象年")
    month = models.CharField(max_length=2, choices=constants.CHOICE_ATTENDANCE_MONTH, verbose_name=u"対象月")
    rate = models.DecimalField(max_digits=3, decimal_places=2, default=1, verbose_name=u"率")
    salary = models.IntegerField(default=0, editable=False, verbose_name=u"給料")
    cost = models.IntegerField(default=0, editable=False, verbose_name=u"コスト",
                               help_text=u"交通費、残業、保険など含む")
    basic_price = models.IntegerField(default=0, editable=False, verbose_name=u"単価")
    total_hours = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=u"合計時間")
    extra_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name=u"残業時間")
    total_days = models.IntegerField(blank=True, null=True, editable=False, verbose_name=u"勤務日数")
    night_days = models.IntegerField(blank=True, null=True, editable=False, verbose_name=u"深夜日数")
    advances_paid = models.IntegerField(blank=True, null=True, editable=False, verbose_name=u"立替金")
    advances_paid_client = models.IntegerField(blank=True, null=True, editable=False, verbose_name=u"客先立替金")
    traffic_cost = models.IntegerField(blank=True, null=True, editable=False, verbose_name=u"勤務交通費",
                                       help_text=u"今月に勤務交通費がない場合、先月のを使用する。")
    allowance = models.IntegerField(blank=True, null=True, editable=False, verbose_name=u"手当",
                                    help_text=u"今月に手当がない場合、先月のを使用する。")
    expenses = models.IntegerField(blank=True, null=True, editable=False, verbose_name=u"経費")
    min_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0, editable=False, verbose_name=u"基準時間")
    max_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0, editable=False, verbose_name=u"最大時間")
    plus_per_hour = models.IntegerField(default=0, editable=False, verbose_name=u"増（円）")
    minus_per_hour = models.IntegerField(default=0, editable=False, verbose_name=u"減（円）")
    price = models.IntegerField(default=0, verbose_name=u"価格")
    comment = models.CharField(blank=True, null=True, max_length=50, verbose_name=u"備考")

    objects = PublicManager(is_deleted=False, project_member__is_deleted=False)

    class Meta:
        ordering = ['project_member', 'year', 'month']
        unique_together = ('project_member', 'year', 'month')
        verbose_name = verbose_name_plural = u"勤務時間"
        permissions = (
            ('input_attendance', u'勤怠入力'),
        )

    def __unicode__(self):
        return u"%s %s %s" % (self.project_member, self.get_year_display(), self.get_month_display())

    def get_night_allowance(self):
        """深夜手当を取得する

        :return:
        """
        contract = self.get_contract()
        if self.night_days and self.night_days > 0:
            if contract and contract.member_type in (1, 2):
                return int(self.night_days) * 3000
            else:
                return 0
        else:
            return 0

    def get_contract(self):
        date = datetime.datetime(int(self.year), int(self.month), 1, tzinfo=common.get_tz_utc())
        return self.project_member.member.get_contract(date)

    def get_total_hours_cost(self):
        """コスト算出時、社内は30分ごとに計算されている。

        規定としては30分ですが、システム設定では変更できます。

        :return:
        """
        attendance_type = Config.get_bp_attendance_type()
        return common.get_attendance_total_hours(self.total_hours, attendance_type)

    def get_cost(self):
        """コストを取得する

        :return:
        """
        contract = self.get_contract()
        if contract:
            if contract.is_hourly_pay:
                return int(contract.get_cost() * self.get_total_hours_cost())
            else:
                return contract.get_cost()
        return 0

    def get_bonus(self):
        """ボーナスを取得する。

        正社員の場合はボーナスある。

        :return:
        """
        return 0

    def get_overtime(self, contract=None):
        if contract is None:
            contract = self.get_contract()
        if contract:
            total_hours = self.get_total_hours_cost()
            if contract.allowance_time_min <= total_hours <= contract.allowance_time_max:
                return 0
            elif contract.is_fixed_cost or contract.is_hourly_pay:
                return 0
            elif self.project_member.project.is_reserve:
                # 待機案件の場合、残業と欠勤を計算する必要がない。
                return 0
            elif total_hours > contract.allowance_time_max:
                overtime = total_hours - contract.allowance_time_max
                return overtime
            else:
                absenteeism = total_hours - contract.allowance_time_min
                return absenteeism
        else:
            return 0

    def get_overtime_cost(self):
        """残業／控除の金額を取得する

        :return:
        """
        contract = self.get_contract()
        if contract:
            if self.project_member.member.employee_id == 'BP01126':
                pass
            total_hours = self.get_total_hours_cost()
            if contract.allowance_time_min <= total_hours <= contract.allowance_time_max:
                return 0
            elif self.project_member.project.is_reserve:
                # 待機案件の場合、残業と欠勤を計算する必要がない。
                return 0
            elif total_hours > contract.allowance_time_max:
                overtime = total_hours - contract.allowance_time_max
                return int(overtime * contract.allowance_overtime)
            else:
                absenteeism = total_hours - contract.allowance_time_min
                return int(absenteeism * contract.allowance_absenteeism)
        else:
            return 0

    def get_employment_insurance(self):
        """雇用保険を取得する

        :return:
        """
        if self.project_member.member.member_type in (1, 2):
            # 正社員、契約社員の場合
            cost = float(self.get_cost())
            bonus = float(self.get_bonus())
            allowance = float(self.allowance) if self.allowance else 0
            night_allowance = float(self.get_night_allowance())
            overtime_cost = self.get_overtime_cost()
            traffic_cost = float(self.traffic_cost) if self.traffic_cost else 0
            return int((cost + bonus + allowance + night_allowance + overtime_cost + traffic_cost) * 0.01)
        else:
            return 0

    def get_health_insurance(self):
        """健康保険を取得する

        :return:
        """
        contract = self.get_contract()
        if contract and hasattr(contract, 'endowment_insurance') \
                and contract.endowment_insurance == "1" and contract.member_type != 4:
            # 契約情報保険加入した場合
            cost = float(self.get_cost())
            bonus = float(self.get_bonus())
            allowance = float(self.allowance) if self.allowance else 0
            night_allowance = float(self.get_night_allowance())
            overtime_cost = self.get_overtime_cost()
            traffic_cost = float(self.traffic_cost) if self.traffic_cost else 0
            return int((cost + bonus + allowance + night_allowance + overtime_cost + traffic_cost) * 0.14)
        else:
            return 0

    def get_all_cost(self):
        """原価合計を取得する

        原価合計 = 月給 + 手当 + 深夜手当 + 残業／控除 + 交通費 + 経費 + 雇用／労災 + 健康／厚生

        :return:
        """
        return sum((self.get_cost(),
                    int(self.allowance) if self.allowance else 0,
                    self.get_night_allowance(),
                    self.get_overtime_cost(),
                    int(self.traffic_cost) if self.traffic_cost else 0,
                    int(self.expenses) if self.expenses else 0,
                    self.get_employment_insurance(),
                    self.get_health_insurance()))

    def get_profits(self):
        """利益を取得する

        税抜きの売上 - 原価合計

        :return:
        """
        request_detail = self.get_project_request_detail()
        if request_detail:
            total_price = request_detail.total_price
            return total_price - self.get_all_cost()
        elif self.project_member.project.is_lump:
            return self.project_member.project.lump_amount - self.get_all_cost()
        elif self.project_member.project.is_reserve:
            return 0 - self.get_all_cost()
        else:
            return None

    def get_prev_attendance(self):
        """先月の出勤情報を取得する。

        :return:
        """
        prev_month = common.add_months(datetime.date(int(self.year), int(self.month), 1), -1)
        try:
            member_attendance = MemberAttendance.objects.get(project_member=self.project_member,
                                                             year="%04d" % prev_month.year,
                                                             month="%02d" % prev_month.month)
            return member_attendance
        except ObjectDoesNotExist:
            return None
        except MultipleObjectsReturned:
            return None

    def get_prev_traffic_cost(self):
        """先月の勤務交通費を取得する。

        :return:
        """
        attendance = self.get_prev_attendance()
        return attendance.traffic_cost if attendance else None

    def get_prev_allowance(self):
        """先月の手当を取得する。

        :return:
        """
        attendance = self.get_prev_attendance()
        return attendance.allowance if attendance else None

    def get_project_request_detail(self):
        """メンバーの出勤情報によて、案件の請求情報を取得する。

        :return: ProjectRequestDetailのQueryset
        """
        try:
            return ProjectRequestDetail.objects.get(project_member=self.project_member,
                                                    project_request__year=self.year,
                                                    project_request__month=self.month)
        except ObjectDoesNotExist:
            return None
        except MultipleObjectsReturned:
            return None

    def get_lump_project_request(self):
        """一括案件の請求情報を取得する

        経営データ統計表の売上を表示するために使われている。

        :return:
        """
        if self.project_member.project.is_lump:
            try:
                project_request = ProjectRequest.objects.get(
                    project=self.project_member.project,
                    year=self.year,
                    month=self.month
                )
            except (ObjectDoesNotExist, MultipleObjectsReturned):
                project_request = None
            return project_request
        else:
            return None

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.pk is None:
            self.basic_price = self.project_member.price
            self.min_hours = self.project_member.min_hours
            self.max_hours = self.project_member.max_hours
            self.plus_per_hour = self.project_member.plus_per_hour
            self.minus_per_hour = self.project_member.minus_per_hour
        super(MemberAttendance, self).save(force_insert, force_update, using, update_fields)


class BpMemberOrder(BaseModel):
    project_member = models.ForeignKey(ProjectMember, on_delete=models.PROTECT, verbose_name=u"案件メンバー")
    subcontractor = models.ForeignKey(Subcontractor, on_delete=models.PROTECT, verbose_name=u"協力会社")
    order_no = models.CharField(max_length=14, unique=True, verbose_name=u"注文番号")
    year = models.CharField(max_length=4, default=str(datetime.date.today().year),
                            choices=constants.CHOICE_ATTENDANCE_YEAR, verbose_name=u"対象年")
    month = models.CharField(max_length=2, choices=constants.CHOICE_ATTENDANCE_MONTH, verbose_name=u"対象月")
    filename = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"注文書ファイル名")
    filename_request = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"注文請書")
    created_user = models.ForeignKey(User, related_name='created_orders', null=True, on_delete=models.PROTECT,
                                     editable=False, verbose_name=u"作成者")
    updated_user = models.ForeignKey(User, related_name='updated_orders', null=True, on_delete=models.PROTECT,
                                     editable=False, verbose_name=u"更新者")

    class Meta:
        unique_together = ('project_member', 'year', 'month')
        verbose_name = verbose_name_plural = u"ＢＰ註文書"

    def __unicode__(self):
        return u"%s(%s)" % (unicode(self.project_member.member), self.order_no)

    @classmethod
    def get_next_bp_order(cls, project_member, year, month, publish_date=None):
        """指定メンバー、年月によって、注文情報を取得する。

        :param project_member:
        :param year:
        :param month:
        :param publish_date:
        :return:
        """
        try:
            order = BpMemberOrder.objects.get(project_member=project_member,
                                              year=year,
                                              month="%02d" % int(month))
        except ObjectDoesNotExist:
            salesperson = project_member.member.get_salesperson(datetime.date(int(year), int(month), 20))
            order = BpMemberOrder(project_member=project_member,
                                  subcontractor=project_member.member.subcontractor,
                                  order_no=BpMemberOrder.get_next_order_no(salesperson, year, month, publish_date),
                                  year=year,
                                  month="%02d" % int(month))
        return order

    @classmethod
    def get_next_order_no(cls, member, year=None, month=None, publish_date=None):
        """注文番号を取得する。

        :param member ログインしているユーザ
        :param year:
        :param month
        :param publish_date:
        """
        prefix = '-'
        date = datetime.date.today()
        if year and month:
            date = common.get_bp_order_publish_date(year, month, publish_date)
        if member and member.first_name_en:
            prefix = member.first_name_en[0].upper()

        order_no = "EB{0:04d}{1:02d}{2:02d}{3}".format(date.year, date.month, date.day, prefix)
        max_order_no = BpMemberOrder.objects.public_filter(order_no__startswith=order_no)\
            .aggregate(Max('order_no'))
        max_order_no = max_order_no.get('order_no__max')
        if max_order_no:
            index = int(max_order_no[-2:]) + 1
        else:
            index = 1
        return "{0}{1:02d}".format(order_no, index)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, data=None, is_request=False):
        super(BpMemberOrder, self).save(force_insert, force_update, using, update_fields)
        # 注文書作成時、注文に関する全ての情報を履歴として保存する。
        if data:
            # 既存のデータを全部消す。
            if hasattr(self, 'bpmemberorderheading'):
                self.bpmemberorderheading.delete()
            heading = BpMemberOrderHeading(bp_order=self,
                                           publish_date=data['DETAIL'].get('PUBLISH_DATE', None),
                                           subcontractor_name=data['DETAIL'].get('SUBCONTRACTOR_NAME', None),
                                           company_address1=data['DETAIL'].get('ADDRESS1', None),
                                           company_address2=data['DETAIL'].get('ADDRESS2', None),
                                           company_name=data['DETAIL'].get('COMPANY_NAME', None),
                                           company_tel=data['DETAIL'].get('TEL', None),
                                           project_name=data['DETAIL'].get('PROJECT_NAME', None),
                                           start_date=data['DETAIL'].get('START_DATE', None),
                                           end_date=data['DETAIL'].get('END_DATE', None),
                                           master=data['DETAIL'].get('MASTER', None),
                                           middleman=data['DETAIL'].get('MIDDLEMAN', None),
                                           subcontractor_master=data['DETAIL'].get('SUBCONTRACTOR_MASTER', None),
                                           subcontractor_middleman=data['DETAIL'].get('SUBCONTRACTOR_MIDDLEMAN', None),
                                           member_name=data['DETAIL'].get('MEMBER_NAME', None),
                                           location=data['DETAIL'].get('LOCATION', None),
                                           is_hourly_pay=data['DETAIL'].get('IS_HOURLY_PAY', False),
                                           is_fixed_cost=data['DETAIL'].get('IS_FIXED_COST', False),
                                           is_show_formula=data['DETAIL'].get('IS_SHOW_FORMULA', False),
                                           allowance_base=data['DETAIL'].get('ALLOWANCE_BASE', None),
                                           allowance_base_memo=data['DETAIL'].get('ALLOWANCE_BASE_MEMO', None),
                                           allowance_time_min=data['DETAIL'].get('ALLOWANCE_TIME_MIN', None),
                                           allowance_time_max=data['DETAIL'].get('ALLOWANCE_TIME_MAX', None),
                                           allowance_time_memo=data['DETAIL'].get('ALLOWANCE_TIME_MEMO', None),
                                           allowance_overtime=data['DETAIL'].get('ALLOWANCE_OVERTIME', None),
                                           allowance_overtime_memo=data['DETAIL'].get('ALLOWANCE_OVERTIME_MEMO', None),
                                           allowance_absenteeism=data['DETAIL'].get('ALLOWANCE_ABSENTEEISM', None),
                                           allowance_absenteeism_memo=data['DETAIL'].get('ALLOWANCE_ABSENTEEISM_MEMO',
                                                                                         None),
                                           comment=data['DETAIL'].get('COMMENT', None),
                                           delivery_properties_comment=data['DETAIL'].get('DELIVERY_PROPERTIES', None),
                                           payment_condition_comments=data['DETAIL'].get('PAYMENT_CONDITION', None),
                                           contract_items_comments=data['DETAIL'].get('CONTRACT_ITEMS', None),
                                           )
            heading.save()


class BpMemberOrderHeading(models.Model):
    bp_order = models.OneToOneField(BpMemberOrder, verbose_name=u"ＢＰ注文書")
    publish_date = models.CharField(max_length=200, verbose_name=u"発行年月日")
    subcontractor_name = models.CharField(blank=True, null=True, max_length=50, verbose_name=u"下請け会社名")
    subcontractor_post_code = models.CharField(blank=True, null=True, max_length=8, verbose_name=u"協力会社郵便番号")
    subcontractor_address1 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"協力会社住所１")
    subcontractor_address2 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"協力会社住所２")
    subcontractor_tel = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"協力会社電話番号")
    subcontractor_fax = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"協力会社ファックス")
    company_address1 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"本社住所１")
    company_address2 = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"本社住所２")
    company_name = models.CharField(blank=True, null=True, max_length=30, verbose_name=u"会社名")
    company_tel = models.CharField(blank=True, null=True, max_length=15, verbose_name=u"お客様電話番号")
    project_name = models.CharField(blank=True, null=True, max_length=50, verbose_name=u"業務名称")
    start_date = models.CharField(blank=True, null=True, max_length=20, verbose_name=u"作業開始日")
    end_date = models.CharField(blank=True, null=True, max_length=20, verbose_name=u"作業終了日")
    master = models.CharField(blank=True, null=True, max_length=30, verbose_name=u"委託業務責任者（甲）")
    middleman = models.CharField(blank=True, null=True, max_length=30, verbose_name=u"連絡窓口担当者（甲）")
    subcontractor_master = models.CharField(blank=True, null=True, max_length=30, verbose_name=u"委託業務責任者（乙）")
    subcontractor_middleman = models.CharField(blank=True, null=True, max_length=30,
                                               verbose_name=u"連絡窓口担当者（乙）")
    member_name = models.CharField(blank=True, null=True, max_length=30, verbose_name=u"作業責任者")
    location = models.CharField(blank=True, null=True, max_length=200, verbose_name=u"作業場所")
    is_hourly_pay = models.BooleanField(default=False, verbose_name=u"時給")
    is_fixed_cost = models.BooleanField(default=False, verbose_name=u"固定")
    is_show_formula = models.BooleanField(default=True, verbose_name=u"計算式")
    allowance_base = models.CharField(blank=True, null=True, max_length=20, verbose_name=u"基本給")
    allowance_base_memo = models.CharField(blank=True, null=True, max_length=255, verbose_name=u"基本給メモ")
    allowance_time_min = models.CharField(blank=True, null=True, max_length=20, verbose_name=u"時間下限")
    allowance_time_max = models.CharField(blank=True, null=True, max_length=20, verbose_name=u"時間上限")
    allowance_time_memo = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"基準時間メモ")
    allowance_overtime = models.CharField(blank=True, null=True, max_length=20, verbose_name=u"残業手当")
    allowance_overtime_memo = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"残業手当メモ")
    allowance_absenteeism = models.CharField(blank=True, null=True, max_length=20, verbose_name=u"欠勤手当")
    allowance_absenteeism_memo = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"欠勤手当メモ")
    allowance_other = models.CharField(blank=True, null=True, max_length=20, verbose_name=u"その他手当")
    allowance_other_memo = models.CharField(blank=True, null=True, max_length=255, verbose_name=u"その他手当メモ")
    comment = models.TextField(blank=True, null=True, verbose_name=u"備考")
    delivery_properties_comment = models.CharField(blank=True, null=True, max_length=255, verbose_name=u"納入物件")
    payment_condition_comments = models.TextField(blank=True, null=True, verbose_name=u"支払条件")
    contract_items_comments = models.TextField(blank=True, null=True, verbose_name=u"契約条項")

    class Meta:
        verbose_name = verbose_name_plural = u"ＢＰ註文書見出し"

    def __unicode__(self):
        return unicode(self.bp_order)


class BpMemberOrderInfo(BaseModel):
    member = models.ForeignKey(Member, on_delete=models.PROTECT, verbose_name=u"協力社員")
    year = models.CharField(max_length=4, default=str(datetime.date.today().year),
                            choices=constants.CHOICE_ATTENDANCE_YEAR, verbose_name=u"対象年")
    month = models.CharField(max_length=2, choices=constants.CHOICE_ATTENDANCE_MONTH, verbose_name=u"対象月")
    min_hours = models.DecimalField(max_digits=5, decimal_places=2, default=160, verbose_name=u"基準時間")
    max_hours = models.DecimalField(max_digits=5, decimal_places=2, default=180, verbose_name=u"最大時間")
    plus_per_hour = models.IntegerField(default=0, verbose_name=u"増（円）")
    minus_per_hour = models.IntegerField(default=0, verbose_name=u"減（円）")
    cost = models.IntegerField(null=False, default=0, verbose_name=u"コスト")
    comment = models.CharField(blank=True, null=True, max_length=50, verbose_name=u"備考")

    class Meta:
        ordering = ['member', 'year', 'month']
        unique_together = ('member', 'year', 'month')
        verbose_name = verbose_name_plural = u"協力社員の注文情報"

    def __unicode__(self):
        return u"%s_%s(%s/%s)" % (unicode(self.member), unicode(self.member.subcontractor), self.year, self.month)


class Degree(BaseModel):
    member = models.ForeignKey(Member, on_delete=models.PROTECT, verbose_name=u"社員")
    start_date = models.DateField(verbose_name=u"入学日")
    end_date = models.DateField(verbose_name=u"卒業日")
    description = models.CharField(blank=True, null=True, max_length=255, verbose_name=u"学校名称/学部/専門/学位")

    class Meta:
        verbose_name = verbose_name_plural = u"学歴"


class HistoryProject(BaseModel):
    name = models.CharField(max_length=50, verbose_name=u"案件名称")
    member = models.ForeignKey(Member, on_delete=models.PROTECT, verbose_name=u"名前")
    location = models.CharField(max_length=20, blank=True, null=True, verbose_name=u"作業場所")
    description = models.TextField(blank=True, null=True, verbose_name=u"案件概要")
    start_date = models.DateField(blank=True, null=True, verbose_name=u"開始日")
    end_date = models.DateField(blank=True, null=True, verbose_name=u"終了日")
    os = models.ManyToManyField(OS, blank=True, verbose_name=u"機種／OS")
    skill = models.ManyToManyField(Skill, blank=True, verbose_name=u"スキル要求")
    role = models.CharField(default="PG", max_length=2, choices=constants.CHOICE_PROJECT_ROLE, verbose_name=u"作業区分")
    stages = models.ManyToManyField(ProjectStage, blank=True, verbose_name=u"作業工程")

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


class Issue(BaseModel):
    title = models.CharField(max_length=30, verbose_name=u"タイトル")
    level = models.PositiveSmallIntegerField(choices=constants.CHOICE_ISSUE_LEVEL, default=1, verbose_name=u"優先度")
    content = models.TextField(verbose_name=u"内容")
    created_user = models.ForeignKey(User, related_name='created_issue_set', editable=False,
                                     on_delete=models.PROTECT, verbose_name=u"作成者")
    present_user = models.ForeignKey(User, blank=False, null=True, related_name='present_issue_set',
                                     on_delete=models.PROTECT,
                                     verbose_name=u"提出者")
    observer = models.ManyToManyField(User, blank=True, verbose_name=u"観察者",
                                      help_text=u"ここで選択されたユーザーに対して、"
                                                u"課題に変更があったら自動的メールを送信します。")
    status = models.CharField(max_length=1, default=1, choices=constants.CHOICE_ISSUE_STATUS,
                              verbose_name=u"ステータス")
    limit_date = models.DateField(blank=True, null=True, verbose_name=u"期限日")
    resolve_user = models.ForeignKey(User, related_name='resolve_issue_set', blank=False, null=True,
                                     on_delete=models.PROTECT,
                                     verbose_name=u"担当者")
    planned_end_date = models.DateField(blank=True, null=True, verbose_name=u"予定完了日")
    really_end_date = models.DateField(blank=True, null=True, verbose_name=u"実際完了日")
    solution = models.TextField(blank=True, null=True, verbose_name=u"対応方法")

    class Meta:
        ordering = ['-id']
        verbose_name = verbose_name_plural = u"課題管理表"

    def __unicode__(self):
        return self.title

    def get_mail_title(self):
        return u"【営業支援システム】[課題管理] #%d: %s - %s" % (self.pk, self.title, self.get_status_display())

    def get_mail_body(self, updated_user):
        """課題のメール本文を取得する。

        :param updated_user:
        :return:
        """
        mail_body = Config.get(constants.CONFIG_ISSUE_MAIL_BODY)
        if mail_body:
            t = Template(mail_body)
            context = {'issue': self,
                       'updated_user': updated_user,
                       'domain': Config.get(constants.CONFIG_DOMAIN_NAME),
                       }
            ctx = Context(context)
            return t.render(ctx)
        else:
            return None

    def get_cc_list(self):
        # システム管理者を取得する
        users = User.objects.filter(is_superuser=True, is_active=True)
        mail_list = [user.email for user in users if user.email]
        # 担当者をメールリストに追加
        if self.resolve_user and self.resolve_user.email not in mail_list:
            mail_list.append(self.resolve_user.email)
        for observer in self.observer.all():
            if observer.email not in mail_list:
                mail_list.append(observer.email)
        return mail_list

    def send_mail(self, updated_user):
        # メール送信
        html = self.get_mail_body(updated_user)
        if not html:
            # メール本文が設定されてないなら、送信を行わずに処理を終了する。
            return
        attachments = []
        from_email = Config.get(constants.CONFIG_ADMIN_EMAIL_ADDRESS)
        recipient_list = [updated_user.email]
        cc_list = self.get_cc_list()
        mail_connection = BatchManage.get_custom_connection()
        email = EmailMultiAlternativesWithEncoding(
            subject=self.get_mail_title(),
            body="",
            from_email=from_email,
            to=recipient_list,
            cc=cc_list,
            connection=mail_connection
        )
        if html:
            email.attach_alternative(html, constants.MIME_TYPE_HTML)
        if attachments:
            for filename, content, mimetype in attachments:
                email.attach(filename, content, mimetype)
        email.send()


class History(BaseModel):
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


class BatchManage(BaseModel):
    name = models.CharField(max_length=50, unique=True, verbose_name=u"バッチＩＤ")
    title = models.CharField(max_length=50, verbose_name=u"バッチタイトル")
    cron_tab = models.CharField(blank=True, null=True, max_length=100, verbose_name=u"バッチの実行タイミング")
    is_active = models.BooleanField(default=True, verbose_name=u"有効フラグ")
    mail_title = models.CharField(max_length=50, verbose_name=u"送信メールのタイトル")
    mail_body = models.TextField(blank=True, null=True, verbose_name=u"メール本文(Plain Text)")
    mail_html = models.TextField(blank=True, null=True, verbose_name=u"メール本文(HTML)")
    attachment1 = models.FileField(blank=True, null=True, upload_to="./attachment", verbose_name=u"添付ファイル１",
                                   help_text=u"メール送信時の添付ファイルその１。")
    attachment2 = models.FileField(blank=True, null=True, upload_to="./attachment", verbose_name=u"添付ファイル２",
                                   help_text=u"メール送信時の添付ファイルその２。")
    attachment3 = models.FileField(blank=True, null=True, upload_to="./attachment", verbose_name=u"添付ファイル３",
                                   help_text=u"メール送信時の添付ファイルその３。")
    is_send_to_boss = models.BooleanField(default=True, verbose_name=u"上司に送る")
    is_send_to_self = models.BooleanField(default=True, verbose_name=u"自分に送る")
    description = models.TextField(blank=True, null=True, verbose_name=u"説明")

    class Meta:
        verbose_name = verbose_name_plural = u"バッチ管理"

    def __unicode__(self):
        return self.title

    def get_logger(self):
        return logging.getLogger('eb.management.commands.%s' % (self.name,))

    @classmethod
    def get_log_entry_user(cls, username='batch'):
        """ログエントリーにログを記録するにはログインユーザが必要

        :return:
        """
        try:
            user = User.objects.get(username=username)
            return user
        except ObjectDoesNotExist:
            try:
                user = User.objects.get(username='admin')
                return user
            except ObjectDoesNotExist:
                return None

    def get_formatted_batch(self, context):
        """フォーマット後のバッチを返す

        メールタイトルに日付追加とか、メール本文にパラメーターなどを設定する。

        :param context:
        :return:
        """
        today = datetime.datetime.now()
        # FROM
        from_email = Config.get(constants.CONFIG_ADMIN_EMAIL_ADDRESS)
        title = self.mail_title + today.strftime(u"_%y%m%d")
        # BODY
        t = Template(self.mail_body)
        ctx = Context(context)
        body = t.render(ctx)
        # HTML
        t = Template(self.mail_html)
        ctx = Context(context)
        html = t.render(ctx)

        return from_email, title, body, html

    def get_cc_list(self):
        batch_carbon_copies = self.batchcarboncopy_set.public_all()
        cc_list = []
        for cc in batch_carbon_copies:
            if cc.member and cc.member.email:
                cc_list.append(cc.member.email)
            if cc.salesperson and cc.salesperson.email:
                cc_list.append(cc.salesperson.email)
            if cc.email:
                cc_list.append(cc.email)
        return cc_list

    def send_notify_mail(self, context, recipient_list, attachments=None, no_cc=False):
        logger = self.get_logger()
        if not recipient_list:
            logger.warning(u"宛先が空白になっている。")
            return False
        from_email, title, body, html = self.get_formatted_batch(context)
        mail_connection = BatchManage.get_custom_connection()
        cc_list = [] if no_cc else self.get_cc_list()
        email = EmailMultiAlternativesWithEncoding(
            subject=title,
            body=body,
            from_email=from_email,
            to=recipient_list,
            cc=cc_list,
            connection=mail_connection
        )
        if html:
            email.attach_alternative(html, constants.MIME_TYPE_HTML)
        if attachments:
            for filename, content, mimetype in attachments:
                email.attach(filename, content, mimetype)
        email.send()
        log_format = u"題名: %s; FROM: %s; TO: %s; CC: %s; 送信完了。"
        logger.info(log_format % (title, from_email, ','.join(recipient_list), ','.join(cc_list)))

    @staticmethod
    def get_custom_connection():
        host = Config.get(constants.CONFIG_ADMIN_EMAIL_SMTP_HOST, default_value='smtp.e-business.co.jp')
        port = Config.get(constants.CONFIG_ADMIN_EMAIL_SMTP_PORT, default_value=587)
        username = Config.get(constants.CONFIG_ADMIN_EMAIL_ADDRESS)
        password = Config.get(constants.CONFIG_ADMIN_EMAIL_PASSWORD)
        backend = get_connection()
        backend.host = str(host)
        backend.port = int(port)
        backend.username = str(username)
        backend.password = str(password)
        return backend


class BatchCarbonCopy(BaseModel):
    batch = models.ForeignKey(BatchManage, on_delete=models.PROTECT, verbose_name=u"バッチ名")
    member = models.ForeignKey(Member, blank=True, null=True, on_delete=models.PROTECT, verbose_name=u"ＣＣ先の社員")
    salesperson = models.ForeignKey(Salesperson, blank=True, null=True, on_delete=models.PROTECT,
                                    verbose_name=u"ＣＣ先の営業員")
    email = models.EmailField(blank=True, null=True, verbose_name=u"メールアドレス")

    class Meta:
        ordering = ['batch']
        verbose_name = verbose_name_plural = u"バッチ送信時のＣＣリスト"

    def __unicode__(self):
        if self.member:
            return self.member.__unicode__()
        elif self.salesperson:
            return self.salesperson.__unicode__()
        else:
            return self.email


class PushNotification(BaseModel):
    user = models.ForeignKey(User, verbose_name=u"ユーザー")
    registration_id = models.CharField(max_length=1000, verbose_name=u"デバイスの登録ＩＤ")
    key_auth = models.CharField(max_length=100)
    key_p256dh = models.CharField(max_length=256)
    title = models.CharField(blank=True, null=True, max_length=100)
    message = models.CharField(blank=True, null=True, max_length=256)

    class Meta:
        ordering = ['user']
        verbose_name = verbose_name_plural = u"プッシュ通知"


class EmailMultiAlternativesWithEncoding(EmailMultiAlternatives):
    def _create_attachment(self, filename, content, mimetype=None):
        """
        Converts the filename, content, mimetype triple into a MIME attachment
        object. Use self.encoding when handling text attachments.
        """
        if mimetype is None:
            mimetype, _ = mimetypes.guess_type(filename)
            if mimetype is None:
                mimetype = constants.MIME_TYPE_EXCEL
        basetype, subtype = mimetype.split('/', 1)
        if basetype == 'text':
            encoding = self.encoding or settings.DEFAULT_CHARSET
            attachment = SafeMIMEText(smart_str(content, settings.DEFAULT_CHARSET), subtype, encoding)
        else:
            # Encode non-text attachments with base64.
            attachment = MIMEBase(basetype, subtype)
            attachment.set_payload(content)
            encoders.encode_base64(attachment)
        if filename:
            try:
                filename = filename.encode('ascii')
            except UnicodeEncodeError:
                filename = Header(filename, 'utf-8').encode()
            attachment.add_header('Content-Disposition', 'attachment', filename=filename)
        return attachment


def get_all_members(date=None):
    if date is None or date.strftime('%Y%m') == datetime.date.today().strftime('%Y%m'):
        first_day = last_day = datetime.date.today()
    else:
        first_day = common.get_first_day_by_month(date)
        last_day = common.get_last_day_by_month(date)
    query_set = Member.objects.filter(
        Q(join_date__isnull=True) | Q(join_date__lte=last_day),
        Q(membersectionperiod__division__is_on_sales=True) |
        Q(membersectionperiod__section__is_on_sales=True) |
        Q(membersectionperiod__subsection__is_on_sales=True),
        membersectionperiod__is_deleted=False
    ).annotate(
        sales_off_period_pk=Subquery(
            MemberSalesOffPeriod.objects.filter(
                (Q(start_date__lte=last_day) & Q(end_date__isnull=True)) |
                (Q(start_date__lte=last_day) & Q(end_date__gte=first_day)),
                member=OuterRef('pk')
            ).values('pk'),
            output_field=models.IntegerField()
        )
    ).distinct()
    # 現在所属の部署を取得
    section_set = MemberSectionPeriod.objects.filter((Q(start_date__lte=last_day) & Q(end_date__isnull=True)) |
                                                     (Q(start_date__lte=last_day) & Q(end_date__gte=first_day)))
    # 現在所属の営業員を取得
    salesperson_set = MemberSalespersonPeriod.objects.filter((Q(start_date__lte=last_day) & Q(end_date__isnull=True)) |
                                                             (Q(start_date__lte=last_day) & Q(end_date__gte=first_day)))
    salesoff_set = MemberSalesOffPeriod.objects.filter(
        (Q(start_date__lte=last_day) & Q(end_date__isnull=True)) |
        (Q(start_date__lte=last_day) & Q(end_date__gte=first_day))
    )
    return query_set.prefetch_related(
        Prefetch('membersectionperiod_set', queryset=section_set, to_attr='current_section_period'),
        Prefetch('membersalespersonperiod_set', queryset=salesperson_set, to_attr='current_salesperson_period'),
        Prefetch('membersalesoffperiod_set', queryset=salesoff_set, to_attr='current_salesoff_period'),
    ).extra(select={
        'last_end_date': "select max(pm.end_date) "
                         "  from eb_projectmember pm "
                         "  join eb_project p on p.id = pm.project_id"
                         " where pm.member_id = eb_member.id "
                         "   and pm.is_deleted = 0 "
                         "   and pm.status = 2"
                         "   and p.is_reserve = 0",
        'is_working': "select count(1)"
                      "  from eb_projectmember pm"
                      "  join eb_project p on p.id = pm.project_id"
                      " where pm.member_id = eb_member.id"
                      "   and pm.status = 2"
                      "   and pm.is_deleted = 0"
                      "   and pm.start_date <= '%s'"
                      "   and pm.end_date >= '%s'"
                      "   and p.is_reserve = 0" % (last_day, first_day),
        'planning_count': "select count(*) "
                          "  from eb_projectmember pm "
                          " where pm.member_id = eb_member.id "
                          "   and pm.is_deleted = 0 "
                          "   and pm.status = 1",
    })


def get_sales_members(date=None):
    """現在の営業対象のメンバーを取得する。

    加入日は現在以前、かつ所属部署は営業対象部署になっている

    :return: MemberのQueryset
    """
    if date is None:
        date = datetime.date.today()
    first_day = common.get_first_day_by_month(date)
    return get_all_members(date).filter(Q(is_retired=False) | (Q(is_retired=True) & Q(retired_date__gt=first_day)))


def get_on_sales_members(date=None):
    """現在の営業対象のメンバーを取得する。

    加入日は現在以前、かつ所属部署は営業対象部署、かつ該当社員は営業対象中になっている

    :return: MemberのQueryset
    """
    if date is None:
        date = datetime.date.today()
    query_set = get_sales_members(date).filter(
        Q(membersalesoffperiod__isnull=True) |
        Q(membersalesoffperiod__end_date__lt=date) |
        (Q(membersalesoffperiod__start_date__gt=date) & Q(membersalesoffperiod__is_deleted=False))
    ).distinct()
    return query_set


def get_off_sales_members(date=None):
    """現在の営業対象外のメンバーを取得する。

    加入日は現在以前、かつ所属部署は営業対象部署、かつ該当社員は営業対象外になっている

    :return: MemberのQueryset
    """
    query_set = get_sales_members(date).filter(sales_off_period_pk__isnull=False)
    return query_set


def get_working_members(date=None):
    """指定日付の稼働中のメンバーを取得する

    日付は指定してない場合は本日とする。

    :param date: 対象年月
    :return: MemberのQueryset
    """
    if not date or date.strftime('%Y%m') == datetime.date.today().strftime('%Y%m'):
        first_day = last_day = datetime.date.today()
    else:
        first_day = common.get_first_day_by_month(date)
        last_day = common.get_last_day_by_month(date)
    members = get_on_sales_members(date).filter(projectmember__start_date__lte=last_day,
                                                projectmember__end_date__gte=first_day,
                                                projectmember__is_deleted=False,
                                                projectmember__status=2,
                                                projectmember__project__is_reserve=False).distinct()
    return members


def get_waiting_members(date=None):
    """現在待機中のメンバーを取得する

    :param date: 対象年月
    :return: MemberのQueryset
    """
    working_members = get_working_members(date)
    return get_on_sales_members(date).exclude(pk__in=working_members)


def get_project_members_by_month(date):
    """指定月の案件メンバー全部取得する。

    案件メンバーのステータスは「作業確定(2)」、該当する案件のステータスは「実施中(4)」

    :param date 指定月
    :return: ProjectMemberのQueryset
    """
    first_day = common.get_first_day_by_month(date)
    # today = datetime.date.today()
    next_2_month = common.add_months(first_day, 2)
    # if date.year == today.year and date.month == today.month:
    #     first_day = today
    last_day = common.get_last_day_by_month(date)
    query_set = ProjectMember.objects.public_filter(end_date__gte=first_day,
                                                    start_date__lte=last_day,
                                                    project__status__in=[4, 5],
                                                    project__is_reserve=False,
                                                    status=2)
    return query_set.extra(select={
        'section_name': "select name "
                        "  from eb_section s "
                        " inner join eb_membersectionperiod msp on s.id = msp.section_id "
                        " where ((msp.start_date <= '{0}' and msp.end_date is null) "
                        "     or (msp.start_date <= '{0}' and msp.end_date >= '{0}')) "
                        "   and msp.member_id = eb_projectmember.member_id "
                        "   and msp.is_deleted = 0".format(date),
        'salesperson_name': "select concat(first_name, last_name) "
                            "  from eb_salesperson s "
                            " inner join eb_membersalespersonperiod msp on s.id = msp.salesperson_id "
                            " where ((msp.start_date <= '{0}' and msp.end_date is null) "
                            "     or (msp.start_date <= '{0}' and msp.end_date >= '{0}')) "
                            "   and msp.member_id = eb_projectmember.member_id "
                            "   and msp.is_deleted = 0".format(date),
        'business_status': "select case"
                           "           when (select count(*) "
                           "                   from eb_projectmember pm2 "
                           "                  where pm2.member_id = eb_projectmember.member_id "
                           "                    and pm2.is_deleted = 0"
                           "                    and pm2.status = 1"
                           "                ) > 0 then '営業中'"
                           "           when (select count(*) "
                           "                   from eb_projectmember pm3 "
                           "                  where pm3.member_id = eb_projectmember.member_id "
                           "                    and pm3.is_deleted = 0 "
                           "                    and pm3.status = 2 "
                           "                    and pm3.end_date >= '%s' "
                           "                ) > 0 then '-' "
                           "           else '未提案' "
                           "       end " % next_2_month,
    }).distinct()


def get_release_members_by_month(date, p=None):
    """指定年月にリリースするメンバーを取得する。

    :param date 指定月
    :param p: 画面からの絞り込み条件
    :return: ProjectMemberのQueryset
    """
    # 次の月はまだ稼働中の案件メンバーは除外する。
    working_member_next_date = get_working_members(date=common.add_months(date, 1))
    project_members = get_project_members_by_month(date).filter(
        Q(member__membersectionperiod__division__is_on_sales=True) |
        Q(member__membersectionperiod__section__is_on_sales=True) |
        Q(member__membersectionperiod__subsection__is_on_sales=True),
        member__membersectionperiod__is_deleted=False,
        member__is_on_sales=True,
    ).exclude(member__in=working_member_next_date)
    if p:
        project_members = project_members.filter(**p)
    return project_members.order_by('member__first_name', 'member__last_name')


def get_release_current_month():
    """今月にリリースするメンバーを取得する

    :return: ProjectMemberのQueryset
    """
    return get_release_members_by_month(datetime.date.today())


def get_release_next_month():
    """来月にリリースするメンバーを取得する

    :return: ProjectMemberのQueryset
    """
    next_month = common.add_months(datetime.date.today(), 1)
    return get_release_members_by_month(next_month)


def get_release_next_2_month():
    """再来月にリリースするメンバーを取得する

    :return: ProjectMemberのQueryset
    """
    next_2_month = common.add_months(datetime.date.today(), 2)
    return get_release_members_by_month(next_2_month)
