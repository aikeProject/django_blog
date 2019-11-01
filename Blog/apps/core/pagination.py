#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@Author  :   成雨
@Contact :   1121352970@qq.com
@Software:   PyCharm
@File    :   pagination.py
@Time    :   2019-11-01 11:11
@Desc    :   分页默认配置
"""
from rest_framework.pagination import PageNumberPagination


class BasePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000
