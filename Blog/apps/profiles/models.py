from django.db import models

from Blog.apps.core.models import TimestampedModel


class Profile(TimestampedModel):
    # 一对一
    user = models.OneToOneField('authentication.User', on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    image = models.URLField(blank=True)

    def __str__(self):
        return self.user.username
