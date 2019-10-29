#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@Author  :   成雨
@Contact :   1121352970@qq.com
@Software:   PyCharm
@File    :   auth.py
@Time    :   2019-10-29 18:02
@Desc    :
"""
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.exceptions import ValidationError

User = get_user_model()


class CustomBackend(ModelBackend):
    """
    用户自定义用户验证
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            raise ValidationError('用户名/邮箱错误')
        else:
            raise ValidationError('密码错误')
