from rest_framework import serializers


class PhoneNumberVerificationSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=18)
    sms_code = serializers.CharField(max_length=6)


class PhoneNumberCheckSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=18)
