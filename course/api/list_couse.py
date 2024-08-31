from rest_framework import generics

from course.models import Course
from course.serializers.corse_serializers import CourseListSerializer, CourseDetailSerializer


class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer


class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
