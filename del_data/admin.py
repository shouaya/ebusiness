# coding: UTF-8

from django.contrib import admin
from . import models
# Register your models here.


def get_full_name(obj):
    return "%s %s" % (obj.first_name, obj.last_name)
get_full_name.short_description = u"名前"
get_full_name.admin_order_field = "first_name"


def is_user_created(obj):
    return obj.user is not None
is_user_created.short_description = u"ユーザ作成"
is_user_created.admin_order_field = "user"
is_user_created.boolean = True


class BaseAdmin(admin.ModelAdmin):

    actions = ['active_objects']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(BaseAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def active_objects(self, request, queryset):
        cnt = 0
        for obj in queryset:
            if obj.is_deleted:
                obj.is_deleted = False
                obj.deleted_date = None
                obj.save()
                cnt += 1
        self.message_user(request,  str(cnt) + u"件選択された対象が復活しました。")
    active_objects.short_description = u"選択されたレコードを復活する。"


class BankInfoAdmin(BaseAdmin):
    list_display = ['bank_name', 'branch_name', 'deleted_date']


class BpMemberOrderInfoAdmin(BaseAdmin):
    list_display = ['member', 'year', 'month', 'deleted_date']


class ClientAdmin(BaseAdmin):
    list_display = ['name', 'president', 'salesperson', 'deleted_date']


class ClientMemberAdmin(BaseAdmin):
    list_display = ['name', 'client', 'email', 'deleted_date']


class ClientOrderAdmin(BaseAdmin):
    list_display = ['name', 'order_no', 'start_date', 'end_date', 'deleted_date']


class DegreeAdmin(BaseAdmin):
    list_display = ['member', 'description', 'deleted_date']


class ExpensesCategoryAdmin(BaseAdmin):
    list_display = ['name', 'deleted_date']


class HistoryProjectAdmin(BaseAdmin):
    list_display = ['member', 'name', 'start_date', 'end_date', 'deleted_date']


class MemberAdmin(BaseAdmin):
    list_display = ['employee_id', get_full_name, 'section', 'subcontractor', 'salesperson',
                    is_user_created, 'is_retired', 'deleted_date']


class MemberAttendanceAdmin(BaseAdmin):
    list_display = ['project_member', 'year', 'month', 'total_hours', 'deleted_date']


class MemberExpensesAdmin(BaseAdmin):
    list_display = ['project_member', 'year', 'month', 'category', 'price', 'deleted_date']


class OsAdmin(BaseAdmin):
    list_display = ['name', 'deleted_date']


class PositionShipAdmin(BaseAdmin):
    list_display = ['member', 'position', 'section', 'deleted_date']


class ProjectAdmin(BaseAdmin):
    list_display = ['name', 'start_date', 'end_date', 'salesperson', 'deleted_date']


class ProjectActivityAdmin(BaseAdmin):
    list_display = ['project', 'name', 'open_date', 'address', 'deleted_date']


class ProjectMemberAdmin(BaseAdmin):
    list_display = ['project', 'member', 'start_date', 'end_date', 'deleted_date']


class ProjectSkillAdmin(BaseAdmin):
    list_display = ['project', 'skill', 'period', 'deleted_date']


class ProjectStageAdmin(BaseAdmin):
    list_display = ['name', 'deleted_date']


class SalesOffReasonAdmin(BaseAdmin):
    list_display = ['name', 'deleted_date']


class SalespersonAdmin(BaseAdmin):
    list_display = ['employee_id', get_full_name, 'email', 'section', 'member_type',
                    is_user_created, 'is_retired', 'deleted_date']


class SectionAdmin(BaseAdmin):
    list_display = ['name', 'is_on_sales', 'deleted_date']


class SkillAdmin(BaseAdmin):
    list_display = ['name', 'deleted_date']


class SubcontractorAdmin(BaseAdmin):
    list_display = ['name', 'deleted_date']


class SubcontractorOrderAdmin(BaseAdmin):
    list_display = ['subcontractor', 'order_no', 'year', 'month', 'deleted_date']


if models.EbBankinfo.objects.all().count() > 0:
    admin.site.register(models.EbBankinfo, BankInfoAdmin)
if models.EbBpmemberorderinfo.objects.all().count() > 0:
    admin.site.register(models.EbBpmemberorderinfo, BpMemberOrderInfoAdmin)
if models.EbClient.objects.all().count() > 0:
    admin.site.register(models.EbClient, ClientAdmin)
if models.EbClientmember.objects.all().count() > 0:
    admin.site.register(models.EbClientmember, ClientMemberAdmin)
if models.EbClientorder.objects.all().count() > 0:
    admin.site.register(models.EbClientorder, ClientOrderAdmin)
if models.EbDegree.objects.all().count() > 0:
    admin.site.register(models.EbDegree, DegreeAdmin)
if models.EbExpensescategory.objects.all().count() > 0:
    admin.site.register(models.EbExpensescategory, ExpensesCategoryAdmin)
if models.EbHistoryproject.objects.all().count() > 0:
    admin.site.register(models.EbHistoryproject, HistoryProjectAdmin)
if models.EbMember.objects.all().count() > 0:
    admin.site.register(models.EbMember, MemberAdmin)
if models.EbMemberattendance.objects.all().count() > 0:
    admin.site.register(models.EbMemberattendance, MemberAttendanceAdmin)
if models.EbMemberexpenses.objects.all().count() > 0:
    admin.site.register(models.EbMemberexpenses, MemberExpensesAdmin)
if models.EbPositionship.objects.all().count() > 0:
    admin.site.register(models.EbPositionship, PositionShipAdmin)
if models.EbOs.objects.all().count() > 0:
    admin.site.register(models.EbOs, OsAdmin)
if models.EbProject.objects.all().count() > 0:
    admin.site.register(models.EbProject, ProjectAdmin)
if models.EbProjectactivity.objects.all().count() > 0:
    admin.site.register(models.EbProjectactivity, ProjectActivityAdmin)
if models.EbProjectmember.objects.all().count() > 0:
    admin.site.register(models.EbProjectmember, ProjectMemberAdmin)
if models.EbProjectskill.objects.all().count() > 0:
    admin.site.register(models.EbProjectskill, ProjectSkillAdmin)
if models.EbProjectstage.objects.all().count() > 0:
    admin.site.register(models.EbProjectstage, ProjectStageAdmin)
if models.EbSalesoffreason.objects.all().count() > 0:
    admin.site.register(models.EbSalesoffreason, SalesOffReasonAdmin)
if models.EbSalesperson.objects.all().count() > 0:
    admin.site.register(models.EbSalesperson, SalespersonAdmin)
if models.EbSection.objects.all().count() > 0:
    admin.site.register(models.EbSection, SectionAdmin)
if models.EbSkill.objects.all().count() > 0:
    admin.site.register(models.EbSkill, SkillAdmin)
if models.EbSubcontractor.objects.all().count() > 0:
    admin.site.register(models.EbSubcontractor, SubcontractorAdmin)
if models.EbSubcontractororder.objects.all().count() > 0:
    admin.site.register(models.EbSubcontractororder, SubcontractorOrderAdmin)
