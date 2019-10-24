from django.contrib import admin
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    # 编辑的字段
    fields = ('body', 'article', 'author',)
    # 列表显示的字段
    list_display = ('id', 'body', 'article', 'author',)


admin.site.register(Comment, CommentAdmin)
