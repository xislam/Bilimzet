from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from user.models import User
from user.serializers.password_reset import PasswordResetSerializer


class PasswordResetView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data.get('phone_number')
        verification_code = serializer.validated_data.get('verification_code')
        new_password = serializer.validated_data.get('new_password')

        user = User.objects.filter(phone_number=phone_number).first()

        if not user or user.verification_code != verification_code:
            return Response({'detail': 'Invalid verification code'}, status=status.HTTP_400_BAD_REQUEST)

        # Update the user's password
        user.set_password(new_password)
        user.save()

        return Response({'detail': 'Password updated successfully'}, status=status.HTTP_200_OK)
