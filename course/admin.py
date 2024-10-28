from django.contrib import admin

from course.models import Question, Exam, Review, Instructor, Module, Course, Answer, \
    Purchase, UserProgress, Duration, Category, Certificate


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1  # Количество пустых форм для добавления новых отзывов


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1  # Количество пустых форм для добавления новых модулей


class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 1  # Количество пустых форм для добавления новых ответов


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1  # Количество пустых форм для добавления новых вопросов
    inlines = [AnswerInline]


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'email')
    search_fields = ('first_name', 'last_name', 'email')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'category', 'language', 'has_promotion', 'discount_percentage')
    search_fields = ('title',)
    list_filter = ('category', 'instructor', 'language', 'has_promotion')
    inlines = [ReviewInline]  # Добавляем Inline для отзывов


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'rating', 'comment')
    search_fields = ('user__username', 'course__title')


@admin.register(Duration)
class DurationAdmin(admin.ModelAdmin):
    list_display = ('course', 'number_hours', 'price')
    search_fields = ('course__title',)
    inlines = [ModuleInline]  # Вложенные модули


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration', 'video_url', 'pdf_document')
    search_fields = ('title', 'duration__course__title')


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'duration', 'purchased_at', 'payment_status', 'payment_method')
    search_fields = ('user__username', 'course__title')
    list_filter = ('payment_status', 'payment_method', 'purchased_at')


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'duration', 'progress_percentage')
    search_fields = ('user__username', 'course__title')
    list_filter = ('duration',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'exam')
    search_fields = ('text', 'exam__title')
    inlines = [AnswerInline]  # Вложенные ответы


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration', 'correct_answers_required')
    search_fields = ('title',)
    inlines = [QuestionInline]  # Вложенные вопросы


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
    search_fields = ('text', 'question__text')


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('user', 'exam', 'file')
    search_fields = ('user',)
