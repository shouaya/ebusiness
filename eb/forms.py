# coding: UTF-8
"""
Created on 2015/08/26

@author: Yang Wanjun
"""
import re
import models

from django import forms
from django.forms.utils import flatatt
from django.utils.html import format_html, mark_safe
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

REG_POST_CODE = r"^\d{7}$"
REG_UPPER_CAMEL = r"^([A-Z][a-z]+)+$"


class SearchSelect(forms.Select):
    def __init__(self, clsModel, attrs=None, choices=()):
        self.clsModel = clsModel
        super(SearchSelect, self).__init__(attrs, choices)

    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        output = ['<div class="related-widget-wrapper">']
        output.extend([format_html('<select{}>', flatatt(final_attrs))])
        options = self.render_options(choices, [value])
        if options:
            output.append(options)
        output.append('</select>')

        from django.contrib import admin
        related_url = reverse(
            'admin:%s_%s_changelist' % (
                self.clsModel._meta.app_label,
                self.clsModel._meta.model_name,
            ),
            current_app=admin.site.name,
        )
        output.append('<a href="%s%s"'
                      ' class="related-lookup"'
                      ' id="lookup_id_%s" title="%s"></a>' %
                      (related_url, '', name, _('Lookup')))
        output.append('</div>')
        return mark_safe('\n'.join(output))


class CompanyForm(forms.ModelForm):
    class Meta:
        models = models.Company
        fields = '__all__'

    post_code = forms.CharField(max_length=7,
                                widget=forms.TextInput(
                                    attrs={'onKeyUp': "AjaxZip3.zip2addr(this,'','address1','address1');"}),
                                label=u"郵便番号",
                                required=False)

    def clean(self):
        cleaned_data = super(CompanyForm, self).clean()
        post_code = cleaned_data.get("post_code")
        if post_code and not re.match(REG_POST_CODE, post_code):
            self.add_error('post_code', u"正しい郵便番号を入力してください。")


class ClientForm(forms.ModelForm):
    class Meta:
        models = models.Company
        fields = '__all__'

    post_code = forms.CharField(max_length=7,
                                widget=forms.TextInput(
                                    attrs={'onKeyUp': "AjaxZip3.zip2addr(this,'','address1','address1');"}),
                                label=u"郵便番号",
                                required=False)

    def clean(self):
        cleaned_data = super(ClientForm, self).clean()
        post_code = cleaned_data.get("post_code")
        if post_code and not re.match(REG_POST_CODE, post_code):
            self.add_error('post_code', u"正しい郵便番号を入力してください。")


class SubcontractorForm(forms.ModelForm):
    class Meta:
        models = models.Subcontractor
        fields = '__all__'

    post_code = forms.CharField(max_length=7,
                                widget=forms.TextInput(
                                    attrs={'onKeyUp': "AjaxZip3.zip2addr(this,'','address1','address1');"}),
                                label=u"郵便番号",
                                required=False)

    def clean(self):
        cleaned_data = super(SubcontractorForm, self).clean()
        post_code = cleaned_data.get("post_code")
        if post_code and not re.match(REG_POST_CODE, post_code):
            self.add_error('post_code', u"正しい郵便番号を入力してください。")


class SectionForm(forms.ModelForm):
    class Meta:
        model = models.Section
        fields = '__all__'


class ProjectForm(forms.ModelForm):
    class Meta:
        models = models.Project
        fields = '__all__'

    def clean(self):
        cleaned_data = super(ProjectForm, self).clean()
        is_lump= cleaned_data.get("is_lump")
        lump_amount = cleaned_data.get("lump_amount")
        if is_lump:
            if not lump_amount or lump_amount <= 0:
                self.add_error('lump_amount', u"一括の場合、一括金額を入力してください。")


