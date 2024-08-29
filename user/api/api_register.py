import random

from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from user.models import User
from user.serializers.register import RegisterSerializer
from user.sms_utils import send_sms


class RegistrationView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data.get('phone_number')
        password = serializer.validated_data.get('password')
        name = serializer.validated_data.get('name')
        email = serializer.validated_data.get('email')  # Added email field
        existing_user = User.objects.filter(phone_number=phone_number).first()

        if existing_user:
            # Отправить SMS-код подтверждения пользователю
            verification_code = random.randint(100000, 999999)
            sms_text = f'От Bilimzet ваш код верификации: {verification_code}'
            send_sms(phone_number, sms_text)

            # Сохранить код подтверждения в базе данных или кэше для дальнейшей проверки
            existing_user.verification_code = verification_code
            existing_user.save()

            return Response({'detail': 'Verification code sent'}, status=status.HTTP_200_OK)
        else:
            user = self.perform_create(serializer)

            # Сохранение пароля, имени и email
            user.set_password(password)
            user.name = name
            user.email = email
            user.save()

            # Отправить SMS-код подтверждения пользователю
            verification_code = random.randint(100000, 999999)
            sms_text = f'От  Bilimzet ваш код верификации: {verification_code}'
            send_sms(phone_number, sms_text)

            # Сохранить код подтверждения в базе данных или кэше для дальнейшей проверки
            user.verification_code = verification_code
            user.save()

            return Response({'detail': 'Verification code sent'}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        # Создать объект пользователя и вернуть его
        return serializer.save()


