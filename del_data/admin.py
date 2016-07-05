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


class DelDataAdminSite(admin.AdminSite):
    site_header = "削除したデータ（データ復元できます）"
    site_title = "管理サイト"


del_data_admin_site = DelDataAdminSite(name='del_data_admin')
del_data_admin_site.register(models.EbBankinfo, BankInfoAdmin)
del_data_admin_site.register(models.EbBpmemberorderinfo, BpMemberOrderInfoAdmin)
del_data_admin_site.register(models.EbClient, ClientAdmin)
del_data_admin_site.register(models.EbClientmember, ClientMemberAdmin)
del_data_admin_site.register(models.EbClientorder, ClientOrderAdmin)
del_data_admin_site.register(models.EbDegree, DegreeAdmin)
del_data_admin_site.register(models.EbExpensescategory, ExpensesCategoryAdmin)
del_data_admin_site.register(models.EbHistoryproject, HistoryProjectAdmin)
del_data_admin_site.register(models.EbMember, MemberAdmin)
del_data_admin_site.register(models.EbMemberattendance, MemberAttendanceAdmin)
del_data_admin_site.register(models.EbMemberexpenses, MemberExpensesAdmin)
del_data_admin_site.register(models.EbPositionship, PositionShipAdmin)
del_data_admin_site.register(models.EbOs, OsAdmin)
del_data_admin_site.register(models.EbProject, ProjectAdmin)
del_data_admin_site.register(models.EbProjectactivity, ProjectActivityAdmin)
del_data_admin_site.register(models.EbProjectmember, ProjectMemberAdmin)
del_data_admin_site.register(models.EbProjectskill, ProjectSkillAdmin)
del_data_admin_site.register(models.EbProjectstage, ProjectStageAdmin)
del_data_admin_site.register(models.EbSalesoffreason, SalesOffReasonAdmin)
del_data_admin_site.register(models.EbSalesperson, SalespersonAdmin)
del_data_admin_site.register(models.EbSection, SectionAdmin)
del_data_admin_site.register(models.EbSkill, SkillAdmin)
del_data_admin_site.register(models.EbSubcontractor, SubcontractorAdmin)
del_data_admin_site.register(models.EbSubcontractororder, SubcontractorOrderAdmin)
