from django.contrib import admin
from .models import Article, Tag


class ArticleAdmin(admin.ModelAdmin):
    fields = ('title', 'author', 'description', 'body',)
    list_display = ('id', 'title', 'author', 'slug', 'description', 'body',)


class TagAdmin(admin.ModelAdmin):
    fields = ('title',)
    list_display = ('nid', 'title',)


admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag, TagAdmin)
