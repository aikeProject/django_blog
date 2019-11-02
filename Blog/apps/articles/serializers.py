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

from .models import Article, Tag, Category, WebCategory

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'uid', 'blog', 'email', 'username', 'image',)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    author = UserDetailSerializer(read_only=True, help_text='作者')
    description = serializers.CharField(required=False, help_text='描述')
    slug = serializers.SlugField(read_only=True, help_text='')
    favorite = serializers.SerializerMethodField()
    favoritesCount = serializers.SerializerMethodField(
        method_name='get_favorites_count'
    )
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)

    # tags = serializers.SerializerMethodField()

    # def get_tags(self, obj):
    #     temp = []
    #     for tag in obj.tags.all():
    #         temp.append({
    #             'id': tag.id,
    #             'title': tag.title
    #         })
    #     return temp

    class Meta:
        model = Article
        fields = '__all__'

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


class WebCategoryChildSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class WebCategorySerializer(serializers.ModelSerializer):
    category_list = WebCategoryChildSerializer(many=True, read_only=True)

    class Meta:
        model = WebCategory
        fields = '__all__'
