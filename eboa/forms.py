# coding: UTF-8

from . import models
from django import forms


class MemberForm(forms.ModelForm):
    class Meta:
        model = models.SysUser
        fields = '__all__'

    def clean(self):
        self.add_error('', u"データ変更禁止！")