class MemberForm(forms.ModelForm):
    class Meta:
        model = models.Member
        fields = '__all__'

    post_code = forms.CharField(max_length=7,
                                widget=forms.TextInput(
                                    attrs={'onKeyUp': "AjaxZip3.zip2addr(this,'','address1','address1');"}),
                                label=u"郵便番号",
                                required=False)

    def clean(self):
        cleaned_data = super(MemberForm, self).clean()
        member_type = cleaned_data.get("member_type")
        company = cleaned_data.get("company")
        subcontractor = cleaned_data.get("subcontractor")
        post_code = cleaned_data.get("post_code")
        first_name_en = cleaned_data.get("first_name_en")
        last_name_en = cleaned_data.get("last_name_en")
        email = cleaned_data.get("email")
        private_email = cleaned_data.get("private_email")
        is_notify = cleaned_data.get("is_notify")
        notify_type = cleaned_data.get("notify_type")

        if post_code and not re.match(REG_POST_CODE, post_code):
            self.add_error('post_code', u"正しい郵便番号を入力してください。")
        if member_type == 4:
            # 派遣社員の場合
            if not subcontractor:
                self.add_error('subcontractor', u"派遣社員の場合、協力会社を選択してください。")
        else:
            if not company:
                self.add_error('company', u"派遣社員以外の場合、会社を選択してください。")

        # ローマ名のチェック
        if first_name_en and not re.match(REG_UPPER_CAMEL, first_name_en):
            self.add_error('first_name_en', u"先頭文字は大文字にしてください（例：Zhang）")
        if last_name_en and not re.match(REG_UPPER_CAMEL, last_name_en):
            self.add_error('last_name_en', u"漢字ごとに先頭文字は大文字にしてください（例：XiaoWang）")

        if company and subcontractor:
            self.add_error('company', u"会社と協力会社が同時に選択されてはいけません。")
            self.add_error('subcontractor', u"会社と協力会社が同時に選択されてはいけません。")

        if is_notify:
            if not notify_type:
                self.add_error('notify_type', u"通知種類を選択してください。")
            if notify_type == 1 and not email:
                self.add_error('notify_type', u"メールアドレスを追加してください。")
            elif notify_type == 2 and not private_email:
                self.add_error('notify_type', u"個人メールアドレスを追加してください。")
            elif notify_type == 3 and (not email or not private_email):
                self.add_error('notify_type', u"メールアドレス及び個人メールアドレスを追加してください。")
        else:
            if notify_type:
                self.add_error('notify_type', u"メール通知を選択してない場合、通知種類を選択しないようにしてください。")


class SalespersonForm(forms.ModelForm):
    class Meta:
        model = models.Salesperson
        fields = '__all__'

    post_code = forms.CharField(max_length=7,
                                widget=forms.TextInput(
                                    attrs={'onKeyUp': "AjaxZip3.zip2addr(this,'','address1','address1');"}),
                                label=u"郵便番号",
                                required=False)

    def clean(self):
        cleaned_data = super(SalespersonForm, self).clean()
        post_code = cleaned_data.get("post_code")
        first_name_en = cleaned_data.get("first_name_en")
        last_name_en = cleaned_data.get("last_name_en")
        email = cleaned_data.get("email")
        private_email = cleaned_data.get("private_email")
        is_notify = cleaned_data.get("is_notify")
        notify_type = cleaned_data.get("notify_type")
        if post_code and not re.match(REG_POST_CODE, post_code):
            self.add_error('post_code', u"正しい郵便番号を入力してください。")
        # ローマ名のチェック
        if first_name_en and not re.match(REG_UPPER_CAMEL, first_name_en):
            self.add_error('first_name_en', u"先頭文字は大文字にしてください（例：Zhang）")
        if last_name_en and not re.match(REG_UPPER_CAMEL, last_name_en):
            self.add_error('last_name_en', u"漢字ごとに先頭文字は大文字にしてください（例：XiaoWang）")
        if is_notify:
            if not notify_type:
                self.add_error('notify_type', u"通知種類を選択してください。")
            if notify_type == 1 and not email:
                self.add_error('notify_type', u"メールアドレスを追加してください。")
            elif notify_type == 2 and not private_email:
                self.add_error('notify_type', u"個人メールアドレスを追加してください。")
            elif notify_type == 3 and (not email or not private_email):
                self.add_error('notify_type', u"メールアドレス及び個人メールアドレスを追加してください。")
        else:
            if notify_type:
                self.add_error('notify_type', u"メール通知を選択してない場合、通知種類を選択しないようにしてください。")


