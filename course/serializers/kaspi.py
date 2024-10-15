from rest_framework import serializers

from course.models import Purchase


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['course', 'kaspi', 'payment_status', 'payment_method']
