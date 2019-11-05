#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@Author  :   成雨
@Contact :   1121352970@qq.com
@Software:   PyCharm
@File    :   serializers.py
@Time    :   2019-10-18 16:12
@Desc    :
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Comment

User = get_user_model()


class CommentChildSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentCreatSerializer(serializers.ModelSerializer):
    body = serializers.CharField(
        min_length=5,
        max_length=1000,
        trim_whitespace=True,
        help_text='评论内容',
        error_messages={
            'required': '评论内容必填',
            'blank': '评论内容必填',
            'min_length': '评论最少5个字',
            'max_length': '评论最多1000个字',
        }
    )
    article = serializers.SlugField(
        help_text='文章的slug字符串，用于查询该文章',
        error_messages={
            'required': '文章必填',
            'blank': '文章必填',
        }
    )
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    reply = serializers.CharField(
        write_only=True,
        required=False,
        help_text='回复评论人的uid'
    )

    def create(self, validated_data):
        context = self.context
        validated_data.pop('article')

        if context.get('reply'):
            validated_data.pop('author')
            validated_data.pop('reply')
            validated_data['author'] = context.get('reply')

        return Comment.objects.create(
            article=context.get('article'),
            **validated_data
        )

    class Meta:
        model = Comment
        fields = '__all__'


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uid', 'username', 'image',)


class CommentsChildSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentsDetailSerializer(serializers.ModelSerializer):
    author = UserDetailSerializer(read_only=True)
    child = CommentsChildSerializer(many=True, read_only=True, source='comment_parent')
    is_own = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'

    def get_is_own(self, data):
        user = self.context['request'].user

        if not user:
            return False

        if not user.is_authenticated:
            return False

        return user == data.author
