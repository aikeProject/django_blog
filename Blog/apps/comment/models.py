from django.db import models
from django.contrib.auth import get_user_model
from ..core.models import TimestampedModel

# Create your models here.

User = get_user_model()


class Comment(TimestampedModel):
    """
    评论
    """

    body = models.TextField(max_length=1000, help_text='评论内容', verbose_name='评论内容')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='评论人',
        help_text='评论人')
    article = models.ForeignKey(
        'articles.Article',
        related_name='comments_article',
        on_delete=models.CASCADE,
        help_text='评论文章',
        verbose_name='评论文章')
    parent = models.ForeignKey(
        'self',
        related_name='comment_parent',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name='父级评论',
        help_text='父级评论'
    )
