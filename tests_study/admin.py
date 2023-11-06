from django.contrib import admin
from tests_study.models import Question, Answer, Test, QuestionTest

# Register your models here.
@admin.register(Question)
class QustionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'part', 'title', 'difficulty')
    list_filter = ('part',)
    search_fields = ('part', 'title', )


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'question', 'title',)
    list_filter = ('question',)
    search_fields = ( 'question', 'title', )


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    # list_display = ('pk', 'date_create', 'user', 'subject', 'type', 'ball',)
    list_filter = ('user', 'subject', 'type',)
    search_fields = ('user', 'subject', 'type',)


@admin.register(QuestionTest)
class QuestionTestAdmin(admin.ModelAdmin):
    list_display = ('pk', 'test', 'question', 'user_answer')
    list_filter = ('test', 'question', )
    search_fields = ('test', 'question', 'answer',)