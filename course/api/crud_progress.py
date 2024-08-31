from rest_framework import generics, permissions

from course.models import UserProgress
from course.serializers.user_progress import UserProgressSerializer


class UserProgressListView(generics.ListAPIView):
    serializer_class = UserProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Показываем только прогресс текущего пользователя
        return UserProgress.objects.filter(user=self.request.user)


class UserProgressDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Разрешаем доступ только к прогрессу текущего пользователя
        return UserProgress.objects.filter(user=self.request.user)
