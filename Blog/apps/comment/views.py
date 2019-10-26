from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.settings import api_settings
from rest_framework.response import Response
from .models import Comment
from ..articles.models import Article
from .serializers import CommentSerializer
from .filters import CommentFilter
from ..core.permissions import IsOwnerOrReadOnly


class CommentViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    lookup_field = 'article__slug'
    lookup_url_kwarg = 'article_slug'
    queryset = Comment.objects.select_related('article', 'author')
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    serializer_class = CommentSerializer
    filter_class = CommentFilter

    def create(self, request, *args, **kwargs):
        serializer_class = self.serializer_class
        data = request.data
        article_slug = data.get('article_slug')

        context = {
            'author': self.request.user
        }

        try:
            context['article'] = Article.objects.get(slug=article_slug)
        except Article.DoesNotExist:
            raise NotFound('参数错误')

        serializer = serializer_class(data=request.data, context=context)
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


class CommentDelViewSet(DestroyModelMixin, GenericViewSet):
    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = CommentSerializer
