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
from django.core.validators import MaxLengthValidator
from django.utils.translation import ugettext as _
from django.db.models import Max
from django.utils.encoding import force_text
from django.utils.text import get_text_list
from django.template import Context, Template

import forms
from . import models, biz, biz_config
from utils import common, constants


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


class RelatedUserFilter(admin.RelatedOnlyFieldListFilter):
    def field_choices(self, field, request, model_admin):
        pk_list = set(model_admin.get_queryset(request).values_list(field.name, flat=True))
        user_list = User.objects.filter(pk__in=pk_list)
        return [(u.pk, u"%s %s" % (u.first_name, u.last_name)) for u in user_list]


class ProjectSkillInline(admin.TabularInline):
    model = models.ProjectSkill
    extra = 0


class ProjectMemberInline(admin.TabularInline):
    model = models.ProjectMember
    form = forms.ProjectMemberForm
    formset = forms.ProjectMemberFormset
    extra = 0

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(ProjectMemberInline, self).get_formset(request, obj, **kwargs)

        class AdminFormsetWithRequest(formset):
            def __new__(cls, *args, **kwargs):
                kwargs.update({'request': request})
                return formset(*args, **kwargs)

        return AdminFormsetWithRequest

    def get_queryset(self, request):
        queryset = super(ProjectMemberInline, self).get_queryset(request)
        return queryset.filter(member__is_retired=False, member__is_deleted=False).order_by('end_date', 'start_date')


class EmployeeExpensesInline(admin.TabularInline):
    model = models.EmployeeExpenses
    extra = 0

    def get_queryset(self, request):
        queryset = super(EmployeeExpensesInline, self).get_queryset(request)
        return queryset.filter(is_deleted=False)


class MemberExpensesInline(admin.TabularInline):
    model = models.MemberExpenses
    extra = 0

    def get_queryset(self, request):
        queryset = super(MemberExpensesInline, self).get_queryset(request)
        return queryset.filter(is_deleted=False)


class MemberAttendanceInline(admin.TabularInline):
    form = forms.MemberAttendanceForm
    model = models.MemberAttendance
    extra = 0

    def get_queryset(self, request):
        queryset = super(MemberAttendanceInline, self).get_queryset(request)
        return queryset.filter(is_deleted=False)


class MemberSectionPeriodInline(admin.TabularInline):
    model = models.MemberSectionPeriod
    extra = 1
    form = forms.MemberSectionPeriodForm
    formset = forms.MemberSectionPeriodFormset


class MemberSalespersonPeriodInline(admin.TabularInline):
    model = models.MemberSalespersonPeriod
    extra = 1
    form = forms.MemberSalespersonPeriodForm
    formset = forms.MemberSalespersonPeriodFormset

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(MemberSalespersonPeriodInline, self).get_formset(request, obj, **kwargs)

        class AdminFormsetWithRequest(formset):
            def __new__(cls, *args, **kwargs):
                kwargs.update({'request': request})
                return formset(*args, **kwargs)

        return AdminFormsetWithRequest


class DegreeInline(admin.TabularInline):
    model = models.Degree
    extra = 0


class BatchCarbonCopyInline(admin.TabularInline):
    model = models.BatchCarbonCopy
    form = forms.BatchCarbonCopyForm
    extra = 0


class PositionShipInline(admin.TabularInline):
    model = models.PositionShip
    form = forms.PositionShipForm
    extra = 0


def get_full_name(obj):
    return "%s %s" % (obj.first_name, obj.last_name)
get_full_name.short_description = u"名前"
get_full_name.admin_order_field = "first_name"


