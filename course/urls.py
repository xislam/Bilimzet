from django.conf.urls.static import static
from django.urls import path

from course.api.crud_progress import UserProgressListView, UserProgressView
from course.api.exam_api import ExamDetailView, ExamResultsViewSet, MyCertificatesView
from course.api.kaspi_api import PurchaseCreateView
from course.api.list_couse import CourseListView, CourseDetailView, CourseWithPromotionList, CategoryListView, \
    ReviewListCreateView, ReviewDetailView, PurchaseListView
from root import settings

urlpatterns = [
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('categories/', CategoryListView.as_view(), name='category-list'),

    path('exams/<int:id>/', ExamDetailView.as_view(), name='exam-detail'),

    path('progress/', UserProgressListView.as_view(), name='user-progress-list'),
    path('progress/<int:course_id>/<int:duration_id>/', UserProgressView.as_view(), name='user-progress'),

    path('kaspi/', PurchaseCreateView.as_view(), name='kaspi-create'),
    path('courses/with-promotions/', CourseWithPromotionList.as_view(), name='courses_with_promotions'),

    path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    path('exams/<int:exam_id>/results/', ExamResultsViewSet.as_view({'post': 'create'}), name='exam-results'),
    path('my/certificates/', MyCertificatesView.as_view(), name='certificate-list'),
    path('purchases/', PurchaseListView.as_view(), name='purchase-list'),

]
