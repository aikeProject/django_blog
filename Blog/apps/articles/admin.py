from django.contrib import admin
from .models import Article, Tag, Category, Article2Tag


class MembershipInline(admin.TabularInline):
    model = Article2Tag
    extra = 1


class ArticleAdmin(admin.ModelAdmin):
    fields = ('title', 'author', 'description', 'body', 'category')
    list_display = (
        'id', 'title', 'author',
        'slug', 'description', 'body',
        'category', 'created_at', 'updated_at',)
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


admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
