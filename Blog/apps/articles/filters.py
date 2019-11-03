#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@Author  :   成雨
@Contact :   1121352970@qq.com
@Software:   PyCharm
@File    :   filters.py
@Time    :   2019-10-20 19:50
@Desc    :   过滤类
"""

from .models import Article, Tag
from django.db.models import Q
from django_filters import rest_framework, UUIDFilter, CharFilter


class ArticlesFilter(rest_framework.FilterSet):
    uid = UUIDFilter(field_name="author__uid", help_text='作者uid')
    tagId = CharFilter(field_name='article2tag__tag__id', help_text='标签id')
    category = CharFilter(field_name='category', help_text='个人文章分类')
    web_category = CharFilter(field_name='web_category', help_text='网站分类，只能查子级分类')
    webCategoryId = CharFilter(method='category_filer', help_text='网站分类，子级和父级分类都能查')

    # 网站分类的父级和子级均可过滤
    def category_filer(self, queryset, name, value):
        return queryset.filter(Q(web_category=value) | Q(web_category__parent_category=value))

    class Meta:
        model = Article
        fields = ()


class TagFilter(rest_framework.FilterSet):
    uid = UUIDFilter(field_name="blog__user_blog__uid")

    class Meta:
        model = Tag
        fields = ('uid',)
