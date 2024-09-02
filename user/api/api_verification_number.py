from random import randint

from rest_framework import status, generics
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import User, VerificationCode
from user.serializers.verification_number import PhoneNumberVerificationSerializer, PhoneNumberCheckSerializer, \
    RequestVerificationCodeSerializer, TokenObtainSerializer, PasswordUpdateSerializer
from user.sms_utils import send_sms


def is_valid_verification_code(user, sms_code):
    if user is None:
        return False

    # Предполагается, что код подтверждения хранится в поле verification_code модели User
    return user.verification_code == sms_code


class PhoneNumberVerificationView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = PhoneNumberVerificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']
        sms_code = serializer.validated_data['sms_code']

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if sms_code:
            # Если предоставлен код подтверждения
            if not is_valid_verification_code(user, sms_code):
                return Response({'detail': 'Invalid verification code'}, status=status.HTTP_400_BAD_REQUEST)

            # Если код подтверждения верный, верифицируйте номер телефона
            user.phone_number_verified = True
            user.save()

            # Генерация и отправка токенов после успешной верификации
            refresh = RefreshToken.for_user(user)
            tokens = {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }

            return Response({
                'detail': 'Phone number verified',
                'tokens': tokens
            }, status=status.HTTP_200_OK)

        return Response({'detail': 'SMS code is required'}, status=status.HTTP_400_BAD_REQUEST)


class PhoneNumberCheckView(GenericAPIView):
    serializer_class = PhoneNumberCheckSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data.get('phone_number')

        existing_user = User.objects.filter(phone_number=phone_number).first()

        if existing_user:
            return Response({'detail': 'Phone number already exists'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'Phone number is available'}, status=status.HTTP_200_OK)


class RequestVerificationCodeView(generics.GenericAPIView):
    serializer_class = RequestVerificationCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return Response({"detail": "Пользователь с указанным номером телефона не найден."},
                            status=status.HTTP_404_NOT_FOUND)

        verification_code = str(randint(100000, 999999))  # Генерация 6-значного кода
        VerificationCode.objects.update_or_create(user=user, defaults={'code': verification_code, 'verified': False})

        sms_text = f'От Bilimzet ваш код верификации: {verification_code}'
        send_sms(phone_number, sms_text)  # Функция для отправки SMS

        return Response({"detail": "Код верификации отправлен на указанный номер телефона."}, status=status.HTTP_200_OK)


class TokenObtainView(generics.GenericAPIView):
    serializer_class = TokenObtainSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        code = serializer.validated_data['code']

        try:
            user = User.objects.get(phone_number=phone_number)
            verification = VerificationCode.objects.get(user=user, code=code)
            if not verification.verified:
                return Response({"detail": "Код верификации не был подтвержден."}, status=status.HTTP_400_BAD_REQUEST)
        except (User.DoesNotExist, VerificationCode.DoesNotExist):
            return Response({"detail": "Пользователь или код верификации не найден."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Генерация токенов
        refresh = RefreshToken.for_user(user)
        tokens = {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

        # Пометка верификации как неактивной после использования
        verification.verified = False
        verification.save()

        return Response({"tokens": tokens}, status=status.HTTP_200_OK)


class PasswordUpdateView(generics.UpdateAPIView):
    serializer_class = PasswordUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Возвращает текущего пользователя
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_password = serializer.validated_data['new_password']
        user.set_password(new_password)
        user.save()

        return Response({"detail": "Пароль успешно обновлен."}, status=status.HTTP_200_OK)
