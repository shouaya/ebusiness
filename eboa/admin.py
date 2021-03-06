# coding: UTF-8
from django.contrib import admin

# Register your models here.
from . import models, forms


class BaseEboaAdmin(admin.ModelAdmin):

    class Media:
        js = ('/static/admin/js/jquery-2.1.4.min.js',
              '/static/admin/js/readonly.js',)

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        # obj.save(using=self.using)
        pass

    def get_actions(self, request):
        actions = super(BaseEboaAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        return list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
        ))


class EbAttendanceAdmin(BaseEboaAdmin):
    form = forms.EbAttendanceForm
    list_display = ['id', 'applicant_name', 'period', 'totalday', 'nightcount',
                    'totaltime', 'transit', 'transit_interval']

    def applicant_name(self, obj):
        return obj.applicant.fullname


class EbEmployeeAdmin(BaseEboaAdmin):
    form = forms.EbEmployeeForm
    list_display = ['id', 'code', 'name', 'address', 'get_sections_name']
    list_display_links = ['name']
    search_fields = ['id', 'code', 'name']

    def get_sections_name(self, obj):
        """所属を結合して表示する。

        :param obj:
        :return:
        """
        sys_user = obj.user
        if sys_user:
            orgs = [o.orgname for o in sys_user.sysorg_set.all()]
            return ",".join(orgs)
        else:
            return ""
    get_sections_name.short_description = u"所属"


class EbEmpContractAdmin(BaseEboaAdmin):
    list_display = ['id', 'code', 'codeid', 'employer_type', 'employment_date', 'employment_period_en']
    list_display_links = ['code']
    search_fields = ['code']


class EbHolidayAdmin(BaseEboaAdmin):
    list_display = ['id', 'holiday', 'memo', 'maker', 'maker_id']


class HolidaysApplicationAdmin(BaseEboaAdmin):
    list_display = ['id', 'employee_name', 'start_date', 'end_date', 'use_days']


class PaidHolidaysAdmin(BaseEboaAdmin):
    list_display = ['id', 'employee_name', 'years', 'days', 'used']
    search_fields = ['employee__userid', 'employee_name', 'year']


class SalaryidmstAdmin(BaseEboaAdmin):
    list_display = ['id', 'salaryid', 'employee_name', 'employeeid']
    list_display_links = ['employee_name']
    search_fields = ['employee_name', 'salaryid']


class SysOrgAdmin(BaseEboaAdmin):
    form = forms.SysOrgForm
    list_display = ['orgid', 'orgname', 'get_parent_org', 'isdelete']
    list_display_links = ['orgname']

    def get_parent_org(self, obj):
        if obj.orgsupid:
            super_org = models.SysOrg.objects.get(pk=obj.orgsupid)
            return super_org.orgname
        else:
            return None


class SysUserAdmin(BaseEboaAdmin):
    form = forms.SysUserForm
    list_display = ['userid', 'fullname']
    search_fields = ['userid', 'fullname']


class EboaAdminSite(admin.AdminSite):
    site_header = "EBOAデータ参照（データは変更できません）"
    site_title = "管理サイト"


eboa_admin_site = EboaAdminSite(name='eboa_admin')
eboa_admin_site.register(models.EbAttendance, EbAttendanceAdmin)
eboa_admin_site.register(models.EbEmployee, EbEmployeeAdmin)
eboa_admin_site.register(models.EbEmpContract, EbEmpContractAdmin)
eboa_admin_site.register(models.EbHoliday, EbHolidayAdmin)
eboa_admin_site.register(models.HolidaysApplication, HolidaysApplicationAdmin)
eboa_admin_site.register(models.PaidHolidays, PaidHolidaysAdmin)
eboa_admin_site.register(models.Salaryidmst, SalaryidmstAdmin)
eboa_admin_site.register(models.SysOrg, SysOrgAdmin)
eboa_admin_site.register(models.SysUser, SysUserAdmin)
