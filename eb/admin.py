# coding: UTF-8
"""
Created on 2015/08/21

@author: Yang Wanjun
"""
import os
import datetime

from django.http import HttpResponse
from django.contrib import admin
from django.contrib import messages
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.db.models import Max

import forms
from .models import Company, Section, Member, Salesperson, Project, Client, ClientMember, \
    ProjectMember, Skill, ProjectSkill, ProjectActivity, Subcontractor, PositionShip,\
    ProjectStage, OS, HistoryProject, MemberAttendance, Degree, ClientOrder, \
    create_group_salesperson, MemberExpenses, ExpensesCategory, BankInfo, History, ProjectRequest, Issue, \
    ProjectRequestHeading, ProjectRequestDetail, SalesOffReason, EmployeeExpenses
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


class ActionFlagFilter(admin.SimpleListFilter):
    title = u"操作種別 "
    parameter_name = "action_flag"

    def lookups(self, request, model_admin):
        return (
            ('1', u"追加"),
            ('2', u"修正"),
            ('3', u"削除"),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(action_flag=self.value())


class ProjectSkillInline(admin.TabularInline):
    model = ProjectSkill
    extra = 0


class ProjectMemberInline(admin.TabularInline):
    model = ProjectMember
    form = forms.ProjectMemberForm
    extra = 0

    def get_queryset(self, request):
        queryset = super(ProjectMemberInline, self).get_queryset(request)
        return queryset.filter(is_deleted=False, member__is_retired=False, member__is_deleted=False)


class EmployeeExpensesInline(admin.TabularInline):
    model = EmployeeExpenses
    extra = 0

    def get_queryset(self, request):
        queryset = super(EmployeeExpensesInline, self).get_queryset(request)
        return queryset.filter(is_deleted=False)


class MemberExpensesInline(admin.TabularInline):
    model = MemberExpenses
    extra = 0

    def get_queryset(self, request):
        queryset = super(MemberExpensesInline, self).get_queryset(request)
        return queryset.filter(is_deleted=False)


class MemberAttendanceInline(admin.TabularInline):
    form = forms.MemberAttendanceForm
    model = MemberAttendance
    extra = 0

    def get_queryset(self, request):
        queryset = super(MemberAttendanceInline, self).get_queryset(request)
        return queryset.filter(is_deleted=False)


class DegreeInline(admin.TabularInline):
    model = Degree
    extra = 0


def get_full_name(obj):
    return "%s %s" % (obj.first_name, obj.last_name)
get_full_name.short_description = u"名前"
get_full_name.admin_order_field = "first_name"


class BaseAdmin(admin.ModelAdmin):

    class Media:
        js = ('http://ajaxzip3.googlecode.com/svn/trunk/ajaxzip3/ajaxzip3.js',
              '/static/js/jquery-2.1.4.min.js',
              '/static/js/filterlist.js',
              '/static/js/select_filter.js',
              '/static/js/base.js')

    def response_change(self, request, obj):
        if request.GET.get('from') == "portal":
            return HttpResponse('''
               <script type="text/javascript">
                  window.close();
               </script>''')
        else:
            response = super(BaseAdmin, self).response_change(request, obj)
            return response

    def response_add(self, request, obj, post_url_continue=None):
        if request.GET.get('from') == "portal":
            return HttpResponse('''
               <script type="text/javascript">
                  window.close();
               </script>''')
        else:
            response = super(BaseAdmin, self).response_add(request, obj)
            return response


class AdminOnlyAdmin(BaseAdmin):

    def has_delete_permission(self, request, obj=None):
        if request.user.username == u"admin":
            return True
        else:
            return False

    def has_add_permission(self, request):
        if request.user.username == u"admin":
            return True
        else:
            return False

    def has_change_permission(self, request, obj=None):
        if request.user.username == u"admin":
            return True
        else:
            return False


class ReadonlyAdmin(admin.ModelAdmin):

    class Media:
        js = ('/static/js/jquery-2.1.4.min.js', '/static/js/readonly.js',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.username == u"admin":
            return True
        else:
            return False

    def get_readonly_fields(self, request, obj=None):
        return list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
        ))


