from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from news.models import News
from news.serializers import NewsSerializer


# Create your views here.
class NewsViewSet(viewsets.GenericViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            news_item = self.get_object()
            news_item.number_views += 1
            news_item.save()
            serializer = self.get_serializer(news_item)
            return Response(serializer.data)
        except News.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    def get_object(self):
        queryset = self.get_queryset()
        filter_kwargs = {'pk': self.kwargs['pk']}
        return get_object_or_404(queryset, **filter_kwargs)
