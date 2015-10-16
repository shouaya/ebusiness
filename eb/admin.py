# coding: UTF-8
"""
Created on 2015/08/21

@author: Yang Wanjun
"""
import datetime

from django.contrib import admin
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

import forms
from .models import Company, Section, Member, Salesperson, Project, Client, ClientMember, \
    ProjectMember, Skill, ProjectSkill, ProjectActivity, Subcontractor, PositionShip,\
    ProjectStage, OS, HistoryProject, MemberAttendance, create_group_salesperson
from utils import common


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


class NoUserFilter(admin.SimpleListFilter):
    title = u"ユーザ"
    parameter_name = 'user__isnull'

    def lookups(self, request, model_admin):
        return (
            ('False', u"ユーザあり"),
            ('True', u"ユーザなし")
        )

    def queryset(self, request, queryset):
        if self.value() == 'True':
            return queryset.filter(user__isnull=True)
        if self.value() == 'False':
            return queryset.filter(user__isnull=False)


class ProjectSkillInline(admin.TabularInline):
    model = ProjectSkill
    extra = 1


class ProjectMemberInline(admin.TabularInline):
    model = ProjectMember
    extra = 1


class MemberAttendanceInline(admin.TabularInline):
    form = forms.MemberAttendanceForm
    model = MemberAttendance
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
    list_filter = ['member_type', 'section', 'subcontractor', 'salesperson', NoUserFilter]
    search_fields = ['first_name', 'last_name']
    fieldsets = (
        (None, {'fields': ('employee_id',
                           ('first_name', 'last_name'),
                           ('first_name_en', 'last_name_en'),
                           ('first_name_ja', 'last_name_ja'),
                           'birthday')}),
        (u'詳細情報',
         {'classes': ('collapse',),
          'fields': (('sex', 'is_married'),
                     'post_code',
                     ('address1', 'address2'),
                     'country', 'graduate_date', 'phone', 'japanese_description', 'certificate', 'comment')}),
        (u"勤務情報", {'fields': ('member_type', 'email', 'section', 'company', 'subcontractor', 'salesperson')})
    )

    class Media:
        js = ('http://ajaxzip3.googlecode.com/svn/trunk/ajaxzip3/ajaxzip3.js',)

    def get_queryset(self, request):
        query_set = admin.ModelAdmin.get_queryset(self, request)
        if request.user.is_superuser:
            return query_set
        else:
            return query_set.filter(salesperson=request.user.salesperson)