class CompanyAdmin(BaseAdmin):

    form = forms.CompanyForm

    def has_delete_permission(self, request, obj=None):
        # 削除禁止
        return False

    def has_add_permission(self, request):
        if Company.objects.all().count() > 0:
            # データが存在する場合、追加を禁止
            return False
        else:
            return True


class BankInfoAdmin(BaseAdmin):

    list_display = ['bank_name', 'is_deleted']
    actions = ['delete_objects', 'active_objects']

    def get_form(self, request, obj=None, **kwargs):
        form = super(BankInfoAdmin, self).get_form(request, obj, **kwargs)
        company = Company.objects.all()[0]
        if company:
            form.base_fields['company'].initial = company
        return form

    def delete_objects(self, request, queryset):
        cnt = 0
        for obj in queryset:
            if not obj.is_deleted:
                obj.delete()
                cnt += 1
        self.message_user(request,  str(cnt) + u"件選択された対象が削除されました。")

    def active_objects(self, request, queryset):
        cnt = 0
        for obj in queryset:
            if obj.is_deleted:
                obj.is_deleted = False
                obj.save()
                cnt += 1
        self.message_user(request,  str(cnt) + u"件選択された対象が復活しました。")

    delete_objects.short_description = u"選択されたレコードを削除する。"
    active_objects.short_description = u"選択されたレコードを復活する。"


