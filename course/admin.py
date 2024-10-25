from django.contrib import admin

from course.models import Question, Exam, Review, Instructor, Module, Course, Answer, UserExamResult, UserAnswer, \
    Purchase, UserProgress, Duration, Category


class AnswerInline(admin.TabularInline):
    model = UserAnswer
    fields = ['answer', 'is_correct']
    extra = 1


class UserExamResultInline(admin.TabularInline):
    model = UserAnswer
    fields = ['answer', 'is_correct']
    extra = 1
    show_change_link = True


class ExamInline(admin.StackedInline):
    model = Exam
    extra = 1


class DurationInline(admin.StackedInline):
    model = Duration
    extra = 1


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1


class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'instructor', 'review_count', 'module_count']
    search_fields = ['title', 'description']
    inlines = [ModuleInline, ExamInline, DurationInline]


class InstructorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone_number', 'email']
    search_fields = ['first_name', 'last_name', 'email']


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['course', 'user', 'rating', 'comment']
    search_fields = ['course__title', 'user__username']


class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'progress_percentage']
    search_fields = ['user__username', 'course__title']


class UserExamResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'exam', 'score', 'total_questions', 'correct_answers', 'incorrect_answers']
    search_fields = ['user__username', 'exam__title']
    inlines = [UserExamResultInline]


class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ['user_exam_result', 'answer', 'is_correct']
    search_fields = ['user_exam_result__user__username', 'answer__text']


admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Module)
admin.site.register(Purchase)
admin.site.register(UserProgress, UserProgressAdmin)
admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(UserExamResult, UserExamResultAdmin)
admin.site.register(UserAnswer, UserAnswerAdmin)

admin.site.register(Duration)
admin.site.register(Category)
