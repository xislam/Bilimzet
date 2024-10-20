from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
import django_filters
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from course.models import Course, Category, Review
from course.serializers.corse_serializers import CourseListSerializer, CourseDetailSerializer, \
    CoursePromotionSerializer, CategorySerializer, ReviewSerializer


class CourseFilter(django_filters.FilterSet):
    number_hours = django_filters.NumberFilter(field_name='duration__number_hours')
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())
    language = django_filters.ChoiceFilter(choices=Course.LANGUAGE_CHOICES)

    class Meta:
        model = Course
        fields = ['number_hours', 'category', 'language']


class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = CourseFilter
    search_fields = ['title']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        # Проверяем, есть ли запрос и пользователь в контексте запроса
        if self.request and hasattr(self.request, 'user'):
            context['request'] = self.request
        return context


class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer


class CourseWithPromotionList(generics.ListAPIView):
    queryset = Course.objects.filter(has_promotion=True)
    serializer_class = CoursePromotionSerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (JWTAuthentication,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (JWTAuthentication,)
