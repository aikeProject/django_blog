from django.contrib import admin
from .models import Article, Tag, Category


class ArticleAdmin(admin.ModelAdmin):
    fields = ('title', 'author', 'description', 'body', 'category',)
    list_display = (
        'id', 'title', 'author',
        'slug', 'description', 'body',
        'category', 'created_at', 'updated_at',)


class TagAdmin(admin.ModelAdmin):
    fields = ('title', 'blog')
    list_display = ('nid', 'title', 'blog', 'created_at', 'updated_at',)


class CategoryAdmin(admin.ModelAdmin):
    fields = ('title', 'blog',)
    list_display = ('nid', 'title', 'blog', 'created_at', 'updated_at',)


admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
