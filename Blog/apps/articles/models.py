from django.db import models
from Blog.apps.core.models import TimestampedModel
from django.contrib.auth import get_user_model

User = get_user_model()


class Article(TimestampedModel):
    """文章"""

    slug = models.SlugField(max_length=255, unique=True, help_text='唯一字符串')
    title = models.CharField(max_length=255, help_text='文章标题')
    description = models.TextField(help_text='文章描述')
    body = models.TextField(help_text='文章内容')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles', help_text='文章作者')

    def __str__(self):
        return self.title
