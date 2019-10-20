from django.apps import AppConfig


class ArticlesConfig(AppConfig):
    name = 'Blog.apps.articles'

    def ready(self):
        import Blog.apps.articles.signals
