import jwt
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models
from datetime import datetime, timedelta
from django.conf import settings


# Create your models here.

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


class User(AbstractBaseUser, PermissionsMixin):
    """用户"""
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    # 删除用户的标志
    is_active = models.BooleanField(default=True)
    # 管理员
    is_staff = models.BooleanField(default=False)
    # 创建时间
    created_at = models.DateTimeField(auto_now_add=True)
    # 更新时间
    updated_at = models.DateTimeField(auto_now=True)
    # 使用email进行登录
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # 指定用户管理类为UserManager
    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        """
        """
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        生成一个token令牌，过期时间为60天
        """
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username
