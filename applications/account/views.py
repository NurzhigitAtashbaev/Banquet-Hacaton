from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import (RegisterSerializer, UpdateSerializer, ForgotPasswordSerializer,
                          ForgotPasswordComleteSerializer, AccountSerializer)
from rest_framework.response import Response
from .models import CustomUser


# from django.contrib.auth import get_user_model

# # User = get_user_model()

class RegisterView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer


class ActivationView(APIView):
    def get(self, request, activation_code):
        try:
            user = CustomUser.objects.get(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response('Успешно', status=200)
        except CustomUser.DoesNotExist:
            return Response('Link expired', status=400)


class ForgotPasswordAPIView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.send_reset_password_code()
        return Response('вам отправлено письмо для восстановления пароля')


class ForgotPasswordCompleteAPIView(APIView):
    def post(self, request):
        serializer = ForgotPasswordComleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        return Response('пароль успешно изменён')


class CustomUserUpdateAPIView(APIView):

    def put(self, request):
        user = request.user
        serializer = UpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class AccountView(RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
