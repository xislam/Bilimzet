import random

from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from user.models import User
from user.serializers.password_reset import RequestPasswordResetSerializer
from user.sms_utils import send_sms


class RequestPasswordResetView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = RequestPasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data.get('phone_number')
        user = User.objects.filter(phone_number=phone_number).first()

        if user:
            # Отправить SMS-код подтверждения пользователю
            verification_code = str(random.randint(100000, 999999))
            sms_text = f'От 8Telecom ваш код верификации: {verification_code}'
            send_sms(phone_number, sms_text)

            # Сохранить код подтверждения в базе данных или кэше для дальнейшей проверки
            user.verification_code = verification_code
            user.save()

            return Response({'detail': 'Verification code sent'}, status=status.HTTP_200_OK)
        else:
            raise NotFound('User with this phone number does not exist')
