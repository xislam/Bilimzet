from django.db import models

from user.models import User


class Instructor(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    avatar = models.ImageField(upload_to='instructors/avatars/', blank=True, null=True, verbose_name="Аватар")
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефона")
    email = models.EmailField(verbose_name="Почта")

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Review(models.Model):
    course = models.ForeignKey('Course', related_name='reviews', on_delete=models.CASCADE, verbose_name="Курс")
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE, verbose_name="Пользователь")
    rating = models.IntegerField(verbose_name="Рейтинг")
    comment = models.TextField(verbose_name="Комментарий", blank=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"Отзыв от {self.user.username} на {self.course.title}"


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название курса")
    description = models.TextField(verbose_name="Описание курса")
    img = models.ImageField(upload_to='course_img', verbose_name='Фото курса')
    instructor = models.ForeignKey(Instructor, related_name='courses', on_delete=models.SET_NULL, null=True,
                                   verbose_name="Преподаватель")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title

    @property
    def review_count(self):
        return self.reviews.count()

    @property
    def module_count(self):
        return self.modules.count()


class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE, verbose_name="Курс")
    title = models.CharField(max_length=255, verbose_name="Название модуля")
    description = models.TextField(verbose_name="Описание модуля")
    video_url = models.URLField(blank=True, null=True, verbose_name="URL видео")
    pdf_document = models.FileField(upload_to='modules/pdf/', blank=True, null=True, verbose_name="PDF документ")

    class Meta:
        verbose_name = "Модуль"
        verbose_name_plural = "Модули"

    def __str__(self):
        return self.title


class Purchase(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('completed', 'Оплачено'),
        ('failed', 'Не удалось'),
        ('refunded', 'Возвращено'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('kaspi', 'Kaspi'),
        ('freedom_pay', 'Freedom Pay'),
    ]
    user = models.ForeignKey(User, related_name='purchases', on_delete=models.CASCADE, verbose_name="Пользователь")
    course = models.ForeignKey(Course, related_name='purchases', on_delete=models.CASCADE, verbose_name="Курс")
    purchased_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата покупки")
    kaspi = models.CharField(verbose_name='Номер каспи', max_length=14)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending',
                                      verbose_name='Статус оплаты')
    payment_method = models.CharField(max_length=15, choices=PAYMENT_METHOD_CHOICES, verbose_name='Способ оплаты')

    class Meta:
        verbose_name = "Покупка"
        verbose_name_plural = "Покупки"

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"


class UserProgress(models.Model):
    user = models.ForeignKey(User, related_name='progress', on_delete=models.CASCADE, verbose_name="Пользователь")
    course = models.ForeignKey(Course, related_name='progress', on_delete=models.CASCADE, verbose_name="Курс")
    completed_modules = models.ManyToManyField(Module, blank=True, verbose_name="Пройденные модули")
    progress_percentage = models.FloatField(default=0.0, verbose_name="Прогресс в процентах")

    class Meta:
        verbose_name = "Прогресс пользователя"
        verbose_name_plural = "Прогрессы пользователей"

    def update_progress(self):
        total_modules = self.course.modules.count()
        completed_modules = self.completed_modules.count()
        if total_modules > 0:
            self.progress_percentage = (completed_modules / total_modules) * 100
        else:
            self.progress_percentage = 0
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.course.title} - {self.progress_percentage}%"


class Exam(models.Model):
    course = models.OneToOneField(Course, related_name='exam', on_delete=models.CASCADE, verbose_name="Курс")
    title = models.CharField(max_length=255, verbose_name="Название экзамена")

    class Meta:
        verbose_name = "Экзамен"
        verbose_name_plural = "Экзамены"

    def __str__(self):
        return f"Экзамен для курса: {self.course.title}"


class Question(models.Model):
    exam = models.ForeignKey(Exam, related_name='questions', on_delete=models.CASCADE, verbose_name="Экзамен")
    text = models.CharField(max_length=255, verbose_name="Текст вопроса")

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE, verbose_name="Вопрос")
    text = models.CharField(max_length=255, verbose_name="Текст ответа")
    is_correct = models.BooleanField(default=False, verbose_name="Правильный ответ")

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self):
        return self.text


class UserExamResult(models.Model):
    user = models.ForeignKey(User, related_name='exam_results', on_delete=models.CASCADE, verbose_name="Пользователь")
    exam = models.ForeignKey(Exam, related_name='user_results', on_delete=models.CASCADE, verbose_name="Экзамен")
    answers = models.ManyToManyField(Answer, through='UserAnswer', verbose_name="Ответы пользователя")
    score = models.FloatField(default=0.0, verbose_name="Оценка")
    total_questions = models.IntegerField(default=0, verbose_name="Всего вопросов")
    correct_answers = models.IntegerField(default=0, verbose_name="Правильные ответы")
    incorrect_answers = models.IntegerField(default=0, verbose_name="Неправильные ответы")

    class Meta:
        verbose_name = "Результат экзамена пользователя"
        verbose_name_plural = "Результаты экзаменов пользователей"

    def calculate_score(self):
        if self.total_questions > 0:
            self.score = (self.correct_answers / self.total_questions) * 100
        else:
            self.score = 0.0
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.exam.title} - {self.score}%"


class UserAnswer(models.Model):
    user_exam_result = models.ForeignKey(UserExamResult, related_name='user_answers', on_delete=models.CASCADE,
                                         verbose_name="Результат экзамена пользователя")
    answer = models.ForeignKey(Answer, related_name='user_answers', on_delete=models.CASCADE, verbose_name="Ответ")
    is_correct = models.BooleanField(default=False, verbose_name="Правильный ответ")

    class Meta:
        verbose_name = "Ответ пользователя"
        verbose_name_plural = "Ответы пользователей"

    def __str__(self):
        return f"{self.user_exam_result.user.name} - {self.answer.text} - {'Correct' if self.is_correct else 'Incorrect'}"
