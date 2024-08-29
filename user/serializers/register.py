from rest_framework import serializers

from user.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)  # Added email field

    class Meta:
        model = User
        fields = ('phone_number', 'password', 'name', 'email')  # Included email field

    def create(self, validated_data):
        user = User.objects.create(
            phone_number=validated_data['phone_number'],
            name=validated_data['name'],
            email=validated_data['email']  # Save email field
        )
        user.set_password(validated_data['password'])
        user.save()

        return user
