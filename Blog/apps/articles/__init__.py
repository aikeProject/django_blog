from django.apps import AppConfig


class ArticlesAppConfig(AppConfig):
    name = 'Blog.apps.articles'
    label = 'articles'
    verbose_name = 'Articles'

    def ready(self):
        import Blog.apps.articles.signals


default_app_config = 'Blog.apps.articles.ArticlesAppConfig'
