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
from rest_framework.exceptions import ValidationError

from .models import Comment
from ..articles.models import Article
from Blog.apps.authentication.serializers import UserDetailSerializer


class CommentSerializer(serializers.ModelSerializer):
    author = UserDetailSerializer(read_only=True, help_text='创建评论的人')
    article_slug = serializers.CharField(required=True, write_only=True, help_text='标识文章的唯一字符串')
    createdAt = serializers.SerializerMethodField(method_name='get_created_at', help_text='创建时间')
    updatedAt = serializers.SerializerMethodField(method_name='get_updated_at', help_text='更新时间')

    class Meta:
        model = Comment
        fields = (
            'id',
            'body',
            'author',
            'createdAt',
            'updatedAt',
            'article_slug'
        )

    def create(self, validated_data):
        context = self.context
        return Comment.objects.create(author=context.get('author'), article=context.get('article'),
                                      body=validated_data.get('body'))

    def get_created_at(self, instance):
        return instance.created_at.isoformat()

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()
