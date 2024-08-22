from django.contrib import admin

from smart_test.forms import QuestionsInlineFormSet, AnswerInlineFormSet
from smart_test.models import TestResult, Answer, Question, Test, Topic

# Register your models here.


class AnswerInline(admin.TabularInline):
    model = Answer
    fields = ('text', 'is_correct')
    show_change_link = True
    extra = 0
    formset = AnswerInlineFormSet


class QuestionAdminModel(admin.ModelAdmin):
    inlines = (AnswerInline, )


class QuestionInline(admin.TabularInline):
    model = Question
    fields = ('text', 'order_number')
    show_change_link = True
    extra = 0
    formset = QuestionsInlineFormSet
    ordering = ('order_number', )


class TestAdminModel(admin.ModelAdmin):

    list_per_page = 10
    inlines = (QuestionInline, )


admin.site.register(Topic)
admin.site.register(Test, TestAdminModel)
admin.site.register(Question, QuestionAdminModel)
admin.site.register(Answer)
admin.site.register(TestResult)
