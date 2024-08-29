import random

from rest_framework import serializers
from rest_framework.exceptions import APIException

from user.models import User
from user.sms_utils import send_sms


class PhoneNumberNotVerified(APIException):
    status_code = 405
    default_detail = 'Номер телефона не верифицирован'
    default_code = 'phone_number_not_verified'


class CustomTokenObtainPairSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=18)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise serializers.ValidationError('Нет активного аккаунта с предоставленными учетными данными',
                                              code='no_active_account')

        if not user.check_password(password):
            raise serializers.ValidationError('Неправильный пароль или номер телефона', code='incorrect_password')

        if not user.phone_number_verified:
            # Отправить SMS-код подтверждения пользователю
            verification_code = random.randint(100000, 999999)
            sms_text = f'От Bilimzet ваш код верификации: {verification_code}'
            send_sms(phone_number, sms_text)

            # Сохранить код подтверждения в базе данных или кэше для дальнейшей проверки
            user.verification_code = verification_code
            user.save()

            raise PhoneNumberNotVerified()

        attrs['user'] = user
        return attrs
