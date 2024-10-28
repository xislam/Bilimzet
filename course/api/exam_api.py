from rest_framework import status, viewsets
from rest_framework.response import Response

from course.models import Certificate, TestResult, UserAnswer, Answer, Question, Exam


class ExamResultsViewSet(viewsets.ViewSet):
    def create(self, request, exam_id):
        exam = Exam.objects.get(id=exam_id)
        user_answers = request.data.get('user_answers')  # Ожидаем список словарей с вопросами и ответами

        correct_answers = 0
        total_questions = exam.questions.count()

        for ua in user_answers:
            question_id = ua['question_id']
            selected_answer_id = ua['selected_answer_id']
            question = Question.objects.get(id=question_id)
            selected_answer = Answer.objects.get(id=selected_answer_id)

            # Сохраняем ответ пользователя
            UserAnswer.objects.create(
                user=request.user,
                question=question,
                selected_answer=selected_answer
            )

            if selected_answer.is_correct:
                correct_answers += 1

        incorrect_answers = total_questions - correct_answers
        score = correct_answers  # Или можно использовать другой алгоритм для расчета баллов

        # Сохраняем результаты теста
        TestResult.objects.create(
            user=request.user,
            exam=exam,
            correct_answers=correct_answers,
            incorrect_answers=incorrect_answers,
            total_questions=total_questions,
            score=score
        )

        # Условие для выдачи сертификата
        certificate = None
        if correct_answers >= exam.correct_answers_required:
            certificate, created = Certificate.objects.get_or_create(user=request.user, exam=exam)
            if created:
                # Генерация сертификата
                pdf_file = self.create_certificate_pdf(request.user.username, exam.title)
                certificate.file.save(f"{request.user.username}_certificate.pdf", File(pdf_file))

        return Response({
            'correct_answers': correct_answers,
            'incorrect_answers': incorrect_answers,
            'total_questions': total_questions,
            'score': score,
            'certificate_issued': hasattr(certificate, 'id')  # Проверяем, выдан ли сертификат
        }, status=status.HTTP_201_CREATED)


