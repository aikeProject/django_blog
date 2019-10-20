from rest_framework import mixins, status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.settings import api_settings

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import Article
from .serializers import ArticleSerializer


class ArticleViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    """

    """
    lookup_field = 'slug'
    queryset = Article.objects.select_related('author', 'author__user')
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = ArticleSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

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

    def retrieve(self, request, slug):
        try:
            serializer_instance = self.queryset.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound('没有此文章')

        serializer = self.serializer_class(serializer_instance)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, slug):
        try:
            serializer_instance = self.queryset.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound('没有此文章，无法修改')

        serializer_data = request.data

        serializer = self.serializer_class(
            serializer_instance, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
