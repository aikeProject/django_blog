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

from .models import Comment
from django_filters import CharFilter, rest_framework


class CommentFilter(rest_framework.FilterSet):
    article_slug = CharFilter(field_name="article__slug")

    class Meta:
        model = Comment
        fields = ('article_slug',)
