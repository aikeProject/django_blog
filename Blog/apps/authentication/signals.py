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

from Blog.apps.profiles.models import Profile

from .models import User


@receiver(post_save, sender=User)
def create_related_profile(sender, instance, created, *args, **kwargs):
    # 创建user的时候同时创建Profile
    if instance and created:
        instance.profile = Profile.objects.create(user=instance)
