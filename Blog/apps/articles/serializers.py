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

from .models import Article, Tag
from Blog.apps.authentication.serializers import UserDetailSerializer


class ArticleSerializer(serializers.ModelSerializer):
    author = UserDetailSerializer(read_only=True, help_text='作者')
    description = serializers.CharField(required=False, help_text='描述')
    slug = serializers.SlugField(read_only=True, help_text='')
    favorite = serializers.SerializerMethodField()
    favoritesCount = serializers.SerializerMethodField(
        method_name='get_favorites_count'
    )

    class Meta:
        model = Article
        fields = (
            'author',
            'body',
            'created_at',
            'description',
            'slug',
            'title',
            'updated_at',
            'favorite',
            'favoritesCount',
        )

    def create(self, validated_data):
        request = self.context.get('request', None)
        author = request.user

        tags = validated_data.pop('tags', [])

        article = Article.objects.create(author=author, **validated_data)

        for tag in tags:
            article.tags.add(tag)

        return article

    def get_favorite(self, instance):
        request = self.context.get('request', None)

        if request is None:
            return False

        if not request.user.is_authenticated:
            return False

        return request.user.has_favorite(instance)

    def get_favorites_count(self, instance):
        return instance.favorite_by.count()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
