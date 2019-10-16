#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@Author  :   成雨
@Contact :   1121352970@qq.com
@Software:   PyCharm
@File    :   renderers.py
@Time    :   2019-10-14 19:49
@Desc    :   JSON 序列化
"""
from Blog.apps.core.renderers import ConduitJSONRenderer


class UserJSONRenderer(ConduitJSONRenderer):
    charset = 'utf-8'
    object_label = 'user'

    def render(self, data, media_type=None, renderer_context=None):
        # token字节解码
        token = data.get('token', None)

        if token is not None and isinstance(token, bytes):
            data['token'] = token.decode('utf-8')

        return super(UserJSONRenderer, self).render(data)
