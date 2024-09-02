from rest_framework import serializers

from user.models import User


class PhoneNumberVerificationSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=18)
    sms_code = serializers.CharField(max_length=6)


class PhoneNumberCheckSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=18)


class RequestVerificationCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=18)

    def validate_phone_number(self, value):
        # Проверяем, существует ли пользователь с таким номером телефона
        if not User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Пользователь с указанным номером телефона не найден.")
        return value


class TokenObtainSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=18)
    code = serializers.CharField(max_length=6)


class PasswordUpdateSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, min_length=8)

