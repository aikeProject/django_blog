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

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet

app_name = 'articles'

router = DefaultRouter(trailing_slash=False)
router.register('articles', ArticleViewSet)

urlpatterns = [
    path('', include(router.urls))
]
