#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@Author  :   成雨
@Contact :   1121352970@qq.com
@Software:   PyCharm
@File    :   permissions.py
@Time    :   2019-10-21 18:06
@Desc    :
"""

from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """
    验证是不是当前用户
    """

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
