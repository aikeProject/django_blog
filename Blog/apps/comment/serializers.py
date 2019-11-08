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
import timeago, datetime

User = get_user_model()


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

    def create(self, validated_data):
        context = self.context
        validated_data.pop('article')

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
    old_time = serializers.SerializerMethodField()
    is_delete = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'

    def get_is_delete(self, data):
        """
        判断是否是可删除
        """
        user = self.context['request'].user

        if not user:
            return False

        if not user.is_authenticated:
            return False

        return user == data.author

    def get_old_time(self, data):
        """
        时间差
        :param data: updated_at created_at
        :return: 刚刚，急几秒前，几分钟前，几小时前....
        """
        return timeago.format(data.updated_at, datetime.datetime.now(), 'zh_CN')


class CommentDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
