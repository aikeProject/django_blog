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

from .models import Article, Tag, Category, WebCategory, Article2Tag

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
    id = serializers.CharField(required=False)

    class Meta:
        model = Tag
        fields = ('id', 'title')


class ArticleEditSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    tags = TagSerializer(many=True, required=True, help_text='文章标签，必填')

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('slug',)

    def create(self, validated_data):
        user = self.context.get('request').user
        tags = validated_data.pop('tags')
        article = Article.objects.create(**validated_data)
        for (tag) in tags:
            tag_id = tag.get('id')
            # 选择已有的标签
            if tag_id:
                Article2Tag.objects.create(article=article, tag_id=tag.get('id'))
            else:
                # 创建标签
                tag_title = tag.get('title')
                tag_object = Tag.objects.create(title=tag_title, blog=user.blog)
                Article2Tag.objects.create(article=article, tag=tag_object)
        return article


class ArticleSerializer(serializers.ModelSerializer):
    author = UserDetailSerializer(read_only=True, help_text='文章作者，必填')
    description = serializers.CharField(required=True, help_text='文章描述，必填')
    slug = serializers.SlugField(read_only=True, help_text='文章slug字符串，用于url')
    category = CategorySerializer(required=True, help_text='文章个人分类,必填')
    tags = TagSerializer(many=True, required=True, help_text='文章标签，必填')
    favorite = serializers.SerializerMethodField()
    favoritesCount = serializers.SerializerMethodField(
        method_name='get_favorites_count'
    )

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
    child = WebCategoryChildSerializer(many=True, read_only=True, source='category_list')

    class Meta:
        model = WebCategory
        fields = '__all__'
