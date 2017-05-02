# coding: UTF-8
from eb import models as eb_models
from django.db import models


class DelManager(models.Manager):
    def get_queryset(self):
        return super(DelManager, self).get_queryset().filter(is_deleted=True)


class EbBankinfo(eb_models.BankInfo):
    objects = DelManager()

    class Meta:
        managed = False
        proxy = True
        verbose_name = verbose_name_plural = u"銀行口座"


class EbBpmemberorderinfo(eb_models.BpMemberOrderInfo):
    objects = DelManager()

    class Meta:
        managed = False
        proxy = True
        verbose_name = verbose_name_plural = u"協力社員の注文情報"


class EbClient(eb_models.Client):
    objects = DelManager()

    class Meta:
        managed = False
        proxy = True
        verbose_name = verbose_name_plural = u"取引先"


class EbClientmember(eb_models.ClientMember):
    objects = DelManager()

    class Meta:
        managed = False
        proxy = True
        verbose_name = verbose_name_plural = u"お客様"


class EbClientorder(eb_models.ClientOrder):
    objects = DelManager()

    class Meta:
        managed = False
        proxy = True
        verbose_name = verbose_name_plural = u"お客様注文書"


class EbDegree(eb_models.Degree):
    objects = DelManager()

    class Meta:
        managed = False
        proxy = True
        verbose_name = verbose_name_plural = u"学歴"


class EbExpensescategory(eb_models.ExpensesCategory):
    objects = DelManager()

    class Meta:
        managed = False
        proxy = True
        verbose_name = verbose_name_plural = u"精算分類"


class EbHistoryproject(eb_models.HistoryProject):
    objects = DelManager()

    class Meta:
        managed = False
        proxy = True
        verbose_name = verbose_name_plural = u"以前やっていた案件"


class EbMember(eb_models.Member):
    objects = DelManager()

    class Meta:
        managed = False
        proxy = True
        verbose_name = verbose_name_plural = u"社員"


class EbMemberattendance(eb_models.MemberAttendance):
    objects = DelManager()

    class Meta:
        managed = False
        proxy = True
        verbose_name = verbose_name_plural = u"勤務時間"


class EbMemberexpenses(eb_models.MemberExpenses):
    objects = DelManager()

    class Meta:
        managed = False
        proxy = True
        verbose_name = verbose_name_plural = u"精算リスト"


class EbOs(eb_models.OS):
    objects = DelManager()

    class Meta:
        managed = False
        proxy = True
        verbose_name = verbose_name_plural = u"機種／OS"


class EbPositionship(eb_models.PositionShip):
    objects = DelManager()

    class Meta:
        managed = False
        proxy = True
        verbose_name = verbose_name_plural = u"職位"


class EbProject(eb_models.Project):
    objects = DelManager()

    class Meta:
        managed = False
        proxy = True
        verbose_name = verbose_name_plural = u"案件"


class EbProjectactivity(eb_models.ProjectActivity):
    objects = DelManager()

    class Meta:
        managed = False
        proxy = True
        verbose_name = verbose_name_plural = u"案件活動"


class EbProjectmember(eb_models.ProjectMember):
    objects = DelManager()

    class Meta:
        managed = False
        proxy = True
        verbose_name = verbose_name_plural = u"案件メンバー"


class EbProjectskill(eb_models.ProjectSkill):
    objects = DelManager()

    class Meta:
        managed = False
        proxy = True
        verbose_name = verbose_name_plural = u"案件のスキル要求"


class EbProjectstage(eb_models.ProjectStage):
    objects = DelManager()

    class Meta:
        managed = False
        proxy = True
        verbose_name = verbose_name_plural = u"作業工程"


class EbSalesoffreason(eb_models.SalesOffReason):
    objects = DelManager()

    class Meta:
        managed = False
        proxy = True
        verbose_name = verbose_name_plural = u"営業対象外理由"


class EbSalesperson(eb_models.Salesperson):
    objects = DelManager()

    class Meta:
        managed = False
        proxy = True
        verbose_name = verbose_name_plural = u"営業員"


class EbSection(eb_models.Section):
    objects = DelManager()

    class Meta:
        managed = False
        proxy = True
        verbose_name = verbose_name_plural = u"部署"


class EbSkill(eb_models.Skill):
    objects = DelManager()

    class Meta:
        managed = False
        proxy = True
        verbose_name = verbose_name_plural = u"スキル"


class EbSubcontractor(eb_models.Subcontractor):
    objects = DelManager()

    class Meta:
        managed = False
        proxy = True
        verbose_name = verbose_name_plural = u"協力会社"


class EbSubcontractororder(eb_models.BpMemberOrder):
    objects = DelManager()

    class Meta:
        managed = False
        proxy = True
        verbose_name = verbose_name_plural = u"ＢＰ註文書"
