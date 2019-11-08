from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.settings import api_settings
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Comment
from ..articles.models import Article
from .serializers import CommentCreatSerializer, CommentsDetailSerializer
from .filters import CommentFilter
from ..core.permissions import IsOwnerOrReadOnly

User = get_user_model()


class CommentCreateViewSet(CreateModelMixin, GenericViewSet):
    queryset = Comment.objects.select_related('article', 'author')
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = CommentCreatSerializer

    def create(self, request, *args, **kwargs):
        serializer_class = self.serializer_class
        data = request.data
        article_slug = data.get('article')
        context = {
            'request': request
        }

        try:
            context['article'] = Article.objects.get(slug=article_slug)
        except Article.DoesNotExist:
            raise NotFound('参数错误,该文章不存在')

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


class CommentsViewSet(ListModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = CommentsDetailSerializer
    filter_class = CommentFilter

    def get_permissions(self):
        if self.action == 'destroy':
            return [IsAuthenticated(), IsOwnerOrReadOnly()]

        return [IsAuthenticatedOrReadOnly()]

    def get_queryset(self):
        # 过滤出顶级评论
        return self.queryset.filter(parent=None)
