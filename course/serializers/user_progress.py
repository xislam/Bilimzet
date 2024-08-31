from rest_framework import serializers

from course.models import Module, UserProgress


class UserProgressSerializer(serializers.ModelSerializer):
    completed_modules = serializers.PrimaryKeyRelatedField(
        queryset=Module.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = UserProgress
        fields = ['id', 'user', 'course', 'completed_modules', 'progress_percentage']
        read_only_fields = ['progress_percentage']

    def update(self, instance, validated_data):
        completed_modules = validated_data.pop('completed_modules', None)

        if completed_modules is not None:
            instance.completed_modules.set(completed_modules)
            instance.update_progress()

        return super().update(instance, validated_data)
