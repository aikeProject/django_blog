import uuid

from django.contrib.auth.models import (BaseUserManager, AbstractUser)
from django.utils.translation import gettext_lazy as _
from django.db import models

from Blog.apps.core.models import TimestampedModel


class UserManager(BaseUserManager):
    """重写用户管理类"""

    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):

        if not username:
            raise ValueError('必须填写用户名')

        if not email:
            raise ValueError('必须填写邮箱')

        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, password=password, **extra_fields)

        # 信号里写过了
        # user.set_password(password)

        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('管理员 is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('管理员 is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser, TimestampedModel):
    """用户"""
    uid = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4, editable=False, help_text='标识用户唯一字符串')
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
    email = models.EmailField(unique=True, blank=True, help_text='邮箱')
    image = models.FileField(unique=False, null=True, blank=False, help_text='头像', upload_to="avatar")
    # symmetrical 取消对称关系
    # 关注
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)
    # 收藏
    favorites = models.ManyToManyField('articles.Article', related_name='favorite_by')
    # 博客
    blog = models.OneToOneField(to='Blog', null=True, on_delete=models.CASCADE)

    # 使用email进行登录
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # 指定用户管理类为UserManager
    objects = UserManager()

    def __str__(self):
        return self.email

    def follow(self, profile):
        """关注"""
        self.follows.add(profile)

    def unfollow(self, profile):
        """取消关注"""
        self.follows.remove(profile)

    def is_following(self, profile):
        """你关注了谁"""
        return self.follows.filter(pk=profile.pk).exists()

    def is_followed_by(self, profile):
        """谁关注了你"""
        return self.followed_by.filter(pk=profile.pk).exists()

    def favorite(self, article):
        self.favorites.add(article)

    def un_favorite(self, article):
        self.favorites.remove(article)

    def has_favorite(self, article):
        return self.favorites.filter(pk=article.pk).exists()


class Blog(TimestampedModel):
    """
    博客信息
    """

    title = models.CharField(verbose_name='个人博客标题', max_length=64)
    site_name = models.CharField(verbose_name='站点名称', max_length=64)
    theme = models.CharField(verbose_name='博客主题', max_length=32)

    def __str__(self):
        return self.title
