from rest_framework import serializers

from course.models import Course, Module, Review, Instructor


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


class CourseListSerializer(serializers.ModelSerializer):
    review_count = serializers.IntegerField(read_only=True)
    module_count = serializers.IntegerField(read_only=True)
    instructor = InstructorSerializer()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'review_count', 'module_count', 'instructor']


class CourseDetailSerializer(serializers.ModelSerializer):
    review_count = serializers.IntegerField(read_only=True)
    module_count = serializers.IntegerField(read_only=True)
    instructor = InstructorSerializer()
    reviews = ReviewSerializer(many=True, read_only=True)
    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'review_count', 'module_count', 'instructor', 'reviews', 'modules']
