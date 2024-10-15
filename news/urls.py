from django.urls import path, include
from rest_framework.routers import DefaultRouter

from news.views import NewsViewSet

router = DefaultRouter()
router.register(r'news', NewsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
