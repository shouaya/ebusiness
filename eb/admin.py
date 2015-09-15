# coding: UTF-8
"""
Created on 2015/08/21

@author: Yang Wanjun
"""
import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Company, Section, Member, Salesperson, Project, Client, ClientMember, \
    ProjectMember, Skill, ProjectSkill, ProjectActivity, Subcontractor, PositionShip


class TextInputListFilter(admin.ListFilter):
    title = None
    parameter_name = None
    template = "admin_name_filter.html"

    def __init__(self, request, params, model, model_admin):
        super(TextInputListFilter, self).__init__(request, params, model, model_admin)

        if self.parameter_name in params:
            value = params.pop(self.parameter_name)
            self.used_parameters[self.parameter_name] = value

    def value(self):
        return self.used_parameters.get(self.parameter_name, None)

    def has_output(self):
        return True

    def expected_parameters(self):
        return [self.parameter_name]

    def choices(self, cl):
        all_choice = {
            'selected': self.value() is None,
            'query_string': cl.get_query_string({}, [self.parameter_name]),
            'display': _('All'),
        }
        return ({
            'get_query': cl.params,
            'current_value': self.value(),
            'all_choice': all_choice,
            'parameter_name': self.parameter_name
        }, )


class ProjectNameListFilter(TextInputListFilter):

    title = u"案件名称"
    parameter_name = "name"

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(name__contains=self.value())


class ProjectSkillInline(admin.TabularInline):
    model = ProjectSkill
    extra = 1


class ProjectMemberInline(admin.TabularInline):
    model = ProjectMember
    extra = 1


def get_full_name(obj):
    return "%s %s" % (obj.first_name, obj.last_name)
get_full_name.short_description = u"名前"
get_full_name.admin_order_field = "first_name"


class CompanyAdmin(admin.ModelAdmin):

    form = forms.CompanyForm

    class Media:
        js = ('http://ajaxzip3.googlecode.com/svn/trunk/ajaxzip3/ajaxzip3.js',)

    def has_delete_permission(self, request, obj=None):
        # 削除禁止
        return False

    def has_add_permission(self, request):
        if Company.objects.all().count() > 0:
            # データが存在する場合、追加を禁止
            return False
        else:
            return True


class SectionAdmin(admin.ModelAdmin):

    form = forms.SectionForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(SectionAdmin, self).get_form(request, obj, **kwargs)
        company = Company.objects.all()[0]
        if company:
            form.base_fields['company'].initial = company
        return form


class MemberAdmin(admin.ModelAdmin):

    form = forms.MemberForm
    list_display = ['employee_id', get_full_name, 'section', 'subcontractor', 'salesperson', 'user']
    list_display_links = [get_full_name]
    list_filter = ['member_type', 'section', 'subcontractor', 'salesperson']
    search_fields = ['first_name', 'last_name']

    class Media:
        js = ('http://ajaxzip3.googlecode.com/svn/trunk/ajaxzip3/ajaxzip3.js',)


class SalespersonAdmin(admin.ModelAdmin):

    form = forms.SalespersonForm
    list_display = ['employee_id', get_full_name, 'section', 'user']
    list_display_links = [get_full_name]
    search_fields = ['first_name', 'last_name']
    list_filter = ['section']

    def get_form(self, request, obj=None, **kwargs):
        form = super(SalespersonAdmin, self).get_form(request, obj, **kwargs)
        company = Company.objects.all()[0]
        if company:
            form.base_fields['company'].initial = company
        return form


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date', 'status', 'salesperson']
    list_display_links = ['name']
    list_filter = [ProjectNameListFilter, 'status', 'salesperson']
    search_fields = ['name']
    inlines = (ProjectSkillInline, ProjectMemberInline)


class ClientAdmin(admin.ModelAdmin):

    form = forms.ClientForm

    class Media:
        js = ('http://ajaxzip3.googlecode.com/svn/trunk/ajaxzip3/ajaxzip3.js',)

    def has_delete_permission(self, request, obj=None):
        # 削除禁止
        return False


class ClientMemberAdmin(admin.ModelAdmin):

    list_display = ['name', 'email', 'client']


class ProjectMemberAdmin(admin.ModelAdmin):

    form = forms.ProjectMemberAdminForm
    search_fields = ['project__name', 'member__first_name', 'member__last_name']

    list_display = ['project', 'display_project_client', 'member', 'start_date', 'end_date', 'status']
    list_display_links = ['member']
    list_filter = ['project__client', 'status']

    def display_project_client(self, obj):
        return obj.project.client.name

    display_project_client.short_description = u"関連会社"
    display_project_client.admin_order_field = 'project__client'

    def get_form(self, request, obj=None, **kwargs):
        form = super(ProjectMemberAdmin, self).get_form(request, obj, **kwargs)
        project_id = request.GET.get('project_id', None)
        if project_id:
            project = Project.objects.get(pk=project_id)
            form.base_fields['project'].initial = project
            form.base_fields['start_date'].initial = project.start_date
            form.base_fields['end_date'].initial = project.end_date
        employee_id = request.GET.get('employee_id', None)
        if employee_id:
            form.base_fields['member'].initial = Member.objects.get(employee_id=employee_id)
        return form


class ProjectActivityAdmin(admin.ModelAdmin):

    list_display = ['project', 'name', 'open_date', 'address', 'get_client_members', 'get_salesperson']
    list_display_links = ['name']
    list_filter = ['project']

    filter_horizontal = ['client_members', 'salesperson', 'members']

    def get_form(self, request, obj=None, **kwargs):
        form = super(ProjectActivityAdmin, self).get_form(request, obj, **kwargs)
        project_id = request.GET.get('project_id', None)
        if project_id:
            project = Project.objects.get(pk=project_id)
            form.base_fields['project'].initial = project
        return form

    def get_client_members(self, obj):
        client_members = obj.client_members.all()
        names = []
        for client_member in client_members:
            names.append(client_member.name)
        return ", ".join(names)

    def get_salesperson(self, obj):
        salesperson_list = obj.salesperson.all()
        names = []
        for salesperson in salesperson_list:
            names.append(u"%s %s" % (salesperson.first_name, salesperson.last_name))
        return ", ".join(names)

    get_client_members.short_description = u"参加しているお客様"
    get_salesperson.short_description = u"参加している営業員"


# Register your models here.
admin.site.register(Company, CompanyAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Salesperson, SalespersonAdmin)
admin.site.register(Skill)
admin.site.register(ProjectSkill)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(ClientMember, ClientMemberAdmin)
admin.site.register(ProjectMember, ProjectMemberAdmin)
admin.site.register(ProjectActivity, ProjectActivityAdmin)
admin.site.register(Subcontractor)
admin.site.register(PositionShip)

admin.site.site_header = u'社員営業状況管理システム'
admin.site.site_title = u'管理サイト'