from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from course.models import Purchase
from course.serializers.kaspi import PurchaseSerializer


class PurchaseCreateView(generics.CreateAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (JWTAuthentication,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
