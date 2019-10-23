#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@Author  :   成雨
@Contact :   1121352970@qq.com
@Software:   PyCharm
@File    :   urls.py
@Time    :   2019-10-18 16:41
@Desc    :
"""

from django.urls import path

from .views import ArticlesFavoriteAPIView, TagListAPIView

app_name = 'article'

urlpatterns = [
    path('articles/<article_slug>/favorite', ArticlesFavoriteAPIView.as_view()),
    path('tags', TagListAPIView.as_view()),
]
