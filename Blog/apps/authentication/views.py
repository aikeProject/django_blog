from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

# from .renderers import UserJSONRenderer
from .serializers import (UserSerializer, UserUpdateSerializer)

User = get_user_model()


class UserViewSet(CreateModelMixin, UpdateModelMixin, GenericViewSet):
    # 允许所有人注册
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_serializer_class(self):

        if self.action == 'create':
            return UserSerializer

        if self.action == 'update':
            return UserUpdateSerializer

        return UserSerializer

    def get_permissions(self):

        if self.action == 'create':
            return []

        if self.action == 'update':
            return [IsAuthenticated]

        return []

    def update(self, request, *args, **kwargs):
        serializer_data = {
            'username': request.data.get('username', request.user.username),
            'email': request.data.get('email', request.user.email),

            'profile': {
                'bio': request.data.get('bio', request.user.profile.bio),
                'image': request.data.get('image', request.user.profile.image)
            }
        }

        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
