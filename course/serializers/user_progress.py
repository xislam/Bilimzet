from rest_framework import serializers

from course.models import Module, UserProgress, Course


class ProgressCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'img']


class UserProgressSerializer(serializers.ModelSerializer):
    completed_modules = serializers.PrimaryKeyRelatedField(
        queryset=Module.objects.all(),
        many=True,
        required=False
    )
    course = ProgressCourseSerializer(read_only=True)  # Добавляем сериализатор курса

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


class UpdateUserProgressSerializer(serializers.ModelSerializer):
    completed_modules = serializers.PrimaryKeyRelatedField(
        queryset=Module.objects.all(),
        many=True,
        required=True
    )

    class Meta:
        model = UserProgress
        fields = ['id', 'course', 'duration', 'completed_modules']

    def create(self, validated_data):
        # Извлекаем completed_modules из данных
        completed_modules = validated_data.pop('completed_modules')

        # Создаем объект UserProgress без completed_modules
        user_progress = UserProgress.objects.create(user=self.context['request'].user, **validated_data)

        # Устанавливаем completed_modules через set()
        user_progress.completed_modules.set(completed_modules)
        user_progress.update_progress()  # Обновляем прогресс

        return user_progress

    def update(self, instance, validated_data):
        completed_modules = validated_data.pop('completed_modules', None)

        # Обновляем поля
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if completed_modules is not None:
            instance.completed_modules.set(completed_modules)  # Используем set()
            instance.update_progress()  # Обновляем прогресс

        instance.save()
        return instance
