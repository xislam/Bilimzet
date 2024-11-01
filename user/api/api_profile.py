from django.contrib.auth.hashers import check_password
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import AdditionalInfo
from user.serializers.profile import UserProfileSerializer, AdditionalInfoSerializer


class UserProfileDetailView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (JWTAuthentication,)

    def get_object(self):
        return self.request.user


class UserProfileUpdateView(generics.UpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (JWTAuthentication,)

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class UserProfileDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (JWTAuthentication,)

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response({"detail": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class UserPasswordUpdateView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (JWTAuthentication,)

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not old_password or not new_password:
            return Response({"detail": "Both old and new passwords are required."}, status=status.HTTP_400_BAD_REQUEST)

        if not check_password(old_password, user.password):
            return Response({"detail": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

        if old_password == new_password:
            return Response({"detail": "New password cannot be the same as the old password."},
                            status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        # Optionally, invalidate the user's JWT tokens
        # You can also log the user out by removing their refresh token if needed

        return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)


class AdditionalInfoView(generics.RetrieveUpdateAPIView):
    serializer_class = AdditionalInfoSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (JWTAuthentication,)

    def get_object(self):
        # Получаем или создаем объект дополнительной информации для текущего пользователя
        user = self.request.user
        additional_info, created = AdditionalInfo.objects.get_or_create(user=user)
        return additional_info


class AdditionalInfoCreateView(generics.CreateAPIView):
    serializer_class = AdditionalInfoSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (JWTAuthentication,)

    def create(self, request, *args, **kwargs):
        # Обработка создания нового объекта дополнительной информации
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        additional_info = serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
