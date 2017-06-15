# coding: UTF-8
"""
Created on 2017/04/24

@author: Yang Wanjun
"""
from django.http import HttpResponse
from django.contrib import admin
from django.utils.translation import ugettext as _
from django.utils.text import get_text_list
from django.utils.encoding import force_text
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from utils import common
from . import models, forms
from eb import models as sales_models
# Register your models here.


def get_full_name(obj):
    return "%s %s" % (obj.first_name, obj.last_name)
get_full_name.short_description = u"名前"
get_full_name.admin_order_field = "first_name"


class BaseAdmin(admin.ModelAdmin):

    class Media:
        js = ('/static/admin/js/jquery-2.1.4.min.js',
              '/static/admin/js/base.js')

    def get_actions(self, request):
        actions = super(BaseAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

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


class ContractAdmin(BaseAdmin):
    list_display = ['member', 'contract_no', 'member_type', 'start_date', 'end_date']
    search_fields = ('member__first_name', 'member__last_name', 'contract_no')


class BpContractAdmin(BaseAdmin):
    form = forms.BpContractForm
    list_display = ['member', 'company', 'start_date', 'end_date', 'is_hourly_pay', 'allowance_base']
    search_fields = ('member__first_name', 'member__last_name', 'company')
    fieldsets = (
        (None, {'fields': ('member',
                           'start_date',
                           'end_date',
                           ('is_hourly_pay', 'is_fixed_cost', 'is_show_formula'),
                           ('allowance_base', 'allowance_base_memo'),
                           ('allowance_time_min', 'calculate_type', 'business_days'),
                           'allowance_time_max',
                           'allowance_time_memo',
                           ('calculate_time_min', 'calculate_time_max'),
                           ('allowance_overtime', 'allowance_overtime_memo'),
                           ('allowance_absenteeism', 'allowance_absenteeism_memo'),
                           ('allowance_other', 'allowance_other_memo'),
                           'comment')}),
    )

    class Media:
        css = {'all': ('/static/admin/css/custom_base.css',)
               }
        js = ('/static/admin/js/calc_contract.js',)

    def get_form(self, request, obj=None, **kwargs):
        form = super(BpContractAdmin, self).get_form(request, obj, **kwargs)
        member_id = request.GET.get('member_id')
        try:
            member = sales_models.Member.objects.get(pk=member_id)
            form.base_fields['member'].initial = member
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            pass
        return form


class ContractAdminSite(admin.AdminSite):
    site_header = "契約管理システム"
    site_title = "管理サイト"


contract_admin_site = ContractAdminSite(name='contract')
contract_admin_site.register(models.Contract, ContractAdmin)
contract_admin_site.register(models.BpContract, BpContractAdmin)
