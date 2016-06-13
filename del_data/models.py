# coding: UTF-8
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from utils import constants
from django.db import models
from django.contrib.auth.models import User


class EbBankinfo(models.Model):
    bank_name = models.CharField(max_length=20)
    branch_no = models.CharField(max_length=3)
    branch_name = models.CharField(max_length=20)
    account_type = models.CharField(max_length=1)
    account_number = models.CharField(max_length=7)
    account_holder = models.CharField(max_length=20, blank=True, null=True)
    is_deleted = models.IntegerField()
    deleted_date = models.DateTimeField(blank=True, null=True)
    company = models.ForeignKey('EbCompany')

    class Meta:
        managed = False
        db_table = 'eb_bankinfo'
        unique_together = (('branch_no', 'account_number'),)


class EbBpmemberorderinfo(models.Model):
    year = models.CharField(max_length=4)
    month = models.CharField(max_length=2)
    min_hours = models.DecimalField(max_digits=5, decimal_places=2)
    max_hours = models.DecimalField(max_digits=5, decimal_places=2)
    plus_per_hour = models.IntegerField()
    minus_per_hour = models.IntegerField()
    comment = models.CharField(max_length=50, blank=True, null=True)
    is_deleted = models.IntegerField()
    deleted_date = models.DateTimeField(blank=True, null=True)
    member = models.ForeignKey('EbMember')
    cost = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'eb_bpmemberorderinfo'
        unique_together = (('member', 'year', 'month'),)


