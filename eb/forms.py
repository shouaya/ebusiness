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
        fields = ['name', 'company']


class MemberForm(forms.ModelForm):
    class Meta:
        model = models.Member
        fields = ['employee_id', 'name', 'email', 'phone', 'section', 'company', 'salesperson']


class SalespersonForm(forms.ModelForm):
    class Meta:
        model = models.Salesperson
        fields = ['employee_id', 'name', 'email', 'phone', 'section', 'company']


class ProjectMemberAdminForm(forms.ModelForm):
    class Meta:
        model = models.ProjectMember
        fields = ['project', 'member', 'start_date', 'end_date', 'price', 'status']


