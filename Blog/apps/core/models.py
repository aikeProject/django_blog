#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@Author  :   成雨
@Contact :   1121352970@qq.com
@Software:   PyCharm
@File    :   models.py
@Time    :   2019-10-15 15:50
@Desc    :   model基类
"""

from django.db import models


class TimestampedModel(models.Model):
    """
    抽象基类
    该模型将不会创建任何数据表。当其用作其它模型类的基类时，它的字段会自动添加至子类
    继承该类的模型都具有创建时间和修改时间
    """

    # 创建时间
    created_at = models.DateTimeField(auto_now_add=True)
    # 更新时间
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

        # 根据创建时间和更新时间倒序排序
        ordering = ['-created_at', '-updated_at']
