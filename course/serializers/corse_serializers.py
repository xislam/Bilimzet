from rest_framework import serializers

from course.models import Course, Module, Review, Instructor, UserProgress, Duration, Purchase, Category, Exam, \
    Certificate


class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = ['first_name', 'last_name', 'avatar', 'phone_number', 'email']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'course', 'user', 'rating', 'comment']
        read_only_fields = ['user']


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['title', 'description', 'video_url', 'pdf_document']


class DurationSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)
    exam_ids = serializers.SerializerMethodField()
    is_purchased = serializers.SerializerMethodField()  # Check if the course was purchased
    certificate_files_user = serializers.SerializerMethodField()  # New field for certificate files

    class Meta:
        model = Duration
        fields = '__all__'

    def get_exam_ids(self, obj):
        return [exam.id for exam in obj.exam_set.all()]

    def get_is_purchased(self, obj):
        request = self.context.get('request', None)
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            user = request.user
            # Проверяем, существует ли покупка с данным пользователем, продолжительностью и статусом "completed"
            purchase = Purchase.objects.filter(duration=obj, user=user, payment_status='completed').exists()
            return purchase
        return False

    def get_certificate_files_user(self, obj):
        user = self.context.get('request', None)
        if user and hasattr(user, 'user') and user.user.is_authenticated:
            user = user.user
            certificates = Certificate.objects.filter(user=user, exam__duration=obj)
            return [certificate.file.url for certificate in certificates if certificate.file]
        return []


class CourseListSerializer(serializers.ModelSerializer):
    review_count = serializers.IntegerField(read_only=True)
    module_count = serializers.IntegerField(read_only=True)
    instructor = InstructorSerializer()
    user_progress = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()

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

    def get_duration(self, obj):
        duration_instances = Duration.objects.filter(course=obj)
        if duration_instances:
            return DurationSerializer(duration_instances, many=True).data
        return None


class CourseDetailSerializer(serializers.ModelSerializer):
    review_count = serializers.IntegerField(read_only=True)
    module_count = serializers.IntegerField(read_only=True)
    instructor = InstructorSerializer()
    reviews = ReviewSerializer(many=True, read_only=True)
    user_progress = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()
    is_purchased = serializers.SerializerMethodField()  # Новое поле для проверки, был ли курс куплен
    purchase_details = serializers.SerializerMethodField()  # Информация о продолжительности курса, если куплен
    certificates = serializers.SerializerMethodField()  # Новое поле для сертификатов

    class Meta:
        model = Course
        fields = [
            'id', 'category', 'img', 'doc', 'title', 'description', 'review_count', 'module_count', 'instructor',
            'reviews',
            'user_progress', 'duration', 'is_purchased', 'purchase_details', 'certificates'
        ]

    def get_duration(self, obj):
        # Получаем продолжительности для курса (уже загружены с помощью prefetch_related)
        duration_instances = obj.duration_set.all()
        if duration_instances:
            # Передаем контекст с пользователем в DurationSerializer
            context = self.context
            return DurationSerializer(duration_instances, many=True, context=context).data
        return None

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

    def get_is_purchased(self, obj):
        # Проверяем, куплен ли курс пользователем
        user = self.context.get('request', None)
        if user and hasattr(user, 'user') and user.user.is_authenticated:
            user = user.user
            purchase = Purchase.objects.filter(course=obj, user=user, payment_status='completed').first()
            return purchase is not None
        return False

    def get_purchase_details(self, obj):
        # Возвращает подробности о покупке курса, если он был куплен
        user = self.context.get('request', None)
        if user and hasattr(user, 'user') and user.user.is_authenticated:
            user = user.user
            purchase = Purchase.objects.filter(course=obj, user=user, payment_status='completed').first()
            if purchase:
                return {
                    'purchase_at': purchase.purchased_at,
                    'duration': DurationSerializer(purchase.duration).data,
                    'payment_method': purchase.payment_method,
                }
        return None

    def get_certificates(self, obj):
        # Возвращает список сертификатов из всех продолжительностей курса
        duration_instances = Duration.objects.filter(course=obj)
        certificates = []
        for duration in duration_instances:
            if duration.certificate:
                certificates.append({
                    'certificate_url': duration.certificate.url,
                })
        return certificates


class CoursePromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'img', 'instructor', 'language', 'has_promotion', 'discount_percentage']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ListPurchaseSerializer(serializers.ModelSerializer):
    duration = DurationSerializer()
    course = serializers.SerializerMethodField()

    class Meta:
        model = Purchase
        fields = ['id', 'course', 'duration', 'purchased_at', 'kaspi', 'payment_status', 'payment_method']

    def get_course(self, obj):
        # Assuming obj.course is the Course instance
        return obj.course.title if obj.course else None


class UniqueNumberHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = Duration
        fields = ['number_hours']
