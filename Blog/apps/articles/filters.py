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
from django_filters import rest_framework, UUIDFilter, CharFilter


class ArticlesFilter(rest_framework.FilterSet):
    uid = UUIDFilter(field_name="author__uid")
    tagId = CharFilter(field_name='article2tag__tag__id')

    class Meta:
        model = Article
        fields = ('uid', 'category', 'tagId', 'web_category')


class TagFilter(rest_framework.FilterSet):
    uid = UUIDFilter(field_name="blog__user_blog__uid")

    class Meta:
        model = Tag
        fields = ('uid',)
