from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from course.models import UserProgress
from course.serializers.user_progress import UserProgressSerializer, UpdateUserProgressSerializer


class UserProgressListView(generics.ListAPIView):
    serializer_class = UserProgressSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (JWTAuthentication,)

    def get_queryset(self):
        # Показываем только прогресс текущего пользователя
        return UserProgress.objects.filter(user=self.request.user)


class UserProgressView(generics.GenericAPIView):
    serializer_class = UpdateUserProgressSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (JWTAuthentication,)


    def get_object(self):
        user = self.request.user
        course_id = self.kwargs.get('course_id')
        duration_id = self.kwargs.get('duration_id')

        try:
            return UserProgress.objects.get(user=user, course_id=course_id, duration_id=duration_id)
        except UserProgress.DoesNotExist:
            return None

    def post(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance is not None:
            # Если объект существует, обновляем его
            serializer = self.get_serializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Если объекта нет, создаем новый
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()  # Пользователь устанавливается в сериализаторе
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is not None:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
