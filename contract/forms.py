# coding: UTF-8
"""
Created on 2017/04/24

@author: Yang Wanjun
"""
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from . import models


class BaseForm(forms.ModelForm):
    pass


class ContractForm(BaseForm):
    class Meta:
        model = models.Contract
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ContractForm, self).__init__(*args, **kwargs)
        self.fields['contract_no'].widget.attrs.update({'readonly': 'readonly'})
        self.fields['allowance_time_max'].widget.attrs.update({
            'onchange': 'set_allowance_overtime_memo("%s", "%s", "%s")' % ('id_allowance_time_max',
                                                                           'id_allowance_overtime',
                                                                           'id_allowance_overtime_memo')
        })
        self.fields['allowance_overtime'].widget.attrs.update({
            'onchange': 'set_allowance_overtime_memo("%s", "%s", "%s")' % ('id_allowance_time_max',
                                                                           'id_allowance_overtime',
                                                                           'id_allowance_overtime_memo')
        })
        self.fields['allowance_time_min'].widget.attrs.update({
            'onchange': 'set_allowance_absenteeism_memo("%s", "%s", "%s")' % ('id_allowance_time_min',
                                                                              'id_allowance_absenteeism',
                                                                              'id_allowance_absenteeism_memo')
        })
        self.fields['allowance_absenteeism'].widget.attrs.update({
            'onchange': 'set_allowance_absenteeism_memo("%s", "%s", "%s")' % ('id_allowance_time_min',
                                                                              'id_allowance_absenteeism',
                                                                              'id_allowance_absenteeism_memo')
        })

    contract_date = forms.DateField(widget=AdminDateWidget, label=u"契約日")
    employment_date = forms.DateField(widget=AdminDateWidget, label=u"雇用日")
    start_date = forms.DateField(widget=AdminDateWidget, label=u"雇用開始日")
    end_date = forms.DateField(widget=AdminDateWidget, label=u"雇用終了日", required=False)
