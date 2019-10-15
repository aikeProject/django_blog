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
from django.contrib.auth import authenticate
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


class LoginSerializer(serializers.Serializer):
    """登录序列化"""

    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, attrs):

        email = attrs.get('email', '')
        password = attrs.get('password', '')

        if email is None:
            raise serializers.ValidationError('请输入邮箱')

        if password is None:
            raise serializers.ValidationError('请输入密码')

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError('用户名密码错误')

        if not user.is_active:
            raise serializers.ValidationError('此用户不存在')

        return {
            'username': user.username,
            'email': user.email,
            'token': user.token
        }


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        allow_blank=True,
        error_messages={
            'required': '请输入密码'
        }
    )

    # allow_blank 将空值设置为有效值
    username = serializers.CharField(allow_blank=True)

    email = serializers.CharField(allow_blank=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'token',)

        read_only_fields = ('token',)

    def update(self, instance, validated_data):

        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value) if value else None

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance
