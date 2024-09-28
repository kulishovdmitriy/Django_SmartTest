from django.contrib import admin

from smart_test.forms import QuestionsInlineFormSet, AnswerInlineFormSet
from smart_test.models import TestResult, Answer, Question, Test, Topic

# Register your models here.


class AnswerInline(admin.TabularInline):
    """
        Represents an inline form for the Answer model within the Django admin interface.

        Attributes:
            model: The model associated with this inline form, which is Answer.
            fields: The fields to be displayed in the inline form, specifically 'text' and 'is_correct'.
            show_change_link: A boolean indicating whether a change link should be shown for each inline form instance.
            extra: The number of extra forms to display in the inline formset.
            formset: The custom formset associated with this inline form, named AnswerInlineFormSet.
    """

    model = Answer
    fields = ('text', 'is_correct')
    show_change_link = True
    extra = 0
    formset = AnswerInlineFormSet


class QuestionAdminModel(admin.ModelAdmin):
    """
        Admin model for the Question entity.

        Attributes:
            inlines (tuple): A tuple containing the inlines for the admin model.

        Inlines:
            AnswerInline: This specifies that AnswerInline will be used as an inline within the QuestionAdminModel. This allows
            for Answer objects to be edited on the same page as the Question object in the Django admin interface.
    """

    inlines = (AnswerInline, )


class QuestionInline(admin.TabularInline):
    """
        QuestionInline

        A Django admin inline class to manage the Questions within another model in a tabular format.

        Attributes:
            model (Model): Specifies the model that this inline is for.
            fields (tuple): Specifies the fields to be displayed in the inline form.
            show_change_link (bool): Enables the change link next to each inline item.
            extra (int): Specifies the number of extra forms to display.
            formset (FormSet): Custom formset to be used with this inline.
            ordering (tuple): Specifies the default ordering for items in the inline.
    """

    model = Question
    fields = ('text', 'order_number')
    show_change_link = True
    extra = 0
    formset = QuestionsInlineFormSet
    ordering = ('order_number', )


class TestAdminModel(admin.ModelAdmin):
    """
        TestAdminModel class customizes the admin interface for a specific model.

        Attributes:
            list_per_page (int): Specifies the number of items to display per page in the admin list view.
            inlines (tuple): Specifies inline models to be displayed within the admin interface for this model.
    """

    list_per_page = 10
    inlines = (QuestionInline, )


admin.site.register(Topic)
admin.site.register(Test, TestAdminModel)
admin.site.register(Question, QuestionAdminModel)
admin.site.register(Answer)
admin.site.register(TestResult)
