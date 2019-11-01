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
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE)
    tags = models.ManyToManyField(
        to="Tag",
        # through参数可以指定用作中介的中间模型
        through='Article2Tag',
    )

    def __str__(self):
        return self.title


class Category(TimestampedModel):
    """
    博主个人文章分类表
    """
    title = models.CharField(verbose_name='分类标题', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客', to='authentication.Blog', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Tag(TimestampedModel):
    title = models.CharField(verbose_name='标签名称', help_text='标签名称', max_length=32)
    blog = models.ForeignKey(related_name='tags', verbose_name='所属博客', help_text='所属博客', to='authentication.Blog',
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Article2Tag(TimestampedModel):
    article = models.ForeignKey(verbose_name='文章', help_text='文章', to="Article", on_delete=models.CASCADE)
    tag = models.ForeignKey(verbose_name='标签', related_name='Article2Tag_tag', help_text='标签', to="Tag", on_delete=models.CASCADE)

    class Meta:
        # 组合唯一约束
        unique_together = [
            ('article', 'tag'),
        ]

    def __str__(self):
        v = self.article.title + "-" + self.tag.title
        return v


class ArticleUpDown(TimestampedModel):
    """
    点赞表
    """

    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    article = models.ForeignKey("Article", null=True, on_delete=models.CASCADE)
    is_up = models.BooleanField(default=True)

    class Meta:
        # 组合唯一约束
        unique_together = [
            ('article', 'user'),
        ]
