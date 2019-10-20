#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@Author  :   成雨
@Contact :   1121352970@qq.com
@Software:   PyCharm
@File    :   signals.py
@Time    :   2019-10-15 19:17
@Desc    :
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_save, sender=User)
def create_user(sender, instance=None, created=False, **kwargs):
    """
    User创建的时候，创建加密的密码，同时将Profile也创建好
    """
    if instance and created:
        password = instance.password
        instance.set_password(password)
        instance.save()