class BaseAdmin(admin.ModelAdmin):

    class Media:
        js = ('https://ajaxzip3.github.io/ajaxzip3.js',
              '/static/admin/js/jquery-2.1.4.min.js',
              '/static/admin/js/filterlist.js',
              '/static/admin/js/select_filter.js',
              '/static/admin/js/base.js')

    def construct_change_message(self, request, form, formsets, add=False):
        """
        Construct a change message from a changed object.
        """
        change_message = []
        if add:
            change_message.append(_('Added.'))
        elif form.changed_data:
            changed_list = []
            for field in form.changed_data:
                changed_list.append(u"%s(%s→%s)" % common.get_form_changed_value(form, field))
            change_message.append(_('Changed %s.') % get_text_list(changed_list, _('and')))

        if formsets:
            for formset in formsets:
                for added_object in formset.new_objects:
                    change_message.append(_('Added %(name)s "%(object)s".')
                                          % {'name': force_text(added_object._meta.verbose_name),
                                             'object': force_text(added_object)})
                for changed_object, changed_fields in formset.changed_objects:
                    changed_list = []
                    for changed_data in common.get_formset_changed_value(formset, changed_object, changed_fields):
                        changed_list.append(u"%s(%s→%s)" % changed_data)
                    change_message.append(_('Changed %(list)s for %(name)s "%(object)s".')
                                          % {'list': get_text_list(changed_list, _('and')),
                                             'name': force_text(changed_object._meta.verbose_name),
                                             'object': force_text(changed_object)})
                for deleted_object in formset.deleted_objects:
                    change_message.append(_('Deleted %(name)s "%(object)s".')
                                          % {'name': force_text(deleted_object._meta.verbose_name),
                                             'object': force_text(deleted_object)})
        change_message = ' '.join(change_message)
        return change_message or _('No fields changed.')

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

    def send_user_create_mail(self, user):
        """ユーザ作成後、お知らせのメールを送信する

        :param user:
        :return:
        """
        try:
            system_name = biz_config.get_sales_system_name()
            mail_title = u"【%s】アカウント作成　- %s %s" % (system_name, user.first_name, user.last_name)
            body_template = models.Config.get(constants.CONFIG_USER_CREATE_MAIL_BODY)
            if body_template:
                t = Template(body_template)
                context = {'user': user,
                           'system_name': system_name,
                           }
                ctx = Context(context)
                mail_body = t.render(ctx)
                from_email = models.Config.get(constants.CONFIG_ADMIN_EMAIL_ADDRESS)
                recipient_list = [user.email]
                connection = models.BatchManage.get_custom_connection()
                email = models.EmailMultiAlternativesWithEncoding(
                    subject=mail_title,
                    body=mail_body,
                    from_email=from_email,
                    to=recipient_list,
                    cc=[],
                    connection=connection
                )
                email.send()
        except:
            pass


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
        js = ('/static/admin/js/jquery-2.1.4.min.js',
              '/static/admin/js/readonly.js')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
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
        if models.Company.objects.all().count() > 0:
            # データが存在する場合、追加を禁止
            return False
        else:
            return True


