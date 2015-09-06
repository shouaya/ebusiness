# coding: UTF-8
"""
Created on 2015/08/21

@author: Yang Wanjun
"""
import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Company, Section, Member, Salesperson, Project, Client, ClientMember, \
    ProjectStatus, ProjectMember, Skill, ProjectSkill, ProjectActivity


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


class MemberNameListFilter(TextInputListFilter):
    title = u"名前"
    parameter_name = "name"

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(name__contains=self.value())


class ProjectNameListFilter(TextInputListFilter):

    title = u"案件名称"
    parameter_name = "name"

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(name__contains=self.value())


class CompanyAdmin(admin.ModelAdmin):

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
    list_display = ['employee_id', 'name', 'section', 'salesperson']
    list_display_links = ['name']
    list_filter = [MemberNameListFilter, 'section', 'salesperson']
    search_fields = ['name']

    def get_form(self, request, obj=None, **kwargs):
        form = super(MemberAdmin, self).get_form(request, obj, **kwargs)
        company = Company.objects.all()[0]
        if company:
            form.base_fields['company'].initial = company
        return form


class SalespersonAdmin(admin.ModelAdmin):

    form = forms.SalespersonForm
    list_display = ['employee_id', 'name', 'section']
    list_display_links = ['name']
    search_fields = ['name']
    list_filter = ['section']

    def get_form(self, request, obj=None, **kwargs):
        form = super(SalespersonAdmin, self).get_form(request, obj, **kwargs)
        company = Company.objects.all()[0]
        if company:
            form.base_fields['company'].initial = company
        return form


class ProjectSkillInline(admin.TabularInline):
    model = ProjectSkill
    extra = 1


class ProjectMemberInline(admin.TabularInline):
    model = ProjectMember
    extra = 1


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['project_id', 'name', 'start_date', 'end_date', 'status', 'salesperson']
    list_display_links = ['name']
    list_filter = [ProjectNameListFilter, 'status', 'salesperson']
    search_fields = ['name']
    inlines = (ProjectSkillInline, ProjectMemberInline)


class ClientAdmin(admin.ModelAdmin):

    def has_delete_permission(self, request, obj=None):
        # 削除禁止
        return False


class ClientMemberAdmin(admin.ModelAdmin):

    list_display = ['name', 'email', 'client']


class ProjectMemberAdmin(admin.ModelAdmin):

    form = forms.ProjectMemberAdminForm
    search_fields = ['project__name']

    list_display = ['project', 'display_project_client', 'member', 'start_date', 'end_date', 'status']
    list_filter = ['project__client', 'status']

    def display_project_client(self, obj):
        return obj.project.client.name

    display_project_client.short_description = u"関連会社"
    display_project_client.admin_order_field = 'project__client'

    def get_form(self, request, obj=None, **kwargs):
        form = super(ProjectMemberAdmin, self).get_form(request, obj, **kwargs)
        project_id = request.GET.get('project_id', None)
        if project_id:
            form.base_fields['project'].initial = Project.objects.get(project_id=project_id)
        employee_id = request.GET.get('employee_id', None)
        if employee_id:
            form.base_fields['member'].initial = Member.objects.get(employee_id=employee_id)
        return form


class ProjectActivityAdmin(admin.ModelAdmin):

    list_display = ['project', 'name', 'address', 'created_date']

    filter_horizontal = ['members', 'salesperson']


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
admin.site.register(ProjectStatus)
admin.site.register(ProjectMember, ProjectMemberAdmin)
admin.site.register(ProjectActivity, ProjectActivityAdmin)

admin.site.site_header = u'管理サイト'
admin.site.site_title = u'管理サイト'