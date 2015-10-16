# coding: UTF-8
"""
Created on 2015/10/16

@author: Yang Wanjun
"""

from django.contrib.auth.models import User, check_password
from django.contrib.auth.backends import ModelBackend


class MyBackend(ModelBackend):

    def has_perm(self, user_obj, perm, obj=None):
        if not isinstance(obj, User):
            return False

        return True

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
