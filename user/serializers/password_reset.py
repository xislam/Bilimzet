from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from user.models import User


class PasswordResetSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=18)
    verification_code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        verification_code = attrs.get('verification_code')
        new_password = attrs.get('new_password')

        # Получаем пользователя по номеру телефона
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise serializers.ValidationError('User with this phone number does not exist')

        # Проверяем, совпадает ли код подтверждения
        if user.verification_code != verification_code:
            raise serializers.ValidationError('Invalid verification code')

        return attrs


class RequestPasswordResetSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=18)
