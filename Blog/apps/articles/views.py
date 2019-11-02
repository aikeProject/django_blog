from rest_framework import status, viewsets
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.settings import api_settings
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from .models import Article, Tag, Category, WebCategory
from .serializers import ArticleSerializer, TagSerializer, CategorySerializer, WebCategorySerializer
from .filters import ArticlesFilter, TagFilter


class ArticleViewSet(CreateModelMixin,
                     ListModelMixin,
                     RetrieveModelMixin,
                     UpdateModelMixin,
                     viewsets.GenericViewSet):
    """
    文章
    """
    lookup_field = 'slug'
    queryset = Article.objects.select_related('author')
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = ArticleSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    filter_backends = (SearchFilter, DjangoFilterBackend,)
    search_fields = ('title',)
    filter_class = ArticlesFilter

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class ArticlesFavoriteAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ArticleSerializer

    def delete(self, request, article_slug=None):
        profile = self.request.user
        serializer_context = {'request': request}

        try:
            article = Article.objects.get(slug=article_slug)
        except Article.DoesNotExist:
            raise NotFound('取消失败')

        profile.un_favorite(article)

        serializer = self.serializer_class(article, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, article_slug=None):
        profile = self.request.user
        serializer_context = {'request': request}

        try:
            article = Article.objects.get(slug=article_slug)
        except Article.DoesNotExist:
            raise NotFound('关注失败')

        profile.favorite(article)

        serializer = self.serializer_class(article, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TagViewSet(ListModelMixin, viewsets.GenericViewSet):
    """
    获取所有标签
    """

    queryset = Tag.objects.all()
    pagination_class = None
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = TagSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = TagFilter


class CategoryViewSet(viewsets.ModelViewSet):
    """
    标签 增、删、改、查
    """
    queryset = Category.objects.all()
    pagination_class = None
    serializer_class = CategorySerializer


class WebCategoryViewSet(ListModelMixin, viewsets.GenericViewSet):
    """
    网站分类
    """
    queryset = WebCategory.objects.all()
    pagination_class = None
    serializer_class = WebCategorySerializer

    def get_queryset(self):
        # 没有父级的分类为顶级分类
        queryset = self.queryset.filter(parent_category=None)
        return queryset
