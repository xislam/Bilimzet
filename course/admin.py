from django.contrib import admin

from course.models import Question, Exam, Review, Instructor, Module, Course, Answer, UserExamResult, UserAnswer


class ModuleInline(admin.TabularInline):  # Используем TabularInline для компактного отображения
    model = Module
    extra = 1  # Показывает одну пустую строку для добавления нового модуля


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


class AnswerInline(admin.TabularInline):
    model = Answer
    fields = ['answer', 'is_correct']
    extra = 1


class ExamAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'instructor', 'review_count', 'module_count']
    search_fields = ['title', 'description']
    inlines = [ModuleInline, ReviewInline]


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone_number', 'email']
    search_fields = ['first_name', 'last_name', 'email']


# Регистрация моделей с правильным отображением связанных объектов
admin.site.register(Module)
admin.site.register(Review)
admin.site.register(Exam, ExamAdmin)
admin.site.register(Question, QuestionAdmin)


# Register your models here.

class UserExamResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'exam', 'score', 'total_questions', 'correct_answers', 'incorrect_answers']
    search_fields = ['user__username', 'exam__title']
    inlines = [AnswerInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'exam')


class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ['user_exam_result', 'answer', 'is_correct']
    search_fields = ['user_exam_result__user__username', 'answer__text']


admin.site.register(UserExamResult, UserExamResultAdmin)
admin.site.register(UserAnswer, UserAnswerAdmin)
