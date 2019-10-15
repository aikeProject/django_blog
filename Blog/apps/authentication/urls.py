#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@Author  :   成雨
@Contact :   1121352970@qq.com
@Software:   PyCharm
@File    :   urls.py
@Time    :   2019-10-14 20:06
@Desc    :   路由
"""

from django.urls import path

from .views import (
    RegistrationAPIView, LoginAPIView, UserRetrieveUpdateAPIView
)

app_name = 'users'

urlpatterns = [
    # 注册
    path('users', RegistrationAPIView.as_view(), name='register'),
    path('users/login', LoginAPIView.as_view(), name='login'),
    path('user', UserRetrieveUpdateAPIView.as_view(), name='update'),
]
