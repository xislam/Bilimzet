import random

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from user.models import User
from user.serializers.login import CustomTokenObtainPairSerializer
from user.sms_utils import send_sms


class LoginOrRegisterView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer

    @swagger_auto_schema(request_body=CustomTokenObtainPairSerializer)
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')
        name = request.data.get('name', '')  # Получаем имя из запроса, если оно передано

        # Проверка наличия пользователя с данным номером телефона
        try:
            User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            # Регистрация нового пользователя
            user = User.objects.create_user(
                phone_number=phone_number,
                password=password,
                name=name,  # Передаем имя при создании пользователя
            )
            # Отправка кода подтверждения
            verification_code = random.randint(100000, 999999)
            sms_text = f'От Bilimzet ваш код верификации: {verification_code}'
            send_sms(user.phone_number, sms_text)

            # Сохранение кода подтверждения в базе данных
            user.verification_code = verification_code
            user.save()

            return Response({'detail': 'User registered. Verification code sent'}, status=status.HTTP_201_CREATED)

        # Если пользователь найден, проверяем его данные
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        if user.phone_number_verified:
            # Если номер телефона подтвержден, генерируем токены и возвращаем их
            refresh = RefreshToken.for_user(user)
            tokens = {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
            return Response(tokens, status=status.HTTP_200_OK)
        else:
            # Если номер телефона не подтвержден, отправляем код подтверждения
            verification_code = random.randint(100000, 999999)
            sms_text = f'От Bilimzet ваш код верификации: {verification_code}'
            send_sms(user.phone_number, sms_text)

            # Сохранение кода подтверждения в базе данных
            user.verification_code = verification_code
            user.save()

            return Response({'detail': 'Phone number not verified. Verification code sent'},
                            status=status.HTTP_400_BAD_REQUEST)
