from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    name = 'Blog.apps.authentication'
    label = 'authentication'
    verbose_name = '用户管理'

    def ready(self):
        import Blog.apps.authentication.signals
