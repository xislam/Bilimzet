from rest_framework import serializers

from user.models import User, AdditionalInfo


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'phone_number', 'avatar', 'receive_notifications', 'receive_promotions',
                  'receive_email_notifications']


class AdditionalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalInfo
        fields = ['iin', 'position', 'workplace', 'phone_number', 'education_diploma']
