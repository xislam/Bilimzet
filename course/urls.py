from django.urls import path

from course.api.crud_progress import UserProgressListView, UserProgressDetailView
from course.api.exam_api import ExamDetailView, SubmitExamAnswersView
from course.api.kaspi_api import PurchaseCreateView
from course.api.list_couse import CourseListView, CourseDetailView, CourseWithPromotionList, CategoryListView, \
    ReviewListCreateView, ReviewDetailView

urlpatterns = [
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('categories/', CategoryListView.as_view(), name='category-list'),

    path('progress/', UserProgressListView.as_view(), name='user-progress-list'),
    path('progress/<int:pk>/', UserProgressDetailView.as_view(), name='user-progress-detail'),

    path('exams/<int:pk>/', ExamDetailView.as_view(), name='exam-detail'),
    path('exams/submit/', SubmitExamAnswersView.as_view(), name='submit-exam-answers'),
    path('kaspi/', PurchaseCreateView.as_view(), name='kaspi-create'),
    path('courses/with-promotions/', CourseWithPromotionList.as_view(), name='courses_with_promotions'),

    path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),

]
