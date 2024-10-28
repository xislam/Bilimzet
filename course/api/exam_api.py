from rest_framework import status, viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from PIL import Image, ImageDraw, ImageFont
from rest_framework_simplejwt.authentication import JWTAuthentication

from course.models import Certificate, TestResult, UserAnswer, Answer, Question, Exam
from django.core.files.base import ContentFile

from course.serializers.exam import ExamDetailSerializer, CertificateSerializer


class ExamResultsViewSet(viewsets.ViewSet):
    authentication_classes = (JWTAuthentication,)

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
        duration_hours = exam.duration.number_hours  # Получаем количество часов из модели Duration
        certificate = None

        if correct_answers >= exam.correct_answers_required:
            # Генерация сертификата
            image_file = self.create_certificate_image(request.user.name, exam.title, duration_hours)

            # Создание и сохранение сертификата в базе данных
            certificate = Certificate.objects.create(
                user=request.user,
                exam=exam,
                file=ContentFile(image_file, name=f"{exam.title}_{duration_hours}h_{request.user.name}_certificate.jpg")
            )

        return Response({
            'correct_answers': correct_answers,
            'incorrect_answers': incorrect_answers,
            'total_questions': total_questions,
            'score': score,
            'certificate_issued': hasattr(certificate, 'id')  # Проверяем, выдан ли сертификат
        }, status=status.HTTP_201_CREATED)

    def create_certificate_image(self, name, course_name, duration_hours):
        # Создание сертификата как изображения
        image_path = f"{duration_hours}.jpg"
        output_path = f"{course_name}_{duration_hours}h_{name}_certificate.jpg"

        # Вызов функции добавления текста к изображению
        add_text_to_image(image_path, output_path, name, course_name)

        # Чтение сгенерированного изображения и возврат его как ContentFile
        with open(output_path, "rb") as img_file:
            return img_file.read()


def add_text_to_image(image_path, output_path, name, course_name, font_path="text.ttf", font_size=250,
                      position1=(4000, 4250), position2=(4000, 4850), fill_color='black'):
    # Открываем изображение
    image = Image.open(image_path)

    # Загружаем шрифт
    font = ImageFont.truetype(font_path, font_size)
    drawer = ImageDraw.Draw(image)

    # Добавляем текст
    drawer.text(position1, name, font=font, fill=fill_color)
    drawer.text(position2, course_name, font=font, fill=fill_color)

    # Сохраняем изображение
    image.save(output_path)


class ExamDetailView(generics.RetrieveAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamDetailSerializer
    lookup_field = 'id'


class CertificateListView(generics.ListAPIView):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (JWTAuthentication,)

    def get_queryset(self):
        """
        Optionally restricts the returned certificates to a given user or exam,
        by filtering against a `user_id` or `exam_id` query parameter in the URL.
        """
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id', None)
        exam_id = self.request.query_params.get('exam_id', None)

        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)
        if exam_id is not None:
            queryset = queryset.filter(exam_id=exam_id)

        return queryset