class ProjectMemberForm(forms.ModelForm):
    class Meta:
        model = models.ProjectMember
        fields = '__all__'

    member = forms.ModelChoiceField(queryset=models.Member.objects.all(),
                                    widget=SearchSelect(models.Member),
                                    label=u"名前")
    price = forms.IntegerField(initial=0,
                               widget=forms.TextInput(attrs={'style': 'width: 70px;',
                                                             'type': 'number',
                                                             'onblur': "calc_plus_minus(this)"}),
                               label=u"単価")
    min_hours = forms.DecimalField(max_digits=5, decimal_places=2, initial=160,
                                   widget=forms.TextInput(attrs={'style': 'width: 60px;',
                                                                 'type': 'number',
                                                                 'onblur': 'calc_minus_from_min_hour(this)'}),
                                   label=u"基準時間", required=True)
    max_hours = forms.DecimalField(max_digits=5, decimal_places=2, initial=180,
                                   widget=forms.TextInput(attrs={'style': 'width: 60px;',
                                                                 'type': 'number',
                                                                 'onblur': 'calc_plus_from_max_hour(this)'}),
                                   label=u"最大時間", required=True)
    plus_per_hour = forms.IntegerField(widget=forms.TextInput(attrs={'style': 'width: 60px;',
                                                                     'type': 'number'}),
                                       label=u"増（円）")
    minus_per_hour = forms.IntegerField(widget=forms.TextInput(attrs={'style': 'width: 60px;',
                                                                      'type': 'number'}),
                                        label=u"減（円）")


class MemberAttendanceForm(forms.ModelForm):
    class Meta:
        model = models.MemberAttendance
        fields = '__all__'

    rate = forms.DecimalField(max_digits=5, decimal_places=2, initial=1,
                              widget=forms.TextInput(attrs={'style': 'width: 70px;',
                                                            'type': 'number',
                                                            'step': 0.1}),
                              label=u"率")
    total_hours = forms.DecimalField(max_digits=5, decimal_places=2,
                                     widget=forms.TextInput(
                                         attrs={'onblur': "calc_extra_hours(this)",
                                                'type': 'number',
                                                'style': 'width: 70px;',
                                                'step': 0.25}),
                                     label=u"合計時間",
                                     required=True)
    extra_hours = forms.DecimalField(max_digits=5, decimal_places=2, initial=0,
                                     widget=forms.TextInput(
                                         attrs={'type': 'number',
                                                'style': 'width: 70px;',
                                                'step': 0.25}),
                                     label=u"残業時間",
                                     required=True)
    # plus_per_hour = forms.IntegerField(widget=forms.TextInput(attrs={'onblur': "calc_price_for_plus(this)",
    #                                                                  'style': 'width: 60px;',
    #                                                                  'type': 'number'}),
    #                                    label=u"増（円）")
    # minus_per_hour = forms.IntegerField(widget=forms.TextInput(attrs={'onblur': "calc_price_for_minus(this)",
    #                                                                   'style': 'width: 60px;',
    #                                                                   'type': 'number'}),
    #                                     label=u"減（円）")
    price = forms.IntegerField(initial=0,
                               widget=forms.TextInput(attrs={'style': 'width: 80px;',
                                                             'type': 'number'}),
                               label=u"価格")

    def clean(self):
        cleaned_data = super(MemberAttendanceForm, self).clean()
        project_member = cleaned_data.get("project_member")
        year = cleaned_data.get("year")
        month = cleaned_data.get("month")
        if not month:
            self.add_error('month', u"入力してください！")
        else:
            if project_member.start_date:
                if str(project_member.start_date.year) + "%02d" % (project_member.start_date.month,) > year + month:
                    self.add_error('year', u"対象年月は案件開始日以前になっています！")
                    self.add_error('month', u"対象年月は案件開始日以前になっています！")
            if project_member.end_date:
                if str(project_member.end_date.year) + "%02d" % (project_member.end_date.month,) < year + month:
                    self.add_error('year', u"対象年月は案件終了日以降になっています！")
                    self.add_error('month', u"対象年月は案件終了日以降になっています！")


