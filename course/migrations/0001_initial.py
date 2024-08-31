# Generated by Django 4.2.15 on 2024-08-31 13:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название курса')),
                ('description', models.TextField(verbose_name='Описание курса')),
                ('img', models.ImageField(upload_to='course_img', verbose_name='Фото курса')),
            ],
            options={
                'verbose_name': 'Курс',
                'verbose_name_plural': 'Курсы',
            },
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название экзамена')),
                ('course', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='exam', to='course.course', verbose_name='Курс')),
            ],
            options={
                'verbose_name': 'Экзамен',
                'verbose_name_plural': 'Экзамены',
            },
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='instructors/avatars/', verbose_name='Аватар')),
                ('phone_number', models.CharField(max_length=20, verbose_name='Номер телефона')),
                ('email', models.EmailField(max_length=254, verbose_name='Почта')),
            ],
            options={
                'verbose_name': 'Преподаватель',
                'verbose_name_plural': 'Преподаватели',
            },
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название модуля')),
                ('description', models.TextField(verbose_name='Описание модуля')),
                ('video_url', models.URLField(blank=True, null=True, verbose_name='URL видео')),
                ('pdf_document', models.FileField(blank=True, null=True, upload_to='modules/pdf/', verbose_name='PDF документ')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modules', to='course.course', verbose_name='Курс')),
            ],
            options={
                'verbose_name': 'Модуль',
                'verbose_name_plural': 'Модули',
            },
        ),
        migrations.CreateModel(
            name='UserProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('progress_percentage', models.FloatField(default=0.0, verbose_name='Прогресс в процентах')),
                ('completed_modules', models.ManyToManyField(blank=True, to='course.module', verbose_name='Пройденные модули')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='progress', to='course.course', verbose_name='Курс')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='progress', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Прогресс пользователя',
                'verbose_name_plural': 'Прогрессы пользователей',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(verbose_name='Рейтинг')),
                ('comment', models.TextField(blank=True, verbose_name='Комментарий')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='course.course', verbose_name='Курс')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255, verbose_name='Текст вопроса')),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='course.exam', verbose_name='Экзамен')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
            },
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchased_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата покупки')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchases', to='course.course', verbose_name='Курс')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchases', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Покупка',
                'verbose_name_plural': 'Покупки',
            },
        ),
        migrations.AddField(
            model_name='course',
            name='instructor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='courses', to='course.instructor', verbose_name='Преподаватель'),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255, verbose_name='Текст ответа')),
                ('is_correct', models.BooleanField(default=False, verbose_name='Правильный ответ')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='course.question', verbose_name='Вопрос')),
            ],
            options={
                'verbose_name': 'Ответ',
                'verbose_name_plural': 'Ответы',
            },
        ),
    ]
