#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@Author  :   成雨
@Contact :   1121352970@qq.com
@Software:   PyCharm
@File    :   serializers.py
@Time    :   2019-10-14 19:48
@Desc    :
"""

from rest_framework import serializers
from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """注册序列化"""

    username = serializers.CharField(
        error_messages={
            'required': '请输入用户名'
        }
    )

    email = serializers.CharField(
        error_messages={
            'required': '请输入邮箱'
        }
    )

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        error_messages={
            'required': '请输入密码',
            'min_length': '密码必须大于8个字符'
        }
    )

    # token只读，注册时候无token
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        # 需要序列化的字段
        fields = ['email', 'username', 'password', 'token']

    def create(self, validated_data):
        """创建一个新用户"""
        return User.objects.create_user(**validated_data)
