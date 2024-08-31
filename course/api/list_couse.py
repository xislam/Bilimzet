from rest_framework import generics

from course.models import Course
from course.serializers.corse_serializers import CourseListSerializer, CourseDetailSerializer


class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer

    def get_serializer_context(self):
        # Передаем контекст запроса в сериализатор
        return {'request': self.request}


class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