class EbClient(models.Model):
    name = models.CharField(unique=True, max_length=30)
    japanese_spell = models.CharField(max_length=30, blank=True, null=True)
    found_date = models.DateField(blank=True, null=True)
    capital = models.BigIntegerField(blank=True, null=True)
    post_code = models.CharField(max_length=7, blank=True, null=True)
    address1 = models.CharField(max_length=200, blank=True, null=True)
    address2 = models.CharField(max_length=200, blank=True, null=True)
    tel = models.CharField(max_length=15, blank=True, null=True)
    fax = models.CharField(max_length=15, blank=True, null=True)
    president = models.CharField(max_length=30, blank=True, null=True)
    employee_count = models.IntegerField(blank=True, null=True)
    sale_amount = models.BigIntegerField(blank=True, null=True)
    undertaker = models.CharField(max_length=30, blank=True, null=True)
    undertaker_mail = models.CharField(max_length=254, blank=True, null=True)
    payment_day = models.CharField(max_length=2, blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    request_file = models.CharField(max_length=100, blank=True, null=True)
    salesperson = models.ForeignKey('EbSalesperson', blank=True, null=True)
    payment_month = models.CharField(max_length=1, blank=True, null=True)
    deleted_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.IntegerField()
    decimal_type = models.CharField(max_length=1)
    tax_rate = models.DecimalField(max_digits=3, decimal_places=2)
    quotation_file = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eb_client'


class EbClientmember(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=254, blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
    client = models.ForeignKey(EbClient)
    deleted_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'eb_clientmember'


class EbClientorder(models.Model):
    name = models.CharField(max_length=50)
    order_no = models.CharField(max_length=20)
    order_file = models.CharField(max_length=100, blank=True, null=True)
    deleted_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.IntegerField()
    end_date = models.DateField()
    start_date = models.DateField()
    bank_info = models.ForeignKey(EbBankinfo, blank=True, null=True)
    order_date = models.DateField(blank=True, null=True)
    member_comma_list = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eb_clientorder'


class EbClientorderProjects(models.Model):
    clientorder = models.ForeignKey(EbClientorder)
    project = models.ForeignKey('EbProject')

    class Meta:
        managed = False
        db_table = 'eb_clientorder_projects'
        unique_together = (('clientorder', 'project'),)


class EbCompany(models.Model):
    name = models.CharField(unique=True, max_length=30)
    japanese_spell = models.CharField(max_length=30, blank=True, null=True)
    found_date = models.DateField(blank=True, null=True)
    capital = models.BigIntegerField(blank=True, null=True)
    post_code = models.CharField(max_length=7, blank=True, null=True)
    address1 = models.CharField(max_length=200, blank=True, null=True)
    address2 = models.CharField(max_length=200, blank=True, null=True)
    tel = models.CharField(max_length=15, blank=True, null=True)
    fax = models.CharField(max_length=15, blank=True, null=True)
    quotation_file = models.CharField(max_length=100, blank=True, null=True)
    request_file = models.CharField(max_length=100, blank=True, null=True)
    request_lump_file = models.CharField(max_length=100, blank=True, null=True)
    order_file = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eb_company'


class EbDegree(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.CharField(max_length=255, blank=True, null=True)
    member = models.ForeignKey('EbMember')
    deleted_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'eb_degree'


class EbExpensescategory(models.Model):
    name = models.CharField(max_length=50)
    deleted_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'eb_expensescategory'


class EbHistory(models.Model):
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    location = models.CharField(max_length=2)
    description = models.TextField()
    deleted_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'eb_history'


class EbHistoryproject(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    role = models.CharField(max_length=2)
    member = models.ForeignKey('EbMember')
    deleted_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'eb_historyproject'


class EbHistoryprojectOs(models.Model):
    historyproject = models.ForeignKey(EbHistoryproject)
    os = models.ForeignKey('EbOs')

    class Meta:
        managed = False
        db_table = 'eb_historyproject_os'
        unique_together = (('historyproject', 'os'),)


class EbHistoryprojectSkill(models.Model):
    historyproject = models.ForeignKey(EbHistoryproject)
    skill = models.ForeignKey('EbSkill')

    class Meta:
        managed = False
        db_table = 'eb_historyproject_skill'
        unique_together = (('historyproject', 'skill'),)


class EbHistoryprojectStages(models.Model):
    historyproject = models.ForeignKey(EbHistoryproject)
    projectstage = models.ForeignKey('EbProjectstage')

    class Meta:
        managed = False
        db_table = 'eb_historyproject_stages'
        unique_together = (('historyproject', 'projectstage'),)


class EbIssue(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    status = models.CharField(max_length=1)
    created_date = models.DateTimeField()
    updated_date = models.DateTimeField()
    user = models.ForeignKey(User, related_name='issue_users')
    deleted_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.IntegerField()
    end_date = models.DateField(blank=True, null=True)
    level = models.SmallIntegerField()
    limit_date = models.DateField(blank=True, null=True)
    resolve_user = models.ForeignKey(User, related_name='issue_resolve_users', blank=True, null=True)
    solution = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eb_issue'


class EbMember(models.Model):
    employee_id = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    first_name_ja = models.CharField(max_length=30, blank=True, null=True)
    last_name_ja = models.CharField(max_length=30, blank=True, null=True)
    first_name_en = models.CharField(max_length=30, blank=True, null=True)
    last_name_en = models.CharField(max_length=30, blank=True, null=True)
    sex = models.CharField(max_length=1, blank=True, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    graduate_date = models.DateField(blank=True, null=True)
    join_date = models.DateField(blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    private_email = models.CharField(max_length=254, blank=True, null=True)
    post_code = models.CharField(max_length=7, blank=True, null=True)
    address1 = models.CharField(max_length=200, blank=True, null=True)
    address2 = models.CharField(max_length=200, blank=True, null=True)
    nearest_station = models.CharField(max_length=15, blank=True, null=True)
    years_in_japan = models.IntegerField(blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
    is_married = models.CharField(max_length=1, blank=True, null=True)
    japanese_description = models.TextField(blank=True, null=True)
    certificate = models.TextField(blank=True, null=True)
    skill_description = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    member_type = models.IntegerField()
    cost = models.IntegerField()
    company = models.ForeignKey(EbCompany, blank=True, null=True)
    salesperson = models.ForeignKey('EbSalesperson', blank=True, null=True)
    section = models.ForeignKey('EbSection', blank=True, null=True)
    subcontractor = models.ForeignKey('EbSubcontractor', blank=True, null=True)
    user = models.OneToOneField(User, blank=True, null=True)
    is_retired = models.BooleanField()
    deleted_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField()
    coordinate_update_date = models.DateTimeField(blank=True, null=True)
    lat = models.CharField(max_length=25, blank=True, null=True)
    lng = models.CharField(max_length=25, blank=True, null=True)
    is_notify = models.IntegerField()
    notify_type = models.IntegerField(blank=True, null=True)
    is_individual_pay = models.IntegerField()
    is_on_sales = models.IntegerField()
    sales_off_reason = models.ForeignKey('EbSalesoffreason', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eb_member'
        ordering = ['first_name', 'last_name']
        verbose_name = verbose_name_plural = u"社員"

    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)


class EbMemberattendance(models.Model):
    year = models.CharField(max_length=4)
    month = models.CharField(max_length=2)
    total_hours = models.DecimalField(max_digits=5, decimal_places=2)
    extra_hours = models.DecimalField(max_digits=5, decimal_places=2)
    project_member = models.ForeignKey('EbProjectmember')
    price = models.IntegerField()
    rate = models.DecimalField(max_digits=3, decimal_places=2)
    comment = models.CharField(max_length=50, blank=True, null=True)
    deleted_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.IntegerField()
    basic_price = models.IntegerField()
    max_hours = models.DecimalField(max_digits=5, decimal_places=2)
    min_hours = models.DecimalField(max_digits=5, decimal_places=2)
    minus_per_hour = models.IntegerField()
    plus_per_hour = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'eb_memberattendance'
        unique_together = (('project_member', 'year', 'month'),)


class EbMemberexpenses(models.Model):
    year = models.CharField(max_length=4)
    month = models.CharField(max_length=2)
    price = models.IntegerField()
    category = models.ForeignKey(EbExpensescategory)
    project_member = models.ForeignKey('EbProjectmember')
    deleted_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'eb_memberexpenses'


class EbOs(models.Model):
    name = models.CharField(unique=True, max_length=15)
    deleted_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'eb_os'


class EbPositionship(models.Model):
    position = models.IntegerField(blank=True, null=True)
    is_part_time = models.IntegerField()
    member = models.ForeignKey(EbMember)
    section = models.ForeignKey('EbSection')
    deleted_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'eb_positionship'


class EbProject(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField()
    boss = models.ForeignKey(EbClientmember, related_name='project_bosses', blank=True, null=True)
    client = models.ForeignKey(EbClient, blank=True, null=True)
    middleman = models.ForeignKey(EbClientmember, related_name='project_middlemen', blank=True, null=True)
    salesperson = models.ForeignKey('EbSalesperson', blank=True, null=True)
    attendance_type = models.CharField(max_length=1)
    deleted_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.IntegerField()
    max_hours = models.DecimalField(max_digits=5, decimal_places=2)
    min_hours = models.DecimalField(max_digits=5, decimal_places=2)
    is_lump = models.IntegerField()
    lump_amount = models.BigIntegerField(blank=True, null=True)
    insert_date = models.DateTimeField(blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)
    lump_comment = models.CharField(max_length=200, blank=True, null=True)
    is_hourly_pay = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'eb_project'
        unique_together = (('name', 'client'),)


class EbProjectOs(models.Model):
    project = models.ForeignKey(EbProject)
    os = models.ForeignKey(EbOs)

    class Meta:
        managed = False
        db_table = 'eb_project_os'
        unique_together = (('project', 'os'),)


class EbProjectactivity(models.Model):
    name = models.CharField(max_length=30)
    open_date = models.DateTimeField()
    address = models.CharField(max_length=255)
    content = models.TextField()
    created_date = models.DateTimeField()
    project = models.ForeignKey(EbProject)
    deleted_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'eb_projectactivity'


class EbProjectactivityClientMembers(models.Model):
    projectactivity = models.ForeignKey(EbProjectactivity)
    clientmember = models.ForeignKey(EbClientmember)

    class Meta:
        managed = False
        db_table = 'eb_projectactivity_client_members'
        unique_together = (('projectactivity', 'clientmember'),)


class EbProjectactivityMembers(models.Model):
    projectactivity = models.ForeignKey(EbProjectactivity)
    member = models.ForeignKey(EbMember)

    class Meta:
        managed = False
        db_table = 'eb_projectactivity_members'
        unique_together = (('projectactivity', 'member'),)


class EbProjectactivitySalesperson(models.Model):
    projectactivity = models.ForeignKey(EbProjectactivity)
    salesperson = models.ForeignKey('EbSalesperson')

    class Meta:
        managed = False
        db_table = 'eb_projectactivity_salesperson'
        unique_together = (('projectactivity', 'salesperson'),)


class EbProjectmember(models.Model):
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    price = models.IntegerField()
    min_hours = models.DecimalField(max_digits=5, decimal_places=2)
    max_hours = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.IntegerField()
    role = models.CharField(max_length=2)
    member = models.ForeignKey(EbMember)
    project = models.ForeignKey(EbProject)
    deleted_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.IntegerField()
    minus_per_hour = models.IntegerField()
    plus_per_hour = models.IntegerField()
    hourly_pay = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eb_projectmember'


class EbProjectmemberStages(models.Model):
    projectmember = models.ForeignKey(EbProjectmember)
    projectstage = models.ForeignKey('EbProjectstage')

    class Meta:
        managed = False
        db_table = 'eb_projectmember_stages'
        unique_together = (('projectmember', 'projectstage'),)


class EbProjectrequest(models.Model):
    year = models.CharField(max_length=4)
    month = models.CharField(max_length=2)
    request_no = models.CharField(unique=True, max_length=7)
    amount = models.IntegerField()
    project = models.ForeignKey(EbProject)
    created_date = models.DateTimeField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    client_order = models.ForeignKey(EbClientorder, blank=True, null=True)
    created_user = models.ForeignKey(User, related_name='projectrequest_createdusers', blank=True, null=True)
    request_name = models.CharField(max_length=50, blank=True, null=True)
    updated_user = models.ForeignKey(User, related_name='projectrequest_updatedusers', blank=True, null=True)
    filename = models.CharField(max_length=255, blank=True, null=True)
    expenses_amount = models.IntegerField()
    tax_amount = models.IntegerField()
    turnover_amount = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'eb_projectrequest'
        unique_together = (('project', 'client_order', 'year', 'month'),)


class EbProjectrequestdetail(models.Model):
    member_type = models.IntegerField()
    cost = models.IntegerField()
    no = models.IntegerField()
    hourly_pay = models.IntegerField()
    basic_price = models.IntegerField()
    min_hours = models.DecimalField(max_digits=5, decimal_places=2)
    max_hours = models.DecimalField(max_digits=5, decimal_places=2)
    total_hours = models.DecimalField(max_digits=5, decimal_places=2)
    extra_hours = models.DecimalField(max_digits=5, decimal_places=2)
    rate = models.DecimalField(max_digits=3, decimal_places=2)
    plus_per_hour = models.IntegerField()
    minus_per_hour = models.IntegerField()
    total_price = models.IntegerField()
    expenses_price = models.IntegerField()
    comment = models.CharField(max_length=50, blank=True, null=True)
    member_section = models.ForeignKey('EbSection')
    project_member = models.ForeignKey(EbProjectmember)
    project_request = models.ForeignKey(EbProjectrequest)
    salesperson = models.ForeignKey('EbSalesperson', blank=True, null=True)
    subcontractor = models.ForeignKey('EbSubcontractor', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eb_projectrequestdetail'
        unique_together = (('project_request', 'no'),)


class EbProjectrequestheading(models.Model):
    is_lump = models.IntegerField()
    lump_amount = models.BigIntegerField(blank=True, null=True)
    lump_comment = models.CharField(max_length=200, blank=True, null=True)
    is_hourly_pay = models.IntegerField()
    client_post_code = models.CharField(max_length=8, blank=True, null=True)
    client_address = models.CharField(max_length=200, blank=True, null=True)
    client_tel = models.CharField(max_length=15, blank=True, null=True)
    client_name = models.CharField(max_length=30, blank=True, null=True)
    tax_rate = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    decimal_type = models.CharField(max_length=1, blank=True, null=True)
    work_period_start = models.DateField(blank=True, null=True)
    work_period_end = models.DateField(blank=True, null=True)
    remit_date = models.DateField(blank=True, null=True)
    publish_date = models.DateField(blank=True, null=True)
    company_post_code = models.CharField(max_length=8, blank=True, null=True)
    company_address = models.CharField(max_length=200, blank=True, null=True)
    company_name = models.CharField(max_length=30, blank=True, null=True)
    company_tel = models.CharField(max_length=15, blank=True, null=True)
    company_master = models.CharField(max_length=30, blank=True, null=True)
    bank_name = models.CharField(max_length=20, blank=True, null=True)
    branch_no = models.CharField(max_length=3, blank=True, null=True)
    branch_name = models.CharField(max_length=20, blank=True, null=True)
    account_type = models.CharField(max_length=1, blank=True, null=True)
    account_number = models.CharField(max_length=7, blank=True, null=True)
    account_holder = models.CharField(max_length=20, blank=True, null=True)
    bank = models.ForeignKey(EbBankinfo, blank=True, null=True)
    client = models.ForeignKey(EbClient, blank=True, null=True)
    project_request = models.OneToOneField(EbProjectrequest)

    class Meta:
        managed = False
        db_table = 'eb_projectrequestheading'


class EbProjectskill(models.Model):
    period = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    project = models.ForeignKey(EbProject)
    skill = models.ForeignKey('EbSkill')
    deleted_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'eb_projectskill'


class EbProjectstage(models.Model):
    name = models.CharField(unique=True, max_length=15)
    deleted_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'eb_projectstage'


class EbSalesoffreason(models.Model):
    name = models.CharField(max_length=50)
    is_deleted = models.IntegerField()
    deleted_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eb_salesoffreason'


class EbSalesperson(models.Model):
    employee_id = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    first_name_ja = models.CharField(max_length=30, blank=True, null=True)
    last_name_ja = models.CharField(max_length=30, blank=True, null=True)
    first_name_en = models.CharField(max_length=30, blank=True, null=True)
    last_name_en = models.CharField(max_length=30, blank=True, null=True)
    sex = models.CharField(max_length=1, blank=True, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    graduate_date = models.DateField(blank=True, null=True)
    join_date = models.DateField(blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    private_email = models.CharField(max_length=254, blank=True, null=True)
    post_code = models.CharField(max_length=7, blank=True, null=True)
    address1 = models.CharField(max_length=200, blank=True, null=True)
    address2 = models.CharField(max_length=200, blank=True, null=True)
    nearest_station = models.CharField(max_length=15, blank=True, null=True)
    years_in_japan = models.IntegerField(blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
    is_married = models.CharField(max_length=1, blank=True, null=True)
    japanese_description = models.TextField(blank=True, null=True)
    certificate = models.TextField(blank=True, null=True)
    skill_description = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    member_type = models.IntegerField(choices=constants.CHOICE_SALESPERSON_TYPE)
    company = models.ForeignKey(EbCompany, blank=True, null=True)
    section = models.ForeignKey('EbSection', blank=True, null=True)
    user = models.OneToOneField(User, blank=True, null=True)
    is_retired = models.BooleanField()
    deleted_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField()
    coordinate_update_date = models.DateTimeField(blank=True, null=True)
    lat = models.CharField(max_length=25, blank=True, null=True)
    lng = models.CharField(max_length=25, blank=True, null=True)
    is_notify = models.BooleanField()
    notify_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eb_salesperson'
        ordering = ['first_name', 'last_name']
        verbose_name = verbose_name_plural = u"営業員"

    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)


class EbSection(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200, blank=True, null=True)
    company = models.ForeignKey(EbCompany)
    is_on_sales = models.IntegerField()
    deleted_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'eb_section'
        ordering = ['name']
        verbose_name = verbose_name_plural = u"部署"

    def __unicode__(self):
        return self.name


class EbSkill(models.Model):
    name = models.CharField(unique=True, max_length=30)
    deleted_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'eb_skill'


class EbSubcontractor(models.Model):
    name = models.CharField(unique=True, max_length=30)
    japanese_spell = models.CharField(max_length=30, blank=True, null=True)
    found_date = models.DateField(blank=True, null=True)
    capital = models.BigIntegerField(blank=True, null=True)
    post_code = models.CharField(max_length=7, blank=True, null=True)
    address1 = models.CharField(max_length=200, blank=True, null=True)
    address2 = models.CharField(max_length=200, blank=True, null=True)
    tel = models.CharField(max_length=15, blank=True, null=True)
    fax = models.CharField(max_length=15, blank=True, null=True)
    president = models.CharField(max_length=30, blank=True, null=True)
    employee_count = models.IntegerField(blank=True, null=True)
    sale_amount = models.BigIntegerField(blank=True, null=True)
    payment_day = models.CharField(max_length=2, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    payment_month = models.CharField(max_length=1, blank=True, null=True)
    deleted_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'eb_subcontractor'


class EbSubcontractororder(models.Model):
    order_no = models.CharField(unique=True, max_length=14)
    year = models.CharField(max_length=4)
    month = models.CharField(max_length=2)
    created_date = models.DateTimeField()
    updated_date = models.DateTimeField()
    is_deleted = models.IntegerField()
    deleted_date = models.DateTimeField(blank=True, null=True)
    subcontractor = models.ForeignKey(EbSubcontractor)
    created_user = models.ForeignKey(User, related_name='subcontractororder_createdusers', blank=True, null=True)
    updated_user = models.ForeignKey(User, related_name='subcontractororder_updatedusers', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eb_subcontractororder'
        unique_together = (('subcontractor', 'year', 'month'),)
