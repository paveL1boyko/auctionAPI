from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializer import CustomUserSerializer, LoginSerializer, UserSerializer


class RegistrationAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CustomUserSerializer


class LoginAPIView(RetrieveAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status.HTTP_200_OK)


class UserRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
