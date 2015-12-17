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
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

import forms
from .models import Company, Section, Member, Salesperson, Project, Client, ClientMember, \
    ProjectMember, Skill, ProjectSkill, ProjectActivity, Subcontractor, PositionShip,\
    ProjectStage, OS, HistoryProject, MemberAttendance, Degree, ClientOrder, \
    create_group_salesperson, MemberExpenses, ExpensesCategory, BankInfo
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
    form = forms.ProjectMemberForm
    extra = 1


class MemberExpensesInline(admin.TabularInline):
    model = MemberExpenses
    extra = 1


class MemberAttendanceInline(admin.TabularInline):
    form = forms.MemberAttendanceForm
    model = MemberAttendance
    extra = 1


class DegreeInline(admin.TabularInline):
    model = Degree
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


class BankInfoAdmin(admin.ModelAdmin):

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


class SectionAdmin(admin.ModelAdmin):

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


class MemberAdmin(admin.ModelAdmin):

    form = forms.MemberForm
    list_display = ['employee_id', get_full_name, 'section', 'subcontractor', 'salesperson',
                    'user', 'is_retired', 'is_deleted']
    list_display_links = [get_full_name]
    list_filter = ['member_type', 'section', 'salesperson', NoUserFilter,
                   'is_retired', 'is_deleted']
    search_fields = ['first_name', 'last_name']
    inlines = (DegreeInline,)
    actions = ['delete_objects', 'active_objects']
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
        (u"勤務情報", {'fields': ('member_type', 'join_date', 'email', 'section', 'company', 'subcontractor', 'salesperson', 'cost', 'is_retired')})
    )

    class Media:
        js = ('http://ajaxzip3.googlecode.com/svn/trunk/ajaxzip3/ajaxzip3.js',
              '/static/js/jquery-2.1.4.min.js',
              '/static/js/filterlist.js',
              '/static/js/select_filter.js')

    def get_actions(self, request):
        actions = super(MemberAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_queryset(self, request):
        query_set = admin.ModelAdmin.get_queryset(self, request)
        if request.user.is_superuser:
            return query_set
        elif request.user.salesperson.member_type == 0 and request.user.salesperson.section:
            # 営業部長の場合
            section = request.user.salesperson.section
            salesperson_list = section.salesperson_set.all()
            return query_set.filter(salesperson__in=salesperson_list)
        else:
            return query_set.filter(salesperson=request.user.salesperson)

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

    def response_change(self, request, obj):
        if request.GET.get('from') == "portal":
            return HttpResponse('''
               <script type="text/javascript">
                  window.close();
               </script>''')
        else:
            response = super(MemberAdmin, self).response_change(request, obj)
            return response

    def response_add(self, request, obj, post_url_continue=None):
        if request.GET.get('from') == "portal":
            return HttpResponse('''
               <script type="text/javascript">
                  window.close();
               </script>''')
        else:
            response = super(MemberAdmin, self).response_add(request, obj)
            return response


class SalespersonAdmin(admin.ModelAdmin):

    form = forms.SalespersonForm
    list_display = ['employee_id', get_full_name, 'email', 'section', 'member_type', 'is_user_created', 'is_deleted']
    list_display_links = [get_full_name]
    search_fields = ['first_name', 'last_name']
    list_filter = ['member_type', 'section', NoUserFilter, 'is_deleted']
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
        (u"勤務情報", {'fields': ('member_type', 'email', 'section', 'company', 'is_retired')})
    )
    actions = ['create_users', 'delete_objects', 'active_objects']

    class Media:
        js = ('http://ajaxzip3.googlecode.com/svn/trunk/ajaxzip3/ajaxzip3.js',)

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

    def get_queryset(self, request):
        query_set = admin.ModelAdmin.get_queryset(self, request)
        if request.user.is_superuser:
            return query_set
        elif request.user.salesperson.member_type == 0 and request.user.salesperson.section:
            # 営業部長の場合は該当部署のすべての営業員が変更できる。
            return query_set.filter(section=request.user.salesperson.section)
        else:
            return query_set.filter(pk=request.user.salesperson.pk)

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