class UploadFileForm(forms.Form):
    file = forms.FileField()


class MemberAttendanceFormSet(forms.ModelForm):
    class Meta:
        model = models.MemberAttendance
        fields = '__all__'

    basic_price = forms.CharField(widget=forms.TextInput(attrs={'style': 'width: 45px; border: 0px;'
                                                                         'background-color: transparent;',
                                                                'readonly': 'readonly'}),
                                  required=False, label=u"単価")
    max_hours = forms.CharField(widget=forms.TextInput(attrs={'style': 'width: 40px; border: 0px;'
                                                                       'background-color: transparent;',
                                                              'readonly': 'readonly'}),
                                required=False, label=u"最大")
    min_hours = forms.CharField(widget=forms.TextInput(attrs={'style': 'width: 40px; border: 0px;'
                                                                       'background-color: transparent;',
                                                              'readonly': 'readonly'}),
                                required=False, label=u"最小")
    rate = forms.DecimalField(max_digits=5, decimal_places=2, initial=1,
                              widget=forms.TextInput(attrs={'style': 'width: 40px;',
                                                            'type': 'number',
                                                            'step': 0.1}),
                              label=u"率")
    total_hours = forms.DecimalField(max_digits=5, decimal_places=2,
                                     widget=forms.TextInput(
                                         attrs={'onblur': "calc_extra_hours_portal(this)",
                                                'type': 'number',
                                                'style': 'width: 60px;',
                                                'step': 0.25}),
                                     label=u"合計時間",
                                     required=True)
    extra_hours = forms.DecimalField(max_digits=5, decimal_places=2, initial=0,
                                     widget=forms.TextInput(
                                         attrs={'type': 'number',
                                                'style': 'width: 50px;',
                                                'step': 0.25}),
                                     label=u"残業時間",
                                     required=True)
    plus_per_hour = forms.IntegerField(widget=forms.TextInput(attrs={'onblur': "calc_price_for_plus_portal(this)",
                                                                     'style': 'width: 42px; '
                                                                              'background-color: transparent;'
                                                                              'border: 0px;',
                                                                     'readonly': 'readonly'}),
                                       label=u"増（円）")
    minus_per_hour = forms.IntegerField(widget=forms.TextInput(attrs={'onblur': "calc_price_for_minus_portal(this)",
                                                                      'style': 'width: 42px;'
                                                                               'background-color: transparent;'
                                                                               'border: 0px;',
                                                                      'readonly': 'readonly'}),
                                        label=u"減（円）")
    price = forms.IntegerField(initial=0,
                               widget=forms.TextInput(attrs={'style': 'width: 70px;',
                                                             'type': 'number'}),
                               label=u"価格")


class BpMemberOrderInfoFormSet(forms.ModelForm):
    class Meta:
        model = models.BpMemberOrderInfo
        fields = '__all__'

    min_hours = forms.DecimalField(max_digits=5, decimal_places=2, initial=160,
                                   widget=forms.TextInput(attrs={'style': 'width: 60px;',
                                                                 'type': 'number'}),
                                   label=u"基準時間", required=True)
    max_hours = forms.DecimalField(max_digits=5, decimal_places=2, initial=180,
                                   widget=forms.TextInput(attrs={'style': 'width: 60px;',
                                                                 'type': 'number'}),
                                   label=u"最大時間", required=True)
    plus_per_hour = forms.IntegerField(widget=forms.TextInput(attrs={'style': 'width: 60px;',
                                                                     'type': 'number'}),
                                       label=u"増（円）")
    minus_per_hour = forms.IntegerField(widget=forms.TextInput(attrs={'style': 'width: 60px;',
                                                                      'type': 'number'}),
                                        label=u"減（円）")
    cost = forms.IntegerField(initial=0,
                              widget=forms.TextInput(attrs={'style': 'width: 70px;'
                                                                     'background-color: transparent;'
                                                                     'border: 0px;',
                                                            'readonly': 'readonly'}),
                              label=u"コスト")
