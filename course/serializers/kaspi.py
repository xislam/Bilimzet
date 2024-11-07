from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from course.models import Purchase


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['course', 'kaspi', 'payment_status', 'payment_method', 'duration']

    def validate(self, data):
        user = self.context['request'].user
        duration = data.get('duration')

        # Проверка, есть ли уже покупка с такой продолжительностью для текущего пользователя
        if Purchase.objects.filter(user=user, duration=duration).exists():
            raise serializers.ValidationError(
                _("Вы уже приобретали курс с такой продолжительностью.")
            )

        return data
