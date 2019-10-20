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

from .models import Article
from Blog.apps.authentication.serializers import UserDetailSerializer


class ArticleSerializer(serializers.ModelSerializer):
    author = UserDetailSerializer(read_only=True, help_text='作者')
    description = serializers.CharField(required=False, help_text='描述')
    slug = serializers.SlugField(read_only=True, help_text='')
    createdAt = serializers.SerializerMethodField(method_name='get_created_at', help_text='创建时间')
    updatedAt = serializers.SerializerMethodField(method_name='get_updated_at', help_text='更新时间')

    class Meta:
        model = Article
        fields = (
            'author',
            'body',
            'createdAt',
            'description',
            'slug',
            'title',
            'updatedAt',
        )

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        return Article.objects.create(author=author, **validated_data)

    def get_created_at(self, instance):
        return instance.created_at.isoformat()

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()
