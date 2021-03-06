from django.contrib import admin
from .models import User, Blog

admin.site.empty_value_display = '(None)'


class UserAdmin(admin.ModelAdmin):
    # 编辑的字段
    fields = ('email', 'username', 'image', 'password', 'blog')
    # 列表显示的字段
    list_display = ('id', 'uid', 'email', 'username', 'image', 'created_at', 'updated_at')
    # 空值字段
    empty_value_display = '--'
    # 根据你指定的日期相关的字段，为页面创建一个时间导航栏，可通过日期过滤对象
    date_hierarchy = 'created_at'
    # 过滤
    list_filter = ('is_staff',)
    # 搜索
    search_fields = ('username', 'email',)


class BlogAdmin(admin.ModelAdmin):
    fields = ('title', 'site_name', 'theme',)
    list_display = ('title', 'site_name', 'theme', 'created_at', 'updated_at',)


admin.site.register(User, UserAdmin)
admin.site.register(Blog, BlogAdmin)
