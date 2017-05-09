# coding: UTF-8
"""
Created on 2017/04/24

@author: Yang Wanjun
"""
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from . import models
from utils import common


class BaseForm(forms.ModelForm):
    pass


class MemberForm(BaseForm):
    class Meta:
        model = models.Member
        fields = '__all__'

    birthday = forms.DateField(widget=AdminDateWidget, label=u"生年月日")
    join_date = forms.DateField(widget=AdminDateWidget, label=u"入社年月日")
    post_code = forms.CharField(max_length=7,
                                widget=forms.TextInput(
                                    attrs={'onKeyUp': "AjaxZip3.zip2addr(this,'','address1','address1');"}),
                                label=u"郵便番号",
                                help_text=u"数値だけを入力してください、例：1230034",
                                required=False)

    def __init__(self, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)
        self.fields['id_from_api'].widget.attrs.update({'readonly': 'readonly'})

    def clean(self):
        cleaned_data = super(MemberForm, self).clean()
        if self.instance and not self.instance.pk:
            cleaned_data["id_from_api"] = models.Member.get_max_api_id()
        return cleaned_data


class ContractMemberForm(BaseForm):
    class Meta:
        model = models.Member
        fields = ('employee_id', 'first_name', 'last_name', 'member_type', 'subcontractor', 'is_on_sales', 'is_retired')

    def __init__(self, *args, **kwargs):
        super(ContractMemberForm, self).__init__(*args, **kwargs)
        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'readonly': 'readonly'})


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


class BpContractForm(BaseForm):
    class Meta:
        model = models.BpContract
        exclude = ('company',)

    def __init__(self, *args, **kwargs):
        super(BpContractForm, self).__init__(*args, **kwargs)
        for name in ('allowance_base_memo', 'allowance_other_memo'):
            self.fields[name].widget.attrs.update({'style': 'width: 100px;'})
        self.fields['allowance_base'].widget.attrs.update({
            'onchange': 'calculate_plus_minus(this, "allowance_base", '
                        '"allowance_time_min", "allowance_time_max", '
                        '"allowance_absenteeism", "allowance_overtime")'
        })
        self.fields['allowance_time_min'].widget.attrs.update({
            'onchange': 'calculate_minus_from_min_hour(this, "allowance_base", '
                        '"allowance_time_min", "allowance_time_max", '
                        '"allowance_absenteeism", "allowance_overtime")'
        })
        self.fields['allowance_time_max'].widget.attrs.update({
            'onchange': 'calculate_plus_from_max_hour(this, "allowance_base", '
                        '"allowance_time_min", "allowance_time_max", '
                        '"allowance_absenteeism", "allowance_overtime")'
        })
        self.fields['comment'].widget.attrs.update({'rows': '1', 'style': 'width: 100px;'})

    def clean(self):
        cleaned_data = super(BpContractForm, self).clean()
        member = cleaned_data.get('member', None)
        company = cleaned_data.get('company', None)
        if not company and member and self.instance:
            self.instance.company = member.subcontractor


class BpContractFormset(forms.BaseInlineFormSet):
    def clean(self):
        count = 0
        dates = []
        for form in self.forms:
            try:
                if form.cleaned_data:
                    start_date = form.cleaned_data.get("start_date")
                    end_date = form.cleaned_data.get("end_date")
                    if start_date:
                        dates.append((start_date, end_date))
                        count += 1
            except AttributeError:
                pass
        if count > 1:
            dates.sort(key=lambda date: date[0])
            for i, period in enumerate(dates):
                start_date, end_date = period
                if common.is_cross_date(dates, start_date, i):
                    raise forms.ValidationError(u"契約期間の開始日が重複している。")
                if end_date and common.is_cross_date(dates, end_date, i):
                    raise forms.ValidationError(u"契約期間の終了日が重複している。")
