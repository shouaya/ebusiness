# coding: UTF-8
"""
Created on 2017/04/24

@author: Yang Wanjun
"""
from __future__ import unicode_literals
import datetime

from django.db import models
from django.utils import timezone

from eb.models import Member, Config, Company, Subcontractor, BatchManage, EmailMultiAlternativesWithEncoding
from utils import constants


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


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, null=True, editable=False, verbose_name=u"作成日時")
    updated_date = models.DateTimeField(auto_now=True, editable=False, verbose_name=u"更新日時")
    is_deleted = models.BooleanField(default=False, editable=False, verbose_name=u"削除フラグ")
    deleted_date = models.DateTimeField(blank=True, null=True, editable=False, verbose_name=u"削除年月日")

    objects = PublicManager(is_deleted=False)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_date = datetime.datetime.now()
        self.save()


class Contract(BaseModel):
    member = models.ForeignKey(Member, editable=False, verbose_name=u"社員")
    company = models.ForeignKey(Company, verbose_name=u"雇用会社")
    contract_no = models.CharField(max_length=20, verbose_name=u"契約番号")
    contract_date = models.DateField(verbose_name=u"契約日", help_text=u"例：2014-01-01")
    member_type = models.IntegerField(choices=constants.CHOICE_MEMBER_TYPE, verbose_name=u"雇用形態")
    is_loan = models.BooleanField(default=False, verbose_name=u"出向")
    employment_date = models.DateField(verbose_name=u"雇用日", help_text=u"例：2014-01-01")
    start_date = models.DateField(verbose_name=u"雇用開始日")
    end_date = models.DateField(blank=True, null=True, verbose_name=u"雇用終了日")
    employment_period_comment = models.TextField(blank=True, null=True, verbose_name=u"雇用期間コメント",
                                                 default=Config.get_employment_period_comment())
    position = models.CharField(max_length=50, blank=True, null=True, verbose_name=u"職位")
    business_address = models.CharField(max_length=255, blank=True, null=True, default=Config.get_business_address(),
                                        verbose_name=u"就業の場所")
    business_type = models.CharField(max_length=2, choices=constants.CHOICE_BUSINESS_TYPE, verbose_name=u"業務の種類")
    business_other = models.TextField(blank=True, null=True, verbose_name=u"業務その他")
    business_time = models.TextField(blank=True, null=True, default=Config.get_business_time(),
                                     verbose_name=u"就業時間")
    is_hourly_pay = models.BooleanField(default=False, verbose_name=u"時給")
    allowance_base = models.IntegerField(verbose_name=u"基本給")
    allowance_base_memo = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"基本給メモ")
    allowance_base_other = models.IntegerField(default=0, verbose_name=u"基本給その他")
    allowance_base_other_memo = models.CharField(max_length=255, blank=True, null=True,
                                                 verbose_name=u"基本給その他メモ")
    allowance_work = models.IntegerField(default=0, verbose_name=u"現場手当")
    allowance_work_memo = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"現場手当メモ")
    allowance_director = models.IntegerField(default=0, verbose_name=u"役職手当")
    allowance_director_memo = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"役職手当メモ")
    allowance_position = models.IntegerField(default=0, verbose_name=u"職務手当")
    allowance_position_memo = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"職務手当メモ")
    allowance_diligence = models.IntegerField(default=0, verbose_name=u"精勤手当")
    allowance_diligence_memo = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"精勤手当メモ")
    allowance_security = models.IntegerField(default=0, verbose_name=u"安全手当")
    allowance_security_memo = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"安全手当メモ")
    allowance_qualification = models.IntegerField(default=0, verbose_name=u"資格手当")
    allowance_qualification_memo = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"資格手当メモ")
    allowance_traffic = models.IntegerField(default=0, verbose_name=u"通勤手当")
    allowance_traffic_memo = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"通勤手当メモ")
    allowance_time_min = models.IntegerField(default=160, verbose_name=u"時間下限", help_text=u"足りないなら欠勤となる")
    allowance_time_max = models.IntegerField(default=200, verbose_name=u"時間上限", help_text=u"超えたら残業となる")
    allowance_overtime = models.IntegerField(default=0, verbose_name=u"残業手当")
    allowance_overtime_memo = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"残業手当メモ")
    allowance_absenteeism = models.IntegerField(default=0, verbose_name=u"欠勤手当")
    allowance_absenteeism_memo = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"欠勤手当メモ")
    allowance_other = models.IntegerField(default=0, verbose_name=u"その他手当")
    allowance_other_memo = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"その他手当メモ")
    endowment_insurance = models.CharField(max_length=1, blank=True, null=True, verbose_name=u"社会保険加入有無",
                                           help_text=u"0:加入しない、1:加入する")
    allowance_ticket_comment = models.TextField(blank=True, null=True, verbose_name=u"諸手当")
    allowance_date_comment = models.TextField(blank=True, null=True, default=Config.get_allowance_date_comment(),
                                              verbose_name=u"給与締め切り日及び支払日")
    allowance_change_comment = models.TextField(blank=True, null=True, default=Config.get_allowance_change_comment(),
                                                verbose_name=u"昇給及び降給")
    bonus_comment = models.TextField(blank=True, null=True, default=Config.get_bonus_comment(), verbose_name=u"賞与")
    holiday_comment = models.TextField(blank=True, null=True, default=Config.get_holiday_comment(), verbose_name=u"休日")
    paid_vacation_comment = models.TextField(blank=True, null=True, default=Config.get_paid_vacation_comment(),
                                             verbose_name=u"有給休暇")
    non_paid_vacation_comment = models.TextField(blank=True, null=True, default=Config.get_no_paid_vacation_comment(),
                                                 verbose_name=u"無給休暇")
    retire_comment = models.TextField(blank=True, null=True, default=Config.get_retire_comment(),
                                      verbose_name=u"退職に関する項目")
    status = models.CharField(max_length=2, default='01', choices=constants.CHOICE_CONTRACT_STATUS,
                              verbose_name=u"契約状態")
    comment = models.TextField(blank=True, null=True, default=Config.get_contract_comment(), verbose_name=u"備考")
    move_flg = models.BooleanField(default=0, editable=False)

    class Meta:
        ordering = ['member', 'contract_no']
        verbose_name = verbose_name_plural = u"社員契約"
        db_table = 'eb_contract'

    def __unicode__(self):
        return u"%s(%s)" % (unicode(self.member), self.contract_no)

    def get_cost(self):
        """コストを取得する

        :return:
        """
        cost = self.allowance_base \
               + self.allowance_base_other \
               + self.allowance_work \
               + self.allowance_director \
               + self.allowance_position \
               + self.allowance_diligence \
               + self.allowance_security \
               + self.allowance_qualification \
               + self.allowance_other
        if self.member_type == 1:
            cost = int((cost * 14) / 12)
        return cost

    def get_next_contract_no(self):
        today = datetime.date.today()
        return "EB%04d%s" % (int(self.member.id_from_api), today.strftime('%Y%m%d'))

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Contract, self).save(force_insert, force_update, using, update_fields)
        # from_email, title, body, html = self.get_formatted_batch(context)
        # mail_connection = BatchManage.get_custom_connection()
        # recipient_list = ContractRecipient.get_recipient_list()
        # cc_list = ContractRecipient.get_cc_list()
        # bcc_list = ContractRecipient.get_bcc_list()
        # email = EmailMultiAlternativesWithEncoding(
        #     subject=title,
        #     body=body,
        #     from_email=from_email,
        #     to=recipient_list,
        #     cc=cc_list,
        #     connection=mail_connection
        # )
        # if html:
        #     email.attach_alternative(html, constants.MIME_TYPE_HTML)
        # if attachments:
        #     for filename, content, mimetype in attachments:
        #         email.attach(filename, content, mimetype)
        # email.send()


