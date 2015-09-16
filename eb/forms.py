# coding: UTF-8
"""
Created on 2015/08/26

@author: Yang Wanjun
"""
import re
import models

from django import forms


class CompanyForm(forms.ModelForm):
    class Meta:
        models = models.Company
        fields = ['name', 'japanese_spell', 'found_date', 'capital', 'post_code', 'address1', 'address2', 'tel', 'fax']

    post_code = forms.CharField(max_length=7,
                                widget=forms.TextInput(
                                    attrs={'onKeyUp': "AjaxZip3.zip2addr(this,'','address1','address1');"}),
                                label=u"郵便番号",
                                required=False)

    def clean(self):
        cleaned_data = super(CompanyForm, self).clean()
        post_code = cleaned_data.get("post_code")
        if post_code and not re.match(r"^\d{7}$", post_code):
            self.add_error('post_code', u"正しい郵便番号を入力してください。")


class ClientForm(forms.ModelForm):
    class Meta:
        models = models.Company
        fields = ['name', 'japanese_spell', 'found_date', 'capital', 'post_code', 'address1', 'address2', 'tel', 'fax',
                  'president', 'employee_count', 'sale_amount', 'payment_type', 'payment_day', 'comment', ]

    post_code = forms.CharField(max_length=7,
                                widget=forms.TextInput(
                                    attrs={'onKeyUp': "AjaxZip3.zip2addr(this,'','address1','address1');"}),
                                label=u"郵便番号",
                                required=False)

    def clean(self):
        cleaned_data = super(ClientForm, self).clean()
        post_code = cleaned_data.get("post_code")
        if post_code and not re.match(r"^\d{7}$", post_code):
            self.add_error('post_code', u"正しい郵便番号を入力してください。")


class SectionForm(forms.ModelForm):
    class Meta:
        model = models.Section
        fields = ['name', 'description', 'company']


class MemberForm(forms.ModelForm):
    class Meta:
        model = models.Member
        fields = ['employee_id', 'first_name', 'last_name',
                  'first_name_ja', 'last_name_ja',
                  'first_name_en', 'last_name_en',
                  'birthday', 'graduate_date',
                  'degree', 'email', 'post_code', 'address1', 'address2', 'phone', 'salesperson',
                  'member_type', 'section', 'company', 'subcontractor']

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
        if post_code and not re.match(r"^\d{7}$", post_code):
            self.add_error('post_code', u"正しい郵便番号を入力してください。")
        if member_type == 3:
            # 派遣社員の場合
            if not subcontractor:
                self.add_error('subcontractor', u"派遣社員の場合、協力会社を選択してください。")
        else:
            if not company:
                self.add_error('company', u"派遣社員以外の場合、会社を選択してください。")

        if company and subcontractor:
            self.add_error('company', u"会社と協力会社が同時に選択されてはいけません。")
            self.add_error('subcontractor', u"会社と協力会社が同時に選択されてはいけません。")


class SalespersonForm(forms.ModelForm):
    class Meta:
        model = models.Salesperson
        fields = ['employee_id', 'first_name', 'last_name',
                  'first_name_ja', 'last_name_ja',
                  'first_name_en', 'last_name_en',
                  'birthday', 'graduate_date',
                  'degree', 'email', 'post_code', 'address1', 'address2', 'phone', 'member_type',
                  'section', 'company']

    post_code = forms.CharField(max_length=7,
                                widget=forms.TextInput(
                                    attrs={'onKeyUp': "AjaxZip3.zip2addr(this,'','address1','address1');"}),
                                label=u"郵便番号",
                                required=False)

    def clean(self):
        cleaned_data = super(SalespersonForm, self).clean()
        post_code = cleaned_data.get("post_code")
        if post_code and not re.match(r"^\d{7}$", post_code):
            self.add_error('post_code', u"正しい郵便番号を入力してください。")


class ProjectMemberAdminForm(forms.ModelForm):
    class Meta:
        model = models.ProjectMember
        fields = ['project', 'member', 'start_date', 'end_date', 'price', 'status', 'role']


