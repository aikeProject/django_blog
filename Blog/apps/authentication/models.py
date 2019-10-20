from django.contrib.auth.models import (BaseUserManager, AbstractUser)
from django.utils.translation import gettext_lazy as _
from django.db import models

from Blog.apps.core.models import TimestampedModel


class UserManager(BaseUserManager):
    """
    自定义User管理类
    """

    def create_user(self, username, email, password=None):
        """创建用户并返回"""
        if username is None:
            raise TypeError('用户名不能为空')

        if email is None:
            raise TypeError('邮箱不能为空')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        """创建管理员"""
        if password is None:
            raise TypeError('密码不能为空')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractUser, TimestampedModel):
    """用户"""
    username = models.CharField(
        _('username'),
        max_length=255,
        unique=True,
        blank=True,
        help_text=_('请输入用户名'),
        error_messages={
            'unique': _('请输入用户名'),
            'blank': _('请输入用户名')
        },
    )
    email = models.EmailField(unique=True, blank=True)
    bio = models.TextField(blank=True)
    image = models.URLField(blank=True)

    # 使用email进行登录
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # 指定用户管理类为UserManager
    objects = UserManager()

    def __str__(self):
        return self.email