class SalespersonAdmin(admin.ModelAdmin):

    form = forms.SalespersonForm
    list_display = ['employee_id', get_full_name, 'section', 'is_user_created']
    list_display_links = [get_full_name]
    search_fields = ['first_name', 'last_name']
    list_filter = ['section', NoUserFilter]
    fieldsets = (
        (None, {'fields': ('employee_id',
                           ('first_name', 'last_name'),
                           ('first_name_en', 'last_name_en'),
                           ('first_name_ja', 'last_name_ja'),
                           'birthday')}),
        (u'詳細情報',
         {'classes': ('collapse',),
          'fields': (('sex', 'is_married'),
                     'post_code',
                     ('address1', 'address2'),
                     'country', 'graduate_date', 'phone', 'japanese_description', 'certificate', 'comment')}),
        (u"勤務情報", {'fields': ('member_type', 'email', 'section', 'company')})
    )
    actions = ['create_users']

    class Media:
        js = ('http://ajaxzip3.googlecode.com/svn/trunk/ajaxzip3/ajaxzip3.js',)

    def get_form(self, request, obj=None, **kwargs):
        form = super(SalespersonAdmin, self).get_form(request, obj, **kwargs)
        company = Company.objects.all()[0]
        if company:
            form.base_fields['company'].initial = company
        return form

    def is_user_created(self, obj):
        return obj.user is not None

    def get_queryset(self, request):
        query_set = admin.ModelAdmin.get_queryset(self, request)
        salesperson = request.user.salesperson
        if request.user.is_superuser:
            return query_set
        elif salesperson.member_type == 0 and salesperson.section:
            # 営業部長の場合は該当部署のすべての営業員が変更できる。
            return query_set.filter(section=salesperson.section)
        else:
            return query_set.filter(pk=salesperson.pk)

    def create_users(self, request, queryset):
        if request.user.is_superuser:
            cnt = 0
            for member in queryset.filter(user__isnull=True):
                name = member.first_name_en.lower() + member.last_name_en.lower()
                pwd = common.get_default_password(member)
                user = User.objects.create_user(name, member.email, pwd)
                user.is_staff = True
                group = create_group_salesperson()
                user.groups.add(group)
                user.save()
                member.user = user
                member.save()
                cnt += 1
            if cnt:
                self.message_user(request, u"選択された営業員にユーザが作成されました。")
            else:
                self.message_user(request, u"すでに作成済みなので、再作成する必要がありません。", messages.WARNING)
        else:
            self.message_user(request, u"権限がありません！", messages.ERROR)

    is_user_created.short_description = u"ユーザ作成"
    is_user_created.admin_order_field = "user"
    is_user_created.boolean = True
    create_users.short_description = u"ユーザを作成する"


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date', 'status', 'salesperson']
    list_display_links = ['name']
    list_filter = [ProjectNameListFilter, 'status', 'salesperson']
    search_fields = ['name']
    inlines = (ProjectSkillInline, ProjectMemberInline)

    def get_form(self, request, obj=None, **kwargs):
        form = super(ProjectAdmin, self).get_form(request, obj, **kwargs)
        if obj and obj.client:
            form.base_fields['boss'].queryset = ClientMember.objects.filter(client=obj.client)
            form.base_fields['middleman'].queryset = ClientMember.objects.filter(client=obj.client)
        return form

    def get_queryset(self, request):
        query_set = admin.ModelAdmin.get_queryset(self, request)
        if request.user.is_superuser:
            return query_set
        else:
            return query_set.filter(salesperson=request.user.salesperson)


class ClientAdmin(admin.ModelAdmin):

    form = forms.ClientForm

    class Media:
        js = ('http://ajaxzip3.googlecode.com/svn/trunk/ajaxzip3/ajaxzip3.js',)


class ClientMemberAdmin(admin.ModelAdmin):

    list_display = ['name', 'email', 'client']
    search_fields = ['name']


class ProjectMemberAdmin(admin.ModelAdmin):

    form = forms.ProjectMemberForm
    search_fields = ['project__name', 'member__first_name', 'member__last_name']

    list_display = ['project', 'display_project_client', 'member', 'start_date', 'end_date', 'status']
    list_display_links = ['member']
    list_filter = ['status']
    inlines = (MemberAttendanceInline,)
    #
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


class MemberAttendanceAdmin(admin.ModelAdmin):
    forms = forms.MemberAttendanceForm
    list_display = ['project_member', 'year', 'month', 'total_hours', 'extra_hours']


class ProjectActivityAdmin(admin.ModelAdmin):

    list_display = ['project', 'name', 'open_date', 'address', 'get_client_members', 'get_salesperson']
    list_display_links = ['name']

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


class HistoryProjectAdmin(admin.ModelAdmin):
    filter_horizontal = ['os', 'stages']


# Register your models here.
admin.site.register(Company, CompanyAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Salesperson, SalespersonAdmin)
admin.site.register(Skill)
# admin.site.register(ProjectSkill)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(ClientMember, ClientMemberAdmin)
admin.site.register(ProjectMember, ProjectMemberAdmin)
admin.site.register(MemberAttendance, MemberAttendanceAdmin)
admin.site.register(ProjectActivity, ProjectActivityAdmin)
admin.site.register(Subcontractor)
admin.site.register(PositionShip)
admin.site.register(ProjectStage)
admin.site.register(OS)
admin.site.register(HistoryProject, HistoryProjectAdmin)

admin.site.site_header = u'社員営業状況管理システム'
admin.site.site_title = u'管理サイト'