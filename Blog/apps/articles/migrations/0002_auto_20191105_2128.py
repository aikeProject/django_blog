# Generated by Django 2.2.6 on 2019-11-05 21:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('articles', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='blog',
            field=models.ForeignKey(help_text='所属博客', on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='authentication.Blog', verbose_name='所属博客'),
        ),
        migrations.AddField(
            model_name='category',
            name='blog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_by', to='authentication.Blog', verbose_name='所属博客'),
        ),
        migrations.AddField(
            model_name='articleupdown',
            name='article',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='articles.Article'),
        ),
        migrations.AddField(
            model_name='articleupdown',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='article2tag',
            name='article',
            field=models.ForeignKey(help_text='文章', on_delete=django.db.models.deletion.CASCADE, to='articles.Article', verbose_name='文章'),
        ),
        migrations.AddField(
            model_name='article2tag',
            name='tag',
            field=models.ForeignKey(help_text='标签', on_delete=django.db.models.deletion.CASCADE, related_name='Article2Tag_tag', to='articles.Tag', verbose_name='标签'),
        ),
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ForeignKey(help_text='文章作者', on_delete=django.db.models.deletion.CASCADE, related_name='articles', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(help_text='个人分类', on_delete=django.db.models.deletion.CASCADE, to='articles.Category', verbose_name='个人分类'),
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(help_text='文章标签', through='articles.Article2Tag', to='articles.Tag', verbose_name='文章标签'),
        ),
        migrations.AddField(
            model_name='article',
            name='web_category',
            field=models.ForeignKey(help_text='网站分类', on_delete=django.db.models.deletion.CASCADE, related_name='article_web_category', to='articles.WebCategory', verbose_name='网站分类'),
        ),
        migrations.AlterUniqueTogether(
            name='articleupdown',
            unique_together={('article', 'user')},
        ),
        migrations.AlterUniqueTogether(
            name='article2tag',
            unique_together={('article', 'tag')},
        ),
    ]
