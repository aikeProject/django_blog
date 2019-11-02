from django.contrib import admin
from .models import Article, Tag, Category, Article2Tag, WebCategory


class MembershipInline(admin.TabularInline):
    model = Article2Tag
    extra = 1


class ArticleAdmin(admin.ModelAdmin):
    fields = ('title', 'author', 'description', 'body', 'category', 'web_category',)
    list_display = (
        'id', 'title', 'author',
        'slug', 'description', 'body',
        'category', 'web_category', 'created_at', 'updated_at',)
    inlines = (MembershipInline,)
    # fieldsets = (
    #     (None, {'fields': ('title', 'author', 'description', 'body', 'category', 'tags',)}),
    # )
    # filter_horizontal = ('tags',)


class TagAdmin(admin.ModelAdmin):
    fields = ('title', 'blog')
    list_display = ('title', 'blog', 'created_at', 'updated_at',)


class CategoryAdmin(admin.ModelAdmin):
    fields = ('title', 'blog',)
    list_display = ('title', 'blog', 'created_at', 'updated_at',)


class WebCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_category', 'created_at', 'updated_at',)
    fields = ('name', 'parent_category',)


admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(WebCategory, WebCategoryAdmin)
