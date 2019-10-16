#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@Author  :   成雨
@Contact :   1121352970@qq.com
@Software:   PyCharm
@File    :   urls.py
@Time    :   2019-10-16 19:48
@Desc    :
"""

from .views import ProfileRetrieveAPIView
from django.urls import path

app_name = 'profiles'

urlpatterns = [
    path('profiles/<username>', ProfileRetrieveAPIView.as_view(), name='profile')
]
