from django.apps import AppConfig


class ArticlesConfig(AppConfig):
    name = 'Blog.apps.articles'
    verbose_name = '文章管理'

    def ready(self):
        import Blog.apps.articles.signals