class ContractRecipient(BaseModel):
    recipient_type = models.CharField(max_length=2, default='01', choices=constants.CHOICE_RECIPIENT_TYPE,
                                      verbose_name=u"送信種類")
    member = models.ForeignKey(Member, blank=True, null=True, verbose_name=u"送信先の社員")
    email = models.EmailField(blank=True, null=True, verbose_name=u"メールアドレス")

    class Meta:
        verbose_name = verbose_name_plural = u"契約変更の受信者"
        db_table = 'eb_contractrecipient'

    def __unicode__(self):
        if self.member:
            return unicode(self.member)
        else:
            return self.email

    @classmethod
    def get_recipient_list(cls):
        return ContractRecipient.objects.public_filter(recipient_type='01')

    @classmethod
    def get_cc_list(cls):
        return ContractRecipient.objects.public_filter(recipient_type='02')

    @classmethod
    def get_bcc_list(cls):
        return ContractRecipient.objects.public_filter(recipient_type='03')


class BpContract(BaseModel):
    member = models.ForeignKey(Member, verbose_name=u"社員")
    company = models.ForeignKey(Subcontractor, verbose_name=u"雇用会社")
    member_type = models.IntegerField(default=4, editable=False, choices=constants.CHOICE_MEMBER_TYPE,
                                      verbose_name=u"雇用形態")
    start_date = models.DateField(verbose_name=u"雇用開始日")
    end_date = models.DateField(blank=True, null=True, verbose_name=u"雇用終了日")
    is_hourly_pay = models.BooleanField(default=False, verbose_name=u"時給")
    is_fixed_cost = models.BooleanField(default=False, verbose_name=u"固定")
    is_show_formula = models.BooleanField(default=True, verbose_name=u"計算式",
                                          help_text=u"注文書に超過単価と不足単価の計算式を表示するか")
    allowance_base = models.IntegerField(verbose_name=u"基本給")
    allowance_base_memo = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"基本給メモ")
    allowance_time_min = models.IntegerField(default=160, verbose_name=u"時間下限", help_text=u"足りないなら欠勤となる")
    allowance_time_max = models.IntegerField(default=200, verbose_name=u"時間上限", help_text=u"超えたら残業となる")
    allowance_time_memo = models.CharField(max_length=255, blank=True, null=True,
                                           default=u"※基準時間：160～200/月", verbose_name=u"基準時間メモ")
    calculate_type = models.CharField(default='01', max_length=2, choices=constants.CHOICE_CALCULATE_TYPE,
                                      verbose_name=u"計算種類")
    business_days = models.IntegerField(blank=True, null=True, verbose_name=u"営業日数")
    calculate_time_min = models.IntegerField(blank=True, null=True, verbose_name=u"計算用下限",
                                             help_text=u"欠勤手当を算出ために使われます。")
    calculate_time_max = models.IntegerField(blank=True, null=True, verbose_name=u"計算用上限",
                                             help_text=u"残業手当を算出ために使われます。")
    allowance_overtime = models.IntegerField(default=0, verbose_name=u"残業手当")
    allowance_overtime_memo = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"残業手当メモ")
    allowance_absenteeism = models.IntegerField(default=0, verbose_name=u"欠勤手当")
    allowance_absenteeism_memo = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"欠勤手当メモ")
    allowance_other = models.IntegerField(default=0, verbose_name=u"その他手当")
    allowance_other_memo = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"その他手当メモ")
    comment = models.TextField(blank=True, null=True,  verbose_name=u"備考")

    class Meta:
        ordering = ['company', 'member', 'start_date']
        verbose_name = verbose_name_plural = u"ＢＰ契約"
        db_table = 'eb_bp_contract'

    def __unicode__(self):
        return u"%s(%s)" % (unicode(self.member), self.start_date)

    def get_cost(self):
        """コストを取得する

        :return:
        """
        cost = self.allowance_base + self.allowance_other
        return cost

    @property
    def endowment_insurance(self):
        """他者技術者の場合、保険なし

        :return:
        """
        return '0'
