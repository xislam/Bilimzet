from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import User
from user.serializers.verification_number import PhoneNumberVerificationSerializer, PhoneNumberCheckSerializer


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
