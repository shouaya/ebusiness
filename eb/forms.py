# coding: UTF-8
"""
Created on 2015/08/26

@author: Yang Wanjun
"""
import models

from django import forms


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

    def clean(self):
        cleaned_data = super(MemberForm, self).clean()
        member_type = cleaned_data.get("member_type")
        company = cleaned_data.get("company")
        section = cleaned_data.get("section")
        subcontractor = cleaned_data.get("subcontractor")
        if member_type == 3:
            # 派遣社員の場合
            if not subcontractor:
                self.add_error('subcontractor', u"派遣社員の場合、協力会社を選択してください。")
        else:
            if not company:
                self.add_error('company', u"派遣社員以外の場合、会社を選択してください。")
            if not section:
                self.add_error('section', u"派遣社員以外の場合、部署を選択してください。")

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


class ProjectMemberAdminForm(forms.ModelForm):
    class Meta:
        model = models.ProjectMember
        fields = ['project', 'member', 'start_date', 'end_date', 'price', 'status', 'role']


