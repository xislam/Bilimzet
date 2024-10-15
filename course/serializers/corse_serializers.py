from rest_framework import serializers

from course.models import Course, Module, Review, Instructor, UserProgress, Duration


class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = ['first_name', 'last_name', 'avatar', 'phone_number', 'email']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['user', 'rating', 'comment']


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['title', 'description', 'video_url', 'pdf_document']


class DurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Duration
        fields = '__all__'


class CourseListSerializer(serializers.ModelSerializer):
    review_count = serializers.IntegerField(read_only=True)
    module_count = serializers.IntegerField(read_only=True)
    instructor = InstructorSerializer()
    user_progress = serializers.SerializerMethodField()
    duration = DurationSerializer()

    class Meta:
        model = Course
        fields = ['id', 'img', 'title', 'description', 'review_count', 'module_count', 'instructor', 'user_progress',
                  'duration']

    def get_user_progress(self, obj):
        # Проверяем, есть ли пользователь в контексте сериализатора и является ли он аутентифицированным
        user = self.context.get('request', None)
        if user and hasattr(user, 'user') and user.user.is_authenticated:
            user = user.user
        else:
            # Если пользователь не аутентифицирован, возвращаем 0 прогресса
            return {
                'completed_modules': 0,
                'progress_percentage': 0.0
            }

        # Если пользователь аутентифицирован, пытаемся получить его прогресс
        try:
            progress = UserProgress.objects.get(user=user, course=obj)
            return {
                'completed_modules': progress.completed_modules.count(),
                'progress_percentage': progress.progress_percentage
            }
        except UserProgress.DoesNotExist:
            # Если прогресса нет, возвращаем 0
            return {
                'completed_modules': 0,
                'progress_percentage': 0.0
            }


class CourseDetailSerializer(serializers.ModelSerializer):
    review_count = serializers.IntegerField(read_only=True)
    module_count = serializers.IntegerField(read_only=True)
    instructor = InstructorSerializer()
    reviews = ReviewSerializer(many=True, read_only=True)
    modules = ModuleSerializer(many=True, read_only=True)
    exam_id = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'img', 'title', 'description', 'review_count', 'module_count', 'instructor', 'reviews',
                  'modules', 'exam_id']

    def get_exam_id(self, obj):
        # Return the exam ID if the course has an associated exam
        if obj.exam:
            return obj.exam.id
        return None
