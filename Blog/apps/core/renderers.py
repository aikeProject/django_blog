#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@Author  :   成雨
@Contact :   1121352970@qq.com
@Software:   PyCharm
@File    :   renderers.py
@Time    :   2019-10-16 19:15
@Desc    :   json序列化
"""

import json

from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnList


class ConduitJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):

        if isinstance(data, ReturnList):
            _data = json.loads(
                super(ConduitJSONRenderer, self).render(data).decode('utf-8')
            )

            return json.dumps(_data)
        else:
            errors = data.get('errors', None)

            if errors is not None:
                return super(ConduitJSONRenderer, self).render(data)

            return json.dumps(data)
