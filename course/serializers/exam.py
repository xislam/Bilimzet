from rest_framework import serializers

from course.models import UserAnswer, UserExamResult, Answer, Question, Exam


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'answers']


class ExamDetailSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Exam
        fields = ['id', 'title', 'questions', 'duration', 'correct_answers_required']

    def get_questions(self, obj):
        questions = obj.questions.all()
        return QuestionSerializer(questions, many=True).data


class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = ['answer', 'is_correct']


class UserExamResultSerializer(serializers.ModelSerializer):
    answers = UserAnswerSerializer(many=True)

    class Meta:
        model = UserExamResult
        fields = ['id', 'user', 'exam', 'answers', 'score', 'total_questions', 'correct_answers', 'incorrect_answers']

    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        user_exam_result = UserExamResult.objects.create(**validated_data)
        total_questions = 0
        correct_answers = 0
        incorrect_answers = 0

        for answer_data in answers_data:
            answer = answer_data['answer']
            is_correct = answer_data['is_correct']
            UserAnswer.objects.create(user_exam_result=user_exam_result, answer=answer, is_correct=is_correct)
            if is_correct:
                correct_answers += 1
            else:
                incorrect_answers += 1
            total_questions += 1

        user_exam_result.total_questions = total_questions
        user_exam_result.correct_answers = correct_answers
        user_exam_result.incorrect_answers = incorrect_answers
        user_exam_result.calculate_score()
        return user_exam_result
