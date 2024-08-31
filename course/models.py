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
    user = models.ForeignKey(User, related_name='purchases', on_delete=models.CASCADE, verbose_name="Пользователь")
    course = models.ForeignKey(Course, related_name='purchases', on_delete=models.CASCADE, verbose_name="Курс")
    purchased_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата покупки")

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
