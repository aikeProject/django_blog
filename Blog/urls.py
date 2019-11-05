"""Blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import DefaultRouter

from Blog.apps.authentication.views import UserViewSet, ProfileFollowsViewSet, UserRetrieveViewSet
from Blog.apps.articles.views import ArticleViewSet, TagViewSet, CategoryViewSet, WebCategoryViewSet
from Blog.apps.comment.views import CommentCreateViewSet, CommentsViewSet

router = DefaultRouter()

router.register('user', UserViewSet, base_name='user')
router.register('profilesFollow', ProfileFollowsViewSet, base_name='profilesFollow')
router.register('userDetail', UserRetrieveViewSet, base_name='userDetail')
router.register('articles', ArticleViewSet, base_name='articles')
router.register('comment', CommentCreateViewSet, base_name='comments')
router.register('comments', CommentsViewSet, base_name='commentsDel')
router.register('tag', TagViewSet, base_name='tags')
router.register('category', CategoryViewSet, base_name='category')
router.register('webCategory', WebCategoryViewSet, base_name='web_category')

urlpatterns = [
    path('admin/', admin.site.urls),
    # web api 认证需要
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include(router.urls)),
    path('api/', include('Blog.apps.articles.urls', namespace='articles')),
    # path('api/', include('Blog.apps.authentication.urls', namespace='authentication')),
    # path('api/', include('Blog.apps.articles.urls', namespace='articles')),
    path('login/', obtain_jwt_token),
    path('docs/', include_docs_urls(title="blog")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
