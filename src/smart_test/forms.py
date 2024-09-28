from django.forms import BaseInlineFormSet, modelformset_factory, inlineformset_factory
from django.core.exceptions import ValidationError
from django import forms

from smart_test.models import Answer, Test, Question


class TestForm(forms.ModelForm):
    """
        TestForm class for handling the Test model form.

        This class provides a form for the Test model and includes the following fields:
        - title
        - description
        - topic
        - level
        - image
    """

    class Meta:
        model = Test
        fields = ['title', 'description', 'topic', 'level', 'image']


class QuestionForm(forms.ModelForm):
    """
        QuestionForm is a ModelForm representing the Question model. It provides form fields corresponding to the model's `order_number` and `text` attributes.

        Attributes:
            model (class): The model associated with this form, here the `Question` model.
            fields (list): The list of fields from the model to include in the form. In this case, ['order_number', 'text'].
    """

    class Meta:
        model = Question
        fields = ['order_number', 'text']


class AnswerForm(forms.ModelForm):
    """
        A Django form for creating or updating an Answer instance.

        This form includes a BooleanField named 'is_selected' that can be used
        to mark the answer as selected or not selected.

        Attributes:
            is_selected (BooleanField): A checkbox field indicating if the answer
            is selected.

        Meta:
            model (Answer): The model associated with this form.
            fields (list): A list of fields to include in the form. In this case,
            'text' and 'is_selected'.
    """

    is_selected = forms.BooleanField()

    class Meta:
        model = Answer
        fields = ['text', 'is_selected']


class QuestionsInlineFormSet(BaseInlineFormSet):
    """
        A custom formset class that ensures the number of question forms within specified limits.

        Attributes:
            BaseInlineFormSet: The parent class that this custom formset inherits from.

        Methods:
            clean:
                Validates the number of question forms against the minimum and maximum limits defined
                by the instance's `QUESTION_MIN_LIMIT` and `QUESTION_MAX_LIMIT` attributes. Raises a
                `ValidationError` if the number of forms is not within this range.
    """

    def clean(self):
        if not (self.instance.QUESTION_MIN_LIMIT <= len(self.forms) <= self.instance.QUESTION_MAX_LIMIT):
            raise ValidationError(
                "Quantity of Question is out of range ({}..{})".format(self.instance.QUESTION_MIN_LIMIT,
                                                                       self.instance.QUESTION_MAX_LIMIT))


class AnswerInlineFormSet(BaseInlineFormSet):
    """
        BaseInlineFormSet subclass for managing and validating a set of Answer forms within a Question form.

        Methods:
            clean: Validates the quantity of answers and the correctness of at least one and not all answers.
    """

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
