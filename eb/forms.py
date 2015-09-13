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
                  'degree', 'email', 'post_code', 'address1', 'address2', 'phone', 'member_type',
                  'section', 'company', 'salesperson', 'subcontractor']


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
        fields = ['project', 'member', 'start_date', 'end_date', 'price', 'status']


