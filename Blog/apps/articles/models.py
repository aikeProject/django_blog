from django.db import models
from Blog.apps.core.models import TimestampedModel
from django.contrib.auth import get_user_model

User = get_user_model()


class Article(TimestampedModel):
    """文章"""

    slug = models.SlugField(db_index=True, max_length=255, unique=True, help_text='唯一字符串')
    title = models.CharField(db_index=True, max_length=255, help_text='文章标题')
    description = models.TextField(help_text='文章描述')
    body = models.TextField(help_text='文章内容')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles', help_text='文章作者')
    tags = models.ManyToManyField(
        'articles.Tag', related_name='articles'
    )

    def __str__(self):
        return self.title


class Tag(TimestampedModel):
    """标签"""

    tag = models.CharField(max_length=255)
    slug = models.SlugField(db_index=True, unique=True)

    def __str__(self):
        return self.tag
