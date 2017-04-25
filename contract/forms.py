# coding: UTF-8
"""
Created on 2017/04/24

@author: Yang Wanjun
"""
from django import forms
from . import models


class BaseForm(forms.ModelForm):
    pass


class ContractForm(BaseForm):
    class Meta:
        model = models.Contract
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ContractForm, self).__init__(*args, **kwargs)
        # for name in ('employment_period_comment',
        #              'business_other',
        #              'business_time',
        #              'allowance_date_comment',
        #              'allowance_change_comment',
        #              'bonus_comment',
        #              'holiday_comment',
        #              'paid_vacation_comment',
        #              'non_paid_vacation_comment',
        #              'retire_comment',
        #              'comment'):
        #     self.fields[name].widget.attrs.update({
        #         'rows': 5,
        #     })