class ProjectAdmin(admin.ModelAdmin):
    form = forms.ProjectForm
    list_display = ['name', 'client', 'start_date', 'end_date', 'status', 'salesperson', 'is_deleted']
    list_display_links = ['name']
    list_filter = [ProjectNameListFilter, 'status', 'salesperson', 'is_deleted']
    search_fields = ['name']
    inlines = (ProjectSkillInline, ProjectMemberInline)
    actions = ['delete_objects', 'active_objects']

    class Media:
        js = ('/static/js/jquery-2.1.4.min.js',
              '/static/js/filterlist.js',
              '/static/js/select_filter.js',
              '/static/js/base.js')

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

    def get_queryset(self, request):
        query_set = admin.ModelAdmin.get_queryset(self, request)
        if request.user.is_superuser:
            return query_set
        elif request.user.salesperson.member_type == 0 and request.user.salesperson.section:
            # 営業部長の場合
            section = request.user.salesperson.section
            salesperson_list = section.salesperson_set.all()
            return query_set.filter(salesperson__in=salesperson_list)
        else:
            return query_set.filter(salesperson=request.user.salesperson)

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

    def response_add(self, request, obj, post_url_continue=None):
        if request.GET.get('from') == "portal":
            return HttpResponse('''
               <script type="text/javascript">
                  window.close();
               </script>''')
        else:
            response = super(ProjectAdmin, self).response_add(request, obj)
            return response

    def response_change(self, request, obj):
        if request.GET.get('from') == "portal":
            return HttpResponse('''
               <script type="text/javascript">
                  window.close();
               </script>''')
        else:
            response = super(ProjectAdmin, self).response_change(request, obj)
            return response


class ClientAdmin(admin.ModelAdmin):

    form = forms.ClientForm

    list_display = ['name', 'is_request_uploaded', 'is_deleted']
    list_filter = ['is_deleted']
    actions = ['delete_objects', 'active_objects']

    class Media:
        js = ('http://ajaxzip3.googlecode.com/svn/trunk/ajaxzip3/ajaxzip3.js',)

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


class ClientOrderAdmin(admin.ModelAdmin):
    list_display = ['project', 'name', 'start_date', 'end_date', 'is_deleted']
    list_filter = ['is_deleted']
    actions = ['delete_objects', 'active_objects']

    class Media:
        js = ('/static/js/jquery-2.1.4.min.js',
              '/static/js/filterlist.js',
              '/static/js/select_filter.js')

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
            project = Project.objects.get(pk=project_id)
            form.base_fields['project'].initial = project
            form.base_fields['name'].initial = project.name
        if ym:
            first_day = datetime.date(int(ym[:4]), int(ym[4:]), 1)
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

    def response_change(self, request, obj):
        if request.GET.get('from') == "portal":
            return HttpResponse('''
               <script type="text/javascript">
                  window.close();
               </script>''')
        else:
            response = super(ClientOrderAdmin, self).response_change(request, obj)
            return response

    def response_add(self, request, obj, post_url_continue=None):
        if request.GET.get('from') == "portal":
            return HttpResponse('''
               <script type="text/javascript">
                  window.close();
               </script>''')
        else:
            response = super(ClientOrderAdmin, self).response_add(request, obj)
            return response


class SubcontractorAdmin(admin.ModelAdmin):

    form = forms.SubcontractorForm

    list_display = ['name', 'is_deleted']
    list_filter = ['is_deleted']
    actions = ['delete_objects', 'active_objects']

    class Media:
        js = ('http://ajaxzip3.googlecode.com/svn/trunk/ajaxzip3/ajaxzip3.js',)

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


class ClientMemberAdmin(admin.ModelAdmin):

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


