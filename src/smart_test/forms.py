from django.forms import BaseInlineFormSet, modelformset_factory, inlineformset_factory
from django.core.exceptions import ValidationError
from django import forms

from smart_test.models import Answer, Test, Question


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title', 'description', 'topic', 'level', 'image']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['order_number', 'text']


class AnswerForm(forms.ModelForm):
    is_selected = forms.BooleanField()

    class Meta:
        model = Answer
        fields = ['text', 'is_selected']


class QuestionsInlineFormSet(BaseInlineFormSet):

    def clean(self):
        if not (self.instance.QUESTION_MIN_LIMIT <= len(self.forms) <= self.instance.QUESTION_MAX_LIMIT):
            raise ValidationError(
                "Quantity of Question is out of range ({}..{})".format(self.instance.QUESTION_MIN_LIMIT,
                                                                       self.instance.QUESTION_MAX_LIMIT))


class AnswerInlineFormSet(BaseInlineFormSet):

    def clean(self):
        if not (self.instance.ANSWER_MIN_LIMIT <= len(self.forms) <= self.instance.ANSWER_MAX_LIMIT):
            raise ValidationError(
                "Quantity of Question is out of range ({}..{})".format(self.instance.ANSWER_MIN_LIMIT,
                                                                       self.instance.ANSWER_MAX_LIMIT))

        num_correct_answers = sum([
            1 for form in self.forms
            if form.cleaned_data["is_correct"]
        ])

        if num_correct_answers == 0:
            raise ValidationError("At LEAST one answer must be correct!")

        if num_correct_answers == len(self.forms):
            raise ValidationError("Not allowed to select ALL answers!")


AnswerFormSet = modelformset_factory(model=Answer, form=AnswerForm, extra=0)
QuestionFormSet = inlineformset_factory(Test, Question, form=QuestionForm, extra=1, can_delete=True)
# AnswerFormSet = inlineformset_factory(Question, Answer, form=AnswerForm, extra=1, can_delete=True)