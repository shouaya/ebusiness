# coding: UTF-8

from . import models
from django import forms


class EbAttendanceForm(forms.ModelForm):
    class Meta:
        model = models.EbAttendance
        fields = '__all__'

    def clean(self):
        self.add_error('', u"データ変更禁止！")


class EbEmployeeForm(forms.ModelForm):
    class Meta:
        model = models.EbEmployee
        fields = '__all__'

    def clean(self):
        self.add_error('', u"データ変更禁止！")


class SysOrgForm(forms.ModelForm):
    class Meta:
        model = models.SysOrg
        fields = '__all__'

    def clean(self):
        self.add_error('', u"データ変更禁止！")


class SysUserForm(forms.ModelForm):
    class Meta:
        model = models.SysUser
        fields = '__all__'

    def clean(self):
        self.add_error('', u"データ変更禁止！")