class ProjectMemberAdmin(admin.ModelAdmin):

    form = forms.ProjectMemberForm
    search_fields = ['project__name', 'member__first_name', 'member__last_name']

    list_display = ['project', 'display_project_client', 'member', 'start_date', 'end_date', 'status', 'is_deleted']
    filter_horizontal = ['stages']
    list_display_links = ['member']
    list_filter = ['status', 'is_deleted']
    inlines = (MemberAttendanceInline, MemberExpensesInline)
    actions = ['delete_objects', 'active_objects']

    class Media:
        js = ('/static/js/jquery-2.1.4.min.js',
              '/static/js/filterlist.js',
              '/static/js/select_filter.js',
              '/static/js/base.js')

    def get_actions(self, request):
        actions = super(ProjectMemberAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def display_project_client(self, obj):
        return obj.project.client.name

    display_project_client.short_description = u"関連会社"
    display_project_client.admin_order_field = 'project__client'

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
        if project_id:
            project = Project.objects.get(pk=project_id)
            form.base_fields['project'].initial = project
            form.base_fields['start_date'].initial = project.start_date
            form.base_fields['end_date'].initial = project.end_date
        employee_id = request.GET.get('employee_id', None)
        if employee_id:
            form.base_fields['member'].initial = Member.objects.get(employee_id=employee_id)
        return form

    def response_change(self, request, obj):
        if request.GET.get('from') == "portal":
            return HttpResponse('''
               <script type="text/javascript">
                  window.close();
               </script>''')
        else:
            response = super(ProjectMemberAdmin, self).response_change(request, obj)
            return response

    def response_add(self, request, obj, post_url_continue=None):
        if request.GET.get('from') == "portal":
            return HttpResponse('''
               <script type="text/javascript">
                  window.close();
               </script>''')
        else:
            response = super(ProjectMemberAdmin, self).response_add(request, obj)
            return response


class ProjectActivityAdmin(admin.ModelAdmin):

    list_display = ['project', 'name', 'open_date', 'address', 'get_client_members', 'get_salesperson', 'is_deleted']
    list_filter = ['is_deleted']
    list_display_links = ['name']
    actions = ['delete_objects', 'active_objects']

    filter_horizontal = ['client_members', 'salesperson', 'members']

    class Media:
        js = ('/static/js/jquery-2.1.4.min.js',
              '/static/js/filterlist.js',
              '/static/js/select_filter.js')

    def get_actions(self, request):
        actions = super(ProjectActivityAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

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

    def response_change(self, request, obj):
        if request.GET.get('from') == "portal":
            return HttpResponse('''
               <script type="text/javascript">
                  window.close();
               </script>''')
        else:
            response = super(ProjectActivityAdmin, self).response_change(request, obj)
            return response

    def response_add(self, request, obj, post_url_continue=None):
        if request.GET.get('from') == "portal":
            return HttpResponse('''
               <script type="text/javascript">
                  window.close();
               </script>''')
        else:
            response = super(ProjectActivityAdmin, self).response_add(request, obj)
            return response

    get_client_members.short_description = u"参加しているお客様"
    get_salesperson.short_description = u"参加している営業員"


class PositionShipAdmin(admin.ModelAdmin):

    list_display = ['position', 'member', 'is_deleted']
    list_filter = ['is_deleted']
    actions = ['delete_objects', 'active_objects']

    class Media:
        js = ('/static/js/jquery-2.1.4.min.js',
              '/static/js/filterlist.js',
              '/static/js/select_filter.js')

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


class HistoryProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'member', 'is_deleted']
    list_filter = ['is_deleted']
    filter_horizontal = ['os', 'skill', 'stages']
    actions = ['delete_objects', 'active_objects']

    class Media:
        js = ('/static/js/jquery-2.1.4.min.js',
              '/static/js/filterlist.js',
              '/static/js/select_filter.js')

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


# Register your models here.
admin.site.register(Company, CompanyAdmin)
admin.site.register(BankInfo, BankInfoAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Salesperson, SalespersonAdmin)
admin.site.register(Skill)
# admin.site.register(ProjectSkill)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(ClientOrder, ClientOrderAdmin)
admin.site.register(ClientMember, ClientMemberAdmin)
admin.site.register(ProjectMember, ProjectMemberAdmin)
# admin.site.register(MemberAttendance, MemberAttendanceAdmin)
admin.site.register(ProjectActivity, ProjectActivityAdmin)
admin.site.register(Subcontractor, SubcontractorAdmin)
admin.site.register(PositionShip, PositionShipAdmin)
admin.site.register(ProjectStage)
admin.site.register(OS)
admin.site.register(ExpensesCategory)
admin.site.register(HistoryProject, HistoryProjectAdmin)

admin.site.site_header = u'社員営業状況管理システム'
admin.site.site_title = u'管理サイト'