class SectionAdmin(BaseAdmin):

    form = forms.SectionForm
    list_display = ['name', 'is_on_sales', 'is_deleted']
    list_filter = ['is_on_sales', 'is_deleted']
    actions = ['delete_objects', 'active_objects']

    def get_form(self, request, obj=None, **kwargs):
        form = super(SectionAdmin, self).get_form(request, obj, **kwargs)
        company = Company.objects.all()[0]
        if company:
            form.base_fields['company'].initial = company
        return form

    def get_actions(self, request):
        actions = super(SectionAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def delete_objects(self, request, queryset):
        cnt = 0
        for obj in queryset:
            if not obj.is_deleted:
                obj.delete()
                cnt += 1
        self.message_user(request,  str(cnt) + u"件選択された対象が削除されました。")

    def active_objects(self, request, queryset):
        cnt = 0
        for obj in queryset:
            if obj.is_deleted:
                obj.is_deleted = False
                obj.save()
                cnt += 1
        self.message_user(request,  str(cnt) + u"件選択された対象が復活しました。")

    delete_objects.short_description = u"選択されたレコードを削除する。"
    active_objects.short_description = u"選択されたレコードを復活する。"


class SalesOffReasonAdmin(BaseAdmin):
    list_display = ['name', 'is_deleted']


class MemberAdmin(BaseAdmin):

    form = forms.MemberForm
    list_display = ['employee_id', get_full_name, 'section', 'subcontractor', 'salesperson',
                    'is_user_created', 'is_retired', 'is_deleted']
    list_display_links = [get_full_name]
    list_filter = ['member_type', 'section', 'salesperson', NoUserFilter,
                   'is_retired', 'is_deleted']
    search_fields = ['first_name', 'last_name']
    inlines = (DegreeInline, EmployeeExpensesInline)
    actions = ['create_users', 'delete_objects', 'active_objects', 'member_retire']
    fieldsets = (
        (None, {'fields': ('employee_id',
                           ('first_name', 'last_name'),
                           ('first_name_en', 'last_name_en'),
                           ('first_name_ja', 'last_name_ja'),
                           'birthday')}),
        (u'詳細情報',
         {'classes': ('collapse',),
          'fields': ('private_email',
                     ('sex', 'is_married', 'years_in_japan'),
                     'post_code',
                     ('address1', 'address2'), 'nearest_station',
                     'country', 'graduate_date', 'phone', 'japanese_description',
                     'certificate', 'skill_description', 'comment')}),
        (u"勤務情報", {'fields': ['member_type', 'join_date', 'email', 'is_notify', 'notify_type', 'section', 'company',
                              'subcontractor', 'is_on_sales', 'sales_off_reason', 'salesperson', 'is_retired']})
    )

    def get_actions(self, request):
        actions = super(MemberAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_form(self, request, obj=None, **kwargs):
        form = super(MemberAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['section'].queryset = Section.objects.public_filter(is_on_sales=True)
        return form

    def is_user_created(self, obj):
        return obj.user is not None
    is_user_created.short_description = u"ユーザ作成"
    is_user_created.admin_order_field = "user"
    is_user_created.boolean = True

    def change_view(self, request, object_id, form_url='', extra_context=None):
        member = Member.objects.get(pk=object_id)
        if member.member_type == 4:
            # 他社技術者
            if self.fieldsets[2][1]['fields'].count('cost') == 0:
                self.fieldsets[2][1]['fields'].insert(-2, 'cost')
            if self.fieldsets[2][1]['fields'].count('is_individual_pay') == 0:
                self.fieldsets[2][1]['fields'].insert(-3, 'is_individual_pay')
        else:
            try:
                self.fieldsets[2][1]['fields'].remove('cost')
                self.fieldsets[2][1]['fields'].remove('is_individual_pay')
            except ValueError:
                pass
        return super(MemberAdmin, self).change_view(request, object_id, form_url, extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        if self.fieldsets[2][1]['fields'].count('cost') == 0:
            self.fieldsets[2][1]['fields'].insert(-2, 'cost')
        if self.fieldsets[2][1]['fields'].count('is_individual_pay') == 0:
            self.fieldsets[2][1]['fields'].insert(-3, 'is_individual_pay')
        return super(MemberAdmin, self).add_view(request, form_url, extra_context)

    def delete_objects(self, request, queryset):
        cnt = 0
        for obj in queryset:
            if not obj.is_deleted:
                obj.delete()
                cnt += 1
        self.message_user(request,  str(cnt) + u"件選択された対象が削除されました。")

    def active_objects(self, request, queryset):
        cnt = 0
        for obj in queryset:
            if obj.is_deleted:
                obj.is_deleted = False
                obj.save()
                cnt += 1
        self.message_user(request,  str(cnt) + u"件選択された対象が復活しました。")

    def member_retire(self, request, queryset):
        cnt = queryset.update(is_retired=True)
        self.message_user(request,  str(cnt) + u"件選択されたメンバーが退職しました。")

    delete_objects.short_description = u"選択されたレコードを削除する。"
    active_objects.short_description = u"選択されたレコードを復活する。"
    member_retire.short_description = u"選択されたメンバーを退職する"

    def create_users(self, request, queryset):
        if request.user.is_superuser:
            cnt = 0
            for member in queryset.filter(user__isnull=True):
                if member.email:
                    name = member.email
                    pwd = common.get_default_password(member)
                    user = User.objects.create_user(name, member.email, pwd)
                    user.is_staff = False
                    user.first_name = member.first_name
                    user.last_name = member.last_name
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

    create_users.short_description = u"ユーザを作成する"


class SalespersonAdmin(BaseAdmin):

    form = forms.SalespersonForm
    list_display = ['employee_id', get_full_name, 'email', 'section', 'member_type',
                    'is_user_created', 'is_retired', 'is_deleted']
    list_display_links = [get_full_name]
    search_fields = ['first_name', 'last_name']
    list_filter = ['member_type', 'section', NoUserFilter, 'is_retired', 'is_deleted']
    fieldsets = (
        (None, {'fields': ('employee_id',
                           ('first_name', 'last_name'),
                           ('first_name_en', 'last_name_en'),
                           ('first_name_ja', 'last_name_ja'),
                           'birthday')}),
        (u'詳細情報',
         {'classes': ('collapse',),
          'fields': ('private_email',
                     ('sex', 'is_married'),
                     'post_code',
                     ('address1', 'address2'),
                     'country', 'graduate_date', 'phone', 'japanese_description', 'certificate', 'comment')}),
        (u"勤務情報", {'fields': ('member_type', 'email', 'is_notify', 'notify_type', 'section', 'company', 'is_retired')})
    )
    actions = ['create_users', 'delete_objects', 'active_objects']

    def get_actions(self, request):
        actions = super(SalespersonAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_form(self, request, obj=None, **kwargs):
        form = super(SalespersonAdmin, self).get_form(request, obj, **kwargs)
        company = Company.objects.all()[0]
        if company:
            form.base_fields['company'].initial = company
        return form

    def is_user_created(self, obj):
        return obj.user is not None

    def create_users(self, request, queryset):
        if request.user.is_superuser:
            cnt = 0
            for member in queryset.filter(user__isnull=True):
                if member.email:
                    name = member.email
                    pwd = common.get_default_password(member)
                    user = User.objects.create_user(name, member.email, pwd)
                    user.is_staff = True
                    group = create_group_salesperson()
                    user.groups.add(group)
                    user.first_name = member.first_name
                    user.last_name = member.last_name
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

    def delete_objects(self, request, queryset):
        cnt = 0
        for obj in queryset:
            if not obj.is_deleted:
                obj.delete()
                cnt += 1
        self.message_user(request,  str(cnt) + u"件選択された対象が削除されました。")

    def active_objects(self, request, queryset):
        cnt = 0
        for obj in queryset:
            if obj.is_deleted:
                obj.is_deleted = False
                obj.save()
                cnt += 1
        self.message_user(request,  str(cnt) + u"件選択された対象が復活しました。")

    delete_objects.short_description = u"選択されたレコードを削除する。"
    active_objects.short_description = u"選択されたレコードを復活する。"


class ProjectAdmin(BaseAdmin):
    form = forms.ProjectForm
    list_display = ['name', 'client', 'start_date', 'end_date', 'status', 'salesperson', 'is_deleted']
    list_display_links = ['name']
    list_filter = [ProjectNameListFilter, 'status', 'salesperson', 'is_deleted']
    search_fields = ['name', 'client__name']
    inlines = (ProjectSkillInline, ProjectMemberInline)
    actions = ['delete_objects', 'active_objects']

    def _create_formsets(self, request, obj, change):
        formsets, inline_instances = super(ProjectAdmin, self)._create_formsets(request, obj, change)
        for fm in formsets:
            if fm.model == ProjectMember:
                fm.form.base_fields['min_hours'].initial = obj.min_hours
                fm.form.base_fields['max_hours'].initial = obj.max_hours
        return formsets, inline_instances

    def get_actions(self, request):
        actions = super(ProjectAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_form(self, request, obj=None, **kwargs):
        form = super(ProjectAdmin, self).get_form(request, obj, **kwargs)
        if obj and obj.client:
            form.base_fields['boss'].queryset = ClientMember.objects.filter(client=obj.client)
            form.base_fields['middleman'].queryset = ClientMember.objects.filter(client=obj.client)
        return form

    def save_related(self, request, form, formsets, change):
        super(ProjectAdmin, self).save_related(request, form, formsets, change)
        # 保存時、配下のすべてのメンバーの営業員項目を案件の営業員に更新する。
        project = form.instance
        today = datetime.date.today()
        if project.salesperson:
            for pm in project.projectmember_set.filter(is_deleted=False, start_date__lte=today, end_date__gte=today):
                member = pm.member
                member.salesperson = project.salesperson
                member.save()
        # 保存時、案件の終了日を一番後ろの案件メンバーの終了日とする。
        max_end_date = project.projectmember_set.filter(is_deleted=False).aggregate(Max('end_date'))
        max_end_date = max_end_date.get('end_date__max')
        if max_end_date and (project.end_date is None or max_end_date > project.end_date):
            project.end_date = max_end_date
            project.save()

    def delete_objects(self, request, queryset):
        cnt = 0
        for obj in queryset:
            if not obj.is_deleted:
                obj.delete()
                cnt += 1
        self.message_user(request,  str(cnt) + u"件選択された対象が削除されました。")

    def active_objects(self, request, queryset):
        cnt = 0
        for obj in queryset:
            if obj.is_deleted:
                obj.is_deleted = False
                obj.save()
                cnt += 1
        self.message_user(request,  str(cnt) + u"件選択された対象が復活しました。")

    delete_objects.short_description = u"選択されたレコードを削除する。"
    active_objects.short_description = u"選択されたレコードを復活する。"


class ClientAdmin(BaseAdmin):

    form = forms.ClientForm

    list_display = ['name', 'is_request_uploaded', 'is_deleted']
    list_filter = ['is_deleted']
    actions = ['delete_objects', 'active_objects']

    def is_request_uploaded(self, obj):
        if obj.request_file and os.path.exists(obj.request_file.path):
            return True
        else:
            return False

    is_request_uploaded.short_description = u"請求書テンプレート"
    is_request_uploaded.boolean = True

    def get_actions(self, request):
        actions = super(ClientAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def delete_objects(self, request, queryset):
        cnt = 0
        for obj in queryset:
            if not obj.is_deleted:
                obj.delete()
                cnt += 1
        self.message_user(request,  str(cnt) + u"件選択された対象が削除されました。")

    def active_objects(self, request, queryset):
        cnt = 0
        for obj in queryset:
            if obj.is_deleted:
                obj.is_deleted = False
                obj.save()
                cnt += 1
        self.message_user(request,  str(cnt) + u"件選択された対象が復活しました。")

    delete_objects.short_description = u"選択されたレコードを削除する。"
    active_objects.short_description = u"選択されたレコードを復活する。"


class ClientOrderAdmin(BaseAdmin):
    list_display = ['name', 'start_date', 'end_date', 'is_deleted']
    list_filter = ['is_deleted']
    filter_horizontal = ['projects']
    search_fields = ['name']
    actions = ['delete_objects', 'active_objects']

    def get_actions(self, request):
        actions = super(ClientOrderAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_form(self, request, obj=None, **kwargs):
        form = super(ClientOrderAdmin, self).get_form(request, obj, **kwargs)
        project_id = request.GET.get('project_id', None)
        ym = request.GET.get("ym", None)
        banks = BankInfo.objects.public_all()
        if project_id:
            project = Project.objects.public_filter(pk=project_id)
            form.base_fields['projects'].initial = project
            form.base_fields['name'].initial = project[0].name if project.count() > 0 else ""
        if ym:
            first_day = common.get_first_day_from_ym(ym)
            form.base_fields['start_date'].initial = first_day
            form.base_fields['end_date'].initial = common.get_last_day_by_month(first_day)
        if banks.count() > 0:
            form.base_fields['bank_info'].initial = banks[0]
        return form

    def delete_objects(self, request, queryset):
        cnt = 0
        for obj in queryset:
            if not obj.is_deleted:
                obj.delete()
                cnt += 1
        self.message_user(request,  str(cnt) + u"件選択された対象が削除されました。")

    def active_objects(self, request, queryset):
        cnt = 0
        for obj in queryset:
            if obj.is_deleted:
                obj.is_deleted = False
                obj.save()
                cnt += 1
        self.message_user(request,  str(cnt) + u"件選択された対象が復活しました。")

    delete_objects.short_description = u"選択されたレコードを削除する。"
    active_objects.short_description = u"選択されたレコードを復活する。"


class SubcontractorAdmin(BaseAdmin):

    form = forms.SubcontractorForm

    list_display = ['name', 'is_deleted']
    list_filter = ['is_deleted']
    actions = ['delete_objects', 'active_objects']

    def get_actions(self, request):
        actions = super(SubcontractorAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def delete_objects(self, request, queryset):
        cnt = 0
        for obj in queryset:
            if not obj.is_deleted:
                obj.delete()
                cnt += 1
        self.message_user(request,  str(cnt) + u"件選択された対象が削除されました。")

    def active_objects(self, request, queryset):
        cnt = 0
        for obj in queryset:
            if obj.is_deleted:
                obj.is_deleted = False
                obj.save()
                cnt += 1
        self.message_user(request,  str(cnt) + u"件選択された対象が復活しました。")

    delete_objects.short_description = u"選択されたレコードを削除する。"
    active_objects.short_description = u"選択されたレコードを復活する。"


class ClientMemberAdmin(BaseAdmin):

    list_display = ['name', 'email', 'client', 'is_deleted']
    list_filter = ['is_deleted']
    search_fields = ['name']
    actions = ['delete_objects', 'active_objects']

    class Media:
        js = ('/static/js/jquery-2.1.4.min.js',
              '/static/js/filterlist.js',
              '/static/js/select_filter.js')

    def get_actions(self, request):
        actions = super(ClientMemberAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def delete_objects(self, request, queryset):
        cnt = 0
        for obj in queryset:
            if not obj.is_deleted:
                obj.delete()
                cnt += 1
        self.message_user(request,  str(cnt) + u"件選択された対象が削除されました。")

    def active_objects(self, request, queryset):
        cnt = 0
        for obj in queryset:
            if obj.is_deleted:
                obj.is_deleted = False
                obj.save()
                cnt += 1
        self.message_user(request,  str(cnt) + u"件選択された対象が復活しました。")

    delete_objects.short_description = u"選択されたレコードを削除する。"
    active_objects.short_description = u"選択されたレコードを復活する。"


class ProjectMemberAdmin(BaseAdmin):

    form = forms.ProjectMemberForm
    search_fields = ['project__name', 'project__client__name', 'member__first_name', 'member__last_name']

    list_display = ['project', 'display_project_client', 'member', 'start_date', 'end_date', 'status',
                    'display_eboa_user_id', 'is_deleted']
    filter_horizontal = ['stages']
    list_display_links = ['member']
    list_filter = ['status', 'is_deleted']
    inlines = (MemberAttendanceInline, MemberExpensesInline)
    actions = ['delete_objects', 'active_objects']

    def get_actions(self, request):
        actions = super(ProjectMemberAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def display_project_client(self, obj):
        return obj.project.client.name
    def display_eboa_user_id(self, obj):
        return obj.member.eboa_user_id
    display_project_client.short_description = u"関連会社"
    display_project_client.admin_order_field = 'project__client'
    display_eboa_user_id.short_description = u"EBOA連携ID"
    display_eboa_user_id.admin_order_field = 'member__eboa_user_id'

    def delete_objects(self, request, queryset):
        cnt = 0
        for obj in queryset:
            if not obj.is_deleted:
                obj.delete()
                cnt += 1
        self.message_user(request,  str(cnt) + u"件選択された対象が削除されました。")

    def active_objects(self, request, queryset):
        cnt = 0
        for obj in queryset:
            if obj.is_deleted:
                obj.is_deleted = False
                obj.save()
                cnt += 1
        self.message_user(request,  str(cnt) + u"件選択された対象が復活しました。")

    delete_objects.short_description = u"選択されたレコードを削除する。"
    active_objects.short_description = u"選択されたレコードを復活する。"

    def get_form(self, request, obj=None, **kwargs):
        form = super(ProjectMemberAdmin, self).get_form(request, obj, **kwargs)
        project_id = request.GET.get('project_id', None)
        form.base_fields['member'].queryset = Member.objects.public_all()
        if project_id:
            project = Project.objects.get(pk=project_id)
            form.base_fields['project'].initial = project
            form.base_fields['start_date'].initial = project.start_date
            form.base_fields['end_date'].initial = project.end_date
            form.base_fields['min_hours'].initial = project.min_hours
            form.base_fields['max_hours'].initial = project.max_hours
        employee_id = request.GET.get('employee_id', None)
        if employee_id:
            form.base_fields['member'].initial = Member.objects.get(employee_id=employee_id)
        return form


class ProjectRequestAdmin(BaseAdmin):
    list_display = ['project', 'year', 'month', 'request_no', 'created_user', 'created_date', 'amount']
    search_fields = ['project__name', 'request_no']
    list_display_links = ['project', 'request_no']

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.username == u"admin":
            return True
        else:
            return False

    def get_actions(self, request):
        actions = super(ProjectRequestAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class ProjectRequestHeadingAdmin(BaseAdmin):
    list_display = ['get_request_no', 'get_project_name']
    search_fields = ['project_request__request_no', 'project_request__project__name']

    def get_request_no(self, obj):
        return obj.project_request.request_no
    get_request_no.short_description = u"請求番号"
    get_request_no.admin_order_field = 'project_request__request_no'

    def get_project_name(self, obj):
        return obj.project_request.project.name
    get_project_name.short_description = u"案件名称"
    get_project_name.admin_order_field = 'project_request__project__name'

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.username == u"admin":
            return True
        else:
            return False

    def get_actions(self, request):
        actions = super(ProjectRequestHeadingAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class ProjectRequestDetailAdmin(BaseAdmin):
    list_display = ['get_request_no', 'get_project_name', 'no', 'project_member', 'total_price', 'expenses_price']
    search_fields = ['project_request__request_no', 'project_request__project__name',
                     'project_member__member__first_name', 'project_member__member__last_name']

    def get_request_no(self, obj):
        return obj.project_request.request_no
    get_request_no.short_description = u"請求番号"
    get_request_no.admin_order_field = 'project_request__request_no'

    def get_project_name(self, obj):
        return obj.project_request.project.name
    get_project_name.short_description = u"案件名称"
    get_project_name.admin_order_field = 'project_request__project__name'

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.username == u"admin":
            return True
        else:
            return False

    def get_actions(self, request):
        actions = super(ProjectRequestDetailAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class ProjectActivityAdmin(BaseAdmin):

    list_display = ['project', 'name', 'open_date', 'address', 'get_client_members', 'get_salesperson', 'is_deleted']
    list_filter = ['is_deleted']
    list_display_links = ['name']
    actions = ['delete_objects', 'active_objects']

    filter_horizontal = ['client_members', 'salesperson', 'members']

    def get_actions(self, request):
        actions = super(ProjectActivityAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_form(self, request, obj=None, **kwargs):
        form = super(ProjectActivityAdmin, self).get_form(request, obj, **kwargs)
        if obj:
            # 修正している場合、すべての案件を表示
            form.base_fields['project'].queryset = Project.objects.public_all()
        else:
            # 追加する場合、現在実施中の案件を表示
            form.base_fields['project'].queryset = Project.objects.public_filter(status=4)
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

    def delete_objects(self, request, queryset):
        cnt = 0
        for obj in queryset:
            if not obj.is_deleted:
                obj.delete()
                cnt += 1
        self.message_user(request,  str(cnt) + u"件選択された対象が削除されました。")

    def active_objects(self, request, queryset):
        cnt = 0
        for obj in queryset:
            if obj.is_deleted:
                obj.is_deleted = False
                obj.save()
                cnt += 1
        self.message_user(request,  str(cnt) + u"件選択された対象が復活しました。")

    delete_objects.short_description = u"選択されたレコードを削除する。"
    active_objects.short_description = u"選択されたレコードを復活する。"

    get_client_members.short_description = u"参加しているお客様"
    get_salesperson.short_description = u"参加している営業員"


class ProjectStageAdmin(AdminOnlyAdmin):
    pass


class PositionShipAdmin(BaseAdmin):

    list_display = ['position', 'member', 'is_deleted']
    list_filter = ['is_deleted']
    actions = ['delete_objects', 'active_objects']

    def get_actions(self, request):
        actions = super(PositionShipAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def delete_objects(self, request, queryset):
        cnt = 0
        for obj in queryset:
            if not obj.is_deleted:
                obj.delete()
                cnt += 1
        self.message_user(request,  str(cnt) + u"件選択された対象が削除されました。")

    def active_objects(self, request, queryset):
        cnt = 0
        for obj in queryset:
            if obj.is_deleted:
                obj.is_deleted = False
                obj.save()
                cnt += 1
        self.message_user(request,  str(cnt) + u"件選択された対象が復活しました。")

    delete_objects.short_description = u"選択されたレコードを削除する。"
    active_objects.short_description = u"選択されたレコードを復活する。"


class HistoryProjectAdmin(BaseAdmin):
    list_display = ['name', 'member', 'is_deleted']
    list_filter = ['is_deleted']
    filter_horizontal = ['os', 'skill', 'stages']
    actions = ['delete_objects', 'active_objects']

    def get_actions(self, request):
        actions = super(HistoryProjectAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def delete_objects(self, request, queryset):
        cnt = 0
        for obj in queryset:
            if not obj.is_deleted:
                obj.delete()
                cnt += 1
        self.message_user(request,  str(cnt) + u"件選択された対象が削除されました。")

    def active_objects(self, request, queryset):
        cnt = 0
        for obj in queryset:
            if obj.is_deleted:
                obj.is_deleted = False
                obj.save()
                cnt += 1
        self.message_user(request,  str(cnt) + u"件選択された対象が復活しました。")

    delete_objects.short_description = u"選択されたレコードを削除する。"
    active_objects.short_description = u"選択されたレコードを復活する。"


class IssueAdmin(BaseAdmin):
    list_display = ['title', 'user', 'status', 'created_date']
    list_filter = ['status']

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


class HistoryAdmin(BaseAdmin):
    list_display = ['start_datetime', 'end_datetime', 'location']
    list_filter = ['location']


class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name',
                    'is_superuser', 'is_staff', 'is_active', 'date_joined']
    list_filter = ['is_staff', 'is_superuser', 'is_active']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(CustomUserAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class LogEntryAdmin(ReadonlyAdmin):
    list_display = ['get_user_name', 'content_type', 'get_object_repr', 'get_action_flag_name', 'action_time',
                    'get_change_message']
    list_filter = (
        ActionFlagFilter,
        ('content_type', admin.RelatedOnlyFieldListFilter),
        'user'
    )
    search_fields = ['object_repr']

    def get_user_name(self, obj):
        if obj.user.first_name or obj.user.last_name:
            return u"%s %s" % (obj.user.first_name, obj.user.last_name)
        else:
            return obj.user.username
    get_user_name.short_description = u"User"
    get_user_name.admin_order_field = 'user'

    def get_action_flag_name(self, obj):
        if obj.action_flag == ADDITION:
            return u"追加"
        elif obj.action_flag == CHANGE:
            return u"修正"
        else:
            return u"削除"
    get_action_flag_name.short_description = u"操作種別"
    get_action_flag_name.admin_order_field = 'action_flag'

    def get_object_repr(self, obj):
        return obj.object_repr[:25]
    get_object_repr.short_description = u"オブジェクトの文字列表現"
    get_object_repr.admin_order_field = 'object_repr'

    def get_change_message(self, obj):
        return obj.change_message[:50]
    get_change_message.short_description = u"変更メッセージ"
    get_change_message.admin_order_field = 'change_message'

    def get_actions(self, request):
        actions = super(LogEntryAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


# Register your models here.
admin.site.register(Company, CompanyAdmin)
admin.site.register(BankInfo, BankInfoAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(SalesOffReason, SalesOffReasonAdmin)
admin.site.register(Salesperson, SalespersonAdmin)
admin.site.register(Skill)
# admin.site.register(ProjectSkill)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(ClientOrder, ClientOrderAdmin)
admin.site.register(ClientMember, ClientMemberAdmin)
admin.site.register(ProjectMember, ProjectMemberAdmin)
admin.site.register(ProjectRequest, ProjectRequestAdmin)
admin.site.register(ProjectRequestHeading, ProjectRequestHeadingAdmin)
admin.site.register(ProjectRequestDetail, ProjectRequestDetailAdmin)
admin.site.register(MemberAttendance)
admin.site.register(ProjectActivity, ProjectActivityAdmin)
admin.site.register(Subcontractor, SubcontractorAdmin)
admin.site.register(PositionShip, PositionShipAdmin)
admin.site.register(ProjectStage, ProjectStageAdmin)
admin.site.register(OS)
admin.site.register(ExpensesCategory)
admin.site.register(HistoryProject, HistoryProjectAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(History, HistoryAdmin)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(LogEntry, LogEntryAdmin)

admin.site.site_header = u'社員営業状況管理システム'
admin.site.site_title = u'管理サイト'
