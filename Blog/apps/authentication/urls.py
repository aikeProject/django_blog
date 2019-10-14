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

from django.conf.urls import url

from .views import (
    RegistrationAPIView
)

app_name = 'users'

urlpatterns = [
    # 注册
    url(r'^users/?$', RegistrationAPIView.as_view(), name='register')
]