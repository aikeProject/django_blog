from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler

from .serializers import (UserSerializer, UserUpdateSerializer, UserDetailSerializer, UserFollowsSerializer)
from ..core.permissions import IsOwnerOrReadOnlyUser

User = get_user_model()


class UserViewSet(CreateModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    create:
        创建新用户
    reade:
        查询登陆用户信息
    """

    # 允许所有人注册
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_serializer_class(self):

        if self.action == 'create':
            return UserSerializer

        if self.action == 'retrieve':
            return UserDetailSerializer

        return UserSerializer

    def get_permissions(self):

        if self.action == 'create':
            return []

        if self.action == 'retrieve':
            return [IsAuthenticated(), IsOwnerOrReadOnlyUser()]

        return []

    def create(self, request, *args, **kwargs):
        """重载create方法"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        res = serializer.data
        # 生成token
        payload = jwt_payload_handler(user)
        res['token'] = jwt_encode_handler(payload)

        headers = self.get_success_headers(serializer.data)
        return Response(res, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def get_object(self):
        """当前用户信息"""
        return self.request.user


class ProfileFollowsViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    """
    用户信息
    create:
        关注
    destroy:
        取消关注
    """
    queryset = User.objects.all()
    serializer_class = UserFollowsSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnlyUser)

    def create(self, request, *args, **kwargs):
        """新增关注"""
        follower = self.request.user

        try:
            followee = User.objects.get(pk=request.data.get('id'))
        except User.DoesNotExist:
            raise NotFound()

        if follower.pk is followee.pk:
            raise ValidationError('不能关注自己')

        follower.follow(followee)

        serializer = self.serializer_class(followee, data=request.data, context={
            'request': request
        })
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        """取消关注"""
        instance = self.get_object()
        self.perform_destroy(instance)
        serializer = self.serializer_class(instance, context={
            'request': request
        })
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        """取消关注"""
        self.request.user.unfollow(instance)


class UserRetrieveViewSet(RetrieveModelMixin, GenericViewSet):
    """
    查询用户信息
    """
    lookup_field = 'uid'
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class UserUploadViewSet(UpdateModelMixin, GenericViewSet):
    lookup_field = 'uid'
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnlyUser,)
