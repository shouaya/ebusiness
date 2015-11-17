# coding: UTF-8
"""
Created on 2015/08/26

@author: Yang Wanjun
"""
import re
import models
import datetime

from utils import common
from django import forms

REG_POST_CODE = r"^\d{7}$"
REG_UPPER_CAMEL = r"^([A-Z][a-z]+)+$"


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
        if post_code and not re.match(REG_POST_CODE, post_code):
            self.add_error('post_code', u"正しい郵便番号を入力してください。")
        # ローマ名のチェック
        if first_name_en and not re.match(REG_UPPER_CAMEL, first_name_en):
            self.add_error('first_name_en', u"先頭文字は大文字にしてください（例：Zhang）")
        if last_name_en and not re.match(REG_UPPER_CAMEL, last_name_en):
            self.add_error('last_name_en', u"漢字ごとに先頭文字は大文字にしてください（例：XiaoWang）")


class ProjectMemberForm(forms.ModelForm):
    class Meta:
        model = models.ProjectMember
        fields = '__all__'

    min_hours = forms.DecimalField(max_digits=5, decimal_places=2, initial=160,
                                   widget=forms.TextInput(attrs={'style': 'width: 70px;', 'type': 'number'}),
                                   label=u"基準時間", required=True)
    max_hours = forms.DecimalField(max_digits=5, decimal_places=2, initial=180,
                                   widget=forms.TextInput(attrs={'style': 'width: 70px;', 'type': 'number'}),
                                   label=u"最大時間", required=True)


class MemberAttendanceForm(forms.ModelForm):
    class Meta:
        model = models.MemberAttendance
        fields = '__all__'

    rate = forms.DecimalField(max_digits=5, decimal_places=2, initial=1,
                              widget=forms.TextInput(attrs={'style': 'width: 70px;',
                                                            'type': 'number'}),
                              label=u"率")
    total_hours = forms.DecimalField(max_digits=5, decimal_places=2,
                                     widget=forms.TextInput(
                                         attrs={'onblur': "calc_extra_hours(this)",
                                                'type': 'number',
                                                'style': 'width: 70px;'}),
                                     label=u"合計時間",
                                     required=True)
    plus_per_hour = forms.IntegerField(widget=forms.TextInput(attrs={'onblur': "calc_price_for_plus(this)",
                                                                     'style': 'width: 70px;'}),
                                       label=u"増（円）")
    minus_per_hour = forms.IntegerField(widget=forms.TextInput(attrs={'onblur': "calc_price_for_minus(this)",
                                                                      'style': 'width: 70px;'}),
                                        label=u"減（円）")

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
