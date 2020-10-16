from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserCreateSerializer, UserLoginSerializer
from .models import User

class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()

    renderer_classes = [JSONRenderer]

    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer

    renderer_classes = [JSONRenderer]

    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)