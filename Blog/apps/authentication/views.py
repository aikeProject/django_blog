from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .renderers import UserJSONRenderer
from .serializers import (RegistrationSerializer, LoginSerializer, UserSerializer)


class RegistrationAPIView(APIView):
    # 允许所有人注册
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = {
            'username': request.data.get('username', ''),
            'email': request.data.get('email', ''),
            'password': request.data.get('password', '')
        }

        # 创建序列化
        serializer = self.serializer_class(data=user)
        # 验证
        serializer.is_valid(raise_exception=True)
        # 保存
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    # 允许所有人注册
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = {
            'email': request.data.get('email', ''),
            'password': request.data.get('password', '')
        }

        # 创建序列化
        serializer = self.serializer_class(data=user)
        # 验证
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    """查询用户信息 修改用户信息"""

    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

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
