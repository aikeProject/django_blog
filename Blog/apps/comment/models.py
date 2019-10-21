from django.db import models
from django.contrib.auth import get_user_model
from ..core.models import TimestampedModel

# Create your models here.

User = get_user_model()


class Comment(TimestampedModel):
    """
    评论
    """

    body = models.TextField(help_text='文章内容')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', help_text='评论人')
    article = models.ForeignKey('articles.Article', on_delete=models.CASCADE, help_text='评论文章')
