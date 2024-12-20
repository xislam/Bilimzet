from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
import django_filters
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from course.models import Course, Category, Review, Purchase, Duration
from course.serializers.corse_serializers import CourseListSerializer, CourseDetailSerializer, \
    CoursePromotionSerializer, CategorySerializer, ReviewSerializer, ListPurchaseSerializer, UniqueNumberHoursSerializer


class CourseFilter(django_filters.FilterSet):
    number_hours = django_filters.NumberFilter(field_name='duration__number_hours')
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())
    language = django_filters.ChoiceFilter(choices=Course.LANGUAGE_CHOICES)

    class Meta:
        model = Course
        fields = ['number_hours', 'category', 'language']


class CourseListView(generics.ListAPIView):
    queryset = Course.objects.prefetch_related(
        Prefetch('duration_set', queryset=Duration.objects.all())
    ).all()
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


class PurchaseListView(generics.ListAPIView):
    serializer_class = ListPurchaseSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (JWTAuthentication,)

    def get_queryset(self):
        # Получаем все покупки текущего пользователя
        return Purchase.objects.filter(user=self.request.user)


class UniqueNumberHoursListView(generics.ListAPIView):
    serializer_class = UniqueNumberHoursSerializer

    def get_queryset(self):
        # Use distinct to get unique number_hours
        return Duration.objects.values('number_hours').distinct()
