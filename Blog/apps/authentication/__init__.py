from django.apps import AppConfig


class AuthenticationAppConfig(AppConfig):
    name = 'Blog.apps.authentication'
    label = 'authentication'
    verbose_name = 'Authentication'

    def ready(self):
        import Blog.apps.authentication.signals


default_app_config = 'Blog.apps.authentication.AuthenticationAppConfig'
