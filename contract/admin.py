# coding: UTF-8
"""
Created on 2017/04/24

@author: Yang Wanjun
"""
from django.contrib import admin
from django.utils.translation import ugettext as _
from django.utils.text import get_text_list
from django.utils.encoding import force_text

from utils import common
from . import models
# Register your models here.


class BaseAdmin(admin.ModelAdmin):

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


class ContractAdmin(BaseAdmin):
    list_display = ['member', 'contract_no', 'member_type', 'start_date', 'end_date']
    search_fields = ('member__first_name', 'member__last_name', 'contract_no')


class ContractAdminSite(admin.AdminSite):
    site_header = "契約管理システム"
    site_title = "管理サイト"


contract_admin_site = ContractAdminSite(name='contract')
contract_admin_site.register(models.Contract, ContractAdmin)
