# coding: UTF-8
from django.contrib import admin

# Register your models here.
from . import models, forms


class BaseEboaAdmin(admin.ModelAdmin):

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


class EbAttendanceAdmin(BaseEboaAdmin):
    form = forms.EbAttendanceForm
    list_display = ['id', 'applicant_name', 'period', 'totalday', 'nightcount', 'transit', 'transit_interval']

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
eboa_admin_site.register(models.SysOrg, SysOrgAdmin)
eboa_admin_site.register(models.SysUser, SysUserAdmin)