class BankInfoAdmin(BaseAdmin):

    list_display = ['bank_name', 'is_deleted']
    actions = ['delete_objects', 'active_objects']

    def get_form(self, request, obj=None, **kwargs):
        form = super(BankInfoAdmin, self).get_form(request, obj, **kwargs)
        company = models.Company.objects.all()[0]
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
    list_display = ['name', 'parent', 'org_type', 'is_on_sales', 'is_deleted']
    list_filter = ['is_on_sales', 'is_deleted']
    actions = ['delete_objects', 'active_objects']
    inlines = (PositionShipInline,)

    def get_form(self, request, obj=None, **kwargs):
        form = super(SectionAdmin, self).get_form(request, obj, **kwargs)
        company = models.Company.objects.all()[0]
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
    list_display = ['employee_id', get_full_name, 'subcontractor', 'is_user_created',
                    'created_date', 'updated_date', 'is_retired']
    list_display_links = [get_full_name]
    list_filter = ['member_type', NoUserFilter,
                   'is_retired', 'is_deleted']
    search_fields = ['first_name', 'last_name', 'employee_id']
    inlines = (DegreeInline, MemberSectionPeriodInline, MemberSalespersonPeriodInline, EmployeeExpensesInline)
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
        (u"勤務情報", {'fields': ['member_type', 'join_date', 'email', 'notify_type', 'section', 'company',
                              'subcontractor', 'is_on_sales', 'sales_off_reason', 'is_retired']})
    )

    def get_actions(self, request):
        actions = super(MemberAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def is_user_created(self, obj):
        return obj.user is not None
    is_user_created.short_description = u"ユーザ作成"
    is_user_created.admin_order_field = "user"
    is_user_created.boolean = True

    def get_form(self, request, obj=None, **kwargs):
        form = super(MemberAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['section'].queryset = models.Section.objects.public_filter(is_on_sales=False)
        if obj is None:
            form.base_fields['employee_id'].initial = biz.get_bp_next_employee_id()
        return form

    def save_model(self, request, obj, form, change):
        if not change:
            obj.employee_id = datetime.datetime.now().strftime('%H%M%S%f')
        super(MemberAdmin, self).save_model(request, obj, form, change)
        if not change and obj.pk:
            try:
                obj.employee_id = 'BP%05d' % (obj.pk,)
                obj.save()
            except:
                pass

    def change_view(self, request, object_id, form_url='', extra_context=None):
        member = models.Member.objects.get(pk=object_id)
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
                    self.send_user_create_mail(user)
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
        (u"勤務情報", {'fields': ('member_type', 'email', 'notify_type', 'section', 'company', 'is_retired')})
    )
    actions = ['create_users', 'delete_objects', 'active_objects']

    def get_actions(self, request):
        actions = super(SalespersonAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_form(self, request, obj=None, **kwargs):
        form = super(SalespersonAdmin, self).get_form(request, obj, **kwargs)
        company = models.Company.objects.all()[0]
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
                    user.first_name = member.first_name
                    user.last_name = member.last_name
                    user.save()
                    self.send_user_create_mail(user)
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
    list_filter = ['status', 'salesperson', 'is_deleted']
    search_fields = ['name', 'client__name']
    inlines = (ProjectSkillInline, ProjectMemberInline)
    actions = ['delete_objects', 'active_objects']

    class Media:
        js = ('/static/admin/js/ready.js',)
        css = {'all': ('/static/admin/css/admin.css',)
               }

    def _create_formsets(self, request, obj, change):
        formsets, inline_instances = super(ProjectAdmin, self)._create_formsets(request, obj, change)
        for fm in formsets:
            if fm.model == models.ProjectMember:
                fm.form.base_fields['min_hours'].initial = obj.min_hours
                fm.form.base_fields['max_hours'].initial = obj.max_hours
        return formsets, inline_instances

    def get_inline_formsets(self, request, formsets, inline_instances,
                            obj=None):
        inline_admin_formsets = super(ProjectAdmin, self).get_inline_formsets(request, formsets, inline_instances, obj)

        return inline_admin_formsets

    def get_actions(self, request):
        actions = super(ProjectAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_form(self, request, obj=None, **kwargs):
        form = super(ProjectAdmin, self).get_form(request, obj, **kwargs)
        if obj and obj.client:
            form.base_fields['boss'].queryset = models.ClientMember.objects.filter(client=obj.client)
            form.base_fields['middleman'].queryset = models.ClientMember.objects.filter(client=obj.client)
        return form

    def save_related(self, request, form, formsets, change):
        super(ProjectAdmin, self).save_related(request, form, formsets, change)
        # 保存時、配下のすべてのメンバーの営業員項目を案件の営業員に更新する。
        project = form.instance
        # today = datetime.date.today()
        # if project.salesperson:
        #     for pm in project.projectmember_set.filter(is_deleted=False, start_date__lte=today, end_date__gte=today):
        #         member = pm.member
        #         member.salesperson = project.salesperson
        #         member.save()
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
        banks = models.BankInfo.objects.public_all()
        if project_id:
            project = models.Project.objects.public_filter(pk=project_id)
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
        js = ('/static/admin/js/jquery-2.1.4.min.js',
              '/static/admin/js/filterlist.js',
              '/static/admin/js/select_filter.js')

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

    # def change_view(self, request, object_id, form_url='', extra_context=None):
    #     project_member = models.ProjectMember.objects.get(pk=object_id)
    #     if project_member.member.is_belong_to(request.user, datetime.date.today()):
    #         try:
    #             self.fieldsets[2][1]['fields'].remove('cost')
    #         except ValueError:
    #             pass
    #     return super(ProjectMemberAdmin, self).change_view(request, object_id, form_url, extra_context)

    def get_form(self, request, obj=None, **kwargs):
        form = super(ProjectMemberAdmin, self).get_form(request, obj, **kwargs)
        project_id = request.GET.get('project_id', None)
        form.base_fields['member'].queryset = models.Member.objects.public_all()
        if project_id:
            project = models.Project.objects.get(pk=project_id)
            form.base_fields['project'].initial = project
            form.base_fields['start_date'].initial = project.start_date
            form.base_fields['end_date'].initial = project.end_date
            form.base_fields['min_hours'].initial = project.min_hours
            form.base_fields['max_hours'].initial = project.max_hours
        employee_id = request.GET.get('employee_id', None)
        if employee_id:
            form.base_fields['member'].initial = models.Member.objects.get(employee_id=employee_id)
        if obj and not obj.member.is_belong_to(request.user, datetime.date.today()):
            del form.base_fields['price']
            del form.base_fields['min_hours']
            del form.base_fields['max_hours']
            del form.base_fields['plus_per_hour']
            del form.base_fields['minus_per_hour']
            if 'hourly_pay' in form.base_fields:
                del form.base_fields['hourly_pay']
        return form


class ProjectRequestAdmin(ReadonlyAdmin):
    list_display = ['project', 'year', 'month', 'request_no', 'created_user', 'created_date', 'amount']
    search_fields = ['project__name', 'request_no']
    list_display_links = ['project', 'request_no']

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def get_actions(self, request):
        actions = super(ProjectRequestAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class ProjectRequestHeadingAdmin(ReadonlyAdmin):
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

    def get_actions(self, request):
        actions = super(ProjectRequestHeadingAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class ProjectRequestDetailAdmin(ReadonlyAdmin):
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
            form.base_fields['project'].queryset = models.Project.objects.public_all()
        else:
            # 追加する場合、現在実施中の案件を表示
            form.base_fields['project'].queryset = models.Project.objects.public_filter(status=4)
        project_id = request.GET.get('project_id', None)
        if project_id:
            project = models.Project.objects.get(pk=project_id)
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

    list_display = ['position', 'member', 'section', 'is_deleted']
    list_filter = ['is_deleted']
    actions = ['delete_objects', 'active_objects']

    def get_actions(self, request):
        actions = super(PositionShipAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_form(self, request, obj=None, **kwargs):
        form = super(PositionShipAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['section'].queryset = models.Section.objects.public_filter(is_on_sales=True)
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
    list_display = ['title', 'created_user', 'status', 'created_date']
    list_filter = ['status']

    def get_form(self, request, obj=None, **kwargs):
        form = super(IssueAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['present_user'].initial = request.user
        return form

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_user = request.user
        obj.save(updated_user=request.user)


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
        ('user', RelatedUserFilter),
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


class BatchManageAdmin(BaseAdmin):
    list_display = ['name', 'title', 'cron_tab', 'is_active', 'mail_title', 'is_deleted']
    list_filter = ['is_active', 'is_deleted']
    inlines = (BatchCarbonCopyInline,)

    def get_actions(self, request):
        actions = super(BatchManageAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class ConfigAdmin(BaseAdmin):
    form = forms.ConfigForm
    list_display = ['name', 'value']


NEW_USERNAME_LENGTH = 50


def reset_username_length():
    """既存のユーザ名の長さは３０なので、ここ５０に設定する。

    この設定はただフォームの検証時のmax lengthを５０に設定するだけ、DBの項目の長さは変更されません。

    :return:
    """
    username = User._meta.get_field("username")
    username.max_length = NEW_USERNAME_LENGTH
    for v in username.validators:
        if isinstance(v, MaxLengthValidator):
            v.limit_value = NEW_USERNAME_LENGTH

reset_username_length()

# Register your models here.
admin.site.register(models.Company, CompanyAdmin)
admin.site.register(models.BankInfo, BankInfoAdmin)
admin.site.register(models.Section, SectionAdmin)
admin.site.register(models.Member, MemberAdmin)
admin.site.register(models.SalesOffReason, SalesOffReasonAdmin)
admin.site.register(models.Salesperson, SalespersonAdmin)
admin.site.register(models.Skill)
# admin.site.register(ProjectSkill)
admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.Client, ClientAdmin)
admin.site.register(models.ClientOrder, ClientOrderAdmin)
admin.site.register(models.ClientMember, ClientMemberAdmin)
admin.site.register(models.ProjectMember, ProjectMemberAdmin)
admin.site.register(models.ProjectRequest, ProjectRequestAdmin)
admin.site.register(models.ProjectRequestHeading, ProjectRequestHeadingAdmin)
admin.site.register(models.ProjectRequestDetail, ProjectRequestDetailAdmin)
admin.site.register(models.MemberAttendance)
admin.site.register(models.ProjectActivity, ProjectActivityAdmin)
admin.site.register(models.Subcontractor, SubcontractorAdmin)
admin.site.register(models.PositionShip, PositionShipAdmin)
admin.site.register(models.ProjectStage, ProjectStageAdmin)
admin.site.register(models.OS)
admin.site.register(models.ExpensesCategory)
admin.site.register(models.HistoryProject, HistoryProjectAdmin)
admin.site.register(models.Issue, IssueAdmin)
admin.site.register(models.History, HistoryAdmin)
admin.site.register(models.BatchManage, BatchManageAdmin)
admin.site.register(models.Config, ConfigAdmin)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(LogEntry, LogEntryAdmin)

admin.site.site_header = constants.NAME_SYSTEM
admin.site.site_title = u'管理サイト'
