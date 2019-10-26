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
from django_filters import CharFilter, rest_framework


class ArticlesFilter(rest_framework.FilterSet):
    title = CharFilter(field_name="title")

    class Meta:
        model = Article
        fields = ('title',)


class TagFilter(rest_framework.FilterSet):
    class Meta:
        model = Tag
        fields = ('blog',)
