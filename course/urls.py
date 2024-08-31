from django.urls import path

from course.api.crud_progress import UserProgressListView, UserProgressDetailView
from course.api.exam_api import ExamDetailView, SubmitExamAnswersView
from course.api.list_couse import CourseListView, CourseDetailView

urlpatterns = [
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),

    path('progress/', UserProgressListView.as_view(), name='user-progress-list'),
    path('progress/<int:pk>/', UserProgressDetailView.as_view(), name='user-progress-detail'),

    path('exams/<int:pk>/', ExamDetailView.as_view(), name='exam-detail'),
    path('exams/submit/', SubmitExamAnswersView.as_view(), name='submit-exam-answers'),
]
