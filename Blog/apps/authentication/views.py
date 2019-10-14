from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .renderers import UserJSONRenderer
from .serializers import (
    RegistrationSerializer
)


class RegistrationAPIView(APIView):
    # 允许所有人注册
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # 创建序列化
        serializer = self.serializer_class(data=user)
        # 验证
        serializer.is_valid(raise_exception=True)
        # 保存
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
