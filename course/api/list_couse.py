from rest_framework import generics

from course.models import Course
from course.serializers.corse_serializers import CourseListSerializer, CourseDetailSerializer


class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        # Проверяем, есть ли запрос и пользователь в контексте запроса
        if self.request and hasattr(self.request, 'user'):
            context['request'] = self.request
        return context


class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
