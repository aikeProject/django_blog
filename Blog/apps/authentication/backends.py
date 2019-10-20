#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@Author  :   成雨
@Contact :   1121352970@qq.com
@Software:   PyCharm
@File    :   backends.py
@Time    :   2019-10-14 19:32
@Desc    :   JWTAuthentication JWT 认证
"""
#
# import jwt
#
# from django.conf import settings
#
# from rest_framework import authentication, exceptions
#
# from .models import User
#
#
# class JWTAuthentication(authentication.BaseAuthentication):
#     authentication_header_prefix = 'Token'
#
#     def authenticate(self, request):
#         """
#         每次请求都会执行该认证
#         1）返回 Npne 认证失败
#         2）返回 (user, token) 认证成功
#         """
#         request.user = None
#
#         # 获取请求头中的Token，分割为数组 ['Token', '后端生成给前端的token值']
#         auth_header = authentication.get_authorization_header(request).split()
#         auth_header_prefix = self.authentication_header_prefix.lower()
#
#         if not auth_header:
#             return None
#
#         if len(auth_header) == 1:
#             return None
#
#         elif len(auth_header) > 2:
#             return None
#
#         # 将字节转换为utf8
#         prefix = auth_header[0].decode('utf-8')
#         token = auth_header[1].decode('utf-8')
#
#         # != 'token'
#         if prefix.lower() != auth_header_prefix:
#             return None
#
#         return self._authenticate_credentials(request, token)
#
#     def _authenticate_credentials(self, request, token):
#         """
#         解析加密的Token
#         """
#         try:
#             payload = jwt.decode(token, settings.SECRET_KEY)
#         except Exception:
#             msg = 'token错误'
#             raise exceptions.AuthenticationFailed(msg)
#
#         try:
#             user = User.objects.get(pk=payload['id'])
#         except User.DoesNotExist:
#             msg = '无此用户'
#             raise exceptions.AuthenticationFailed(msg)
#
#         if not user.is_active:
#             msg = '无此用户'
#             raise exceptions.AuthenticationFailed(msg)
#
#         # 成功返回当前用户和token
#         return (
#             user,
#             token
#         )
