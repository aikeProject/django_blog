from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler

from .serializers import (UserSerializer, UserUpdateSerializer, UserDetailSerializer)

User = get_user_model()


class UserViewSet(CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    create:
        创建新用户
    update:
        更新用户信息
    partial_update:
        更新用户信息
    """

    # 允许所有人注册
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_serializer_class(self):

        if self.action == 'create':
            return UserSerializer

        if self.action == 'update' or self.action == 'partial_update':
            return UserUpdateSerializer

        if self.action == 'retrieve':
            return UserDetailSerializer

        return UserSerializer

    def get_permissions(self):

        if self.action == 'create':
            return []

        if self.action == 'update' or self.action == 'partial_update' or self.action == 'retrieve':
            return [IsAuthenticated()]

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
