from rest_framework import permissions, generics, serializers

from course.models import Exam
from course.serializers.exam import UserExamResultSerializer, QuestionSerializer


class ExamDetailView(generics.RetrieveAPIView):
    queryset = Exam.objects.all()
    serializer_class = serializers.ModelSerializer

    def get_serializer_class(self):
        class ExamDetailSerializer(serializers.ModelSerializer):
            questions = serializers.SerializerMethodField()

            class Meta:
                model = Exam
                fields = ['id', 'title', 'questions']

            def get_questions(self, obj):
                questions = obj.questions.all()
                return QuestionSerializer(questions, many=True).data

        return ExamDetailSerializer


class SubmitExamAnswersView(generics.CreateAPIView):
    serializer_class = UserExamResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
