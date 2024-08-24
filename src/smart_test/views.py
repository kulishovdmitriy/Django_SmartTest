from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from smart_test.forms import AnswerFormSet
from smart_test.models import Test, Question, TestResult
from smart_test.utils import test_result_for_user


# Create your views here.

class TestListView(ListView):
    model = Test
    template_name = 'list.html'
    context_object_name = 'tests'
    paginate_by = 10


class TestDetailView(DetailView):
    model = Test
    template_name = 'details.html'
    context_object_name = 'test'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['continue_flag'] = TestResult.objects.filter(
            user=self.request.user,
            state=TestResult.STATE.NEW,
            test=self.get_object(),
        ).count()

        return context


class TestStartView(LoginRequiredMixin, View):

    def get(self, request, id):

        current_user_tests = TestResult.objects.filter(
            user=request.user,
            state=TestResult.STATE.NEW,
            test=Test.objects.get(id=id)
        )

        if current_user_tests.count() == 0:
            TestResult.objects.create(
                user=request.user,
                state=TestResult.STATE.NEW,
                test=Test.objects.get(id=id),
                num_correct_answers=0,
                num_incorrect_answers=0,
                current_order_number=1,
            )

        return redirect(reverse('tests:next', args=(id, )))


class TestQuestionView(LoginRequiredMixin, View):

    def get(self, request, id):

        test_result = test_result_for_user(request.user, id)

        order_number = test_result.current_order_number

        question = Question.objects.get(test__id=id, order_number=order_number)
        answers = question.answers.all()

        form_set = AnswerFormSet(queryset=answers)

        return render(
            request=request,
            template_name='question.html',
            context={
                'question': question,
                'form_set': form_set,
            }
        )

    def post(self, request, id):

        test_result = test_result_for_user(request.user, id)

        order_number = test_result.current_order_number

        question = Question.objects.get(test__id=id, order_number=order_number)
        answer = question.answers.all()

        form_set = AnswerFormSet(data=request.POST)

        possible_choices = len(form_set.forms)
        selected_choices = [
            'is_selected' in form.changed_data
            for form in form_set.forms
        ]

        num_selected_choices = sum(selected_choices)

        if num_selected_choices == 0:
            messages.error(request, extra_tags='danger', message='ERROR: You should select at least 1 answer')
            return redirect(reverse('tests:next', args=(id, )))

        if num_selected_choices == possible_choices:
            messages.error(request, extra_tags='danger', message='ERROR: You can`t select ALL answer')
            return redirect(reverse('tests:next', args=(id, )))

        current_choices = sum(
            answer.is_correct == choice
            for answer, choice in zip(answer, selected_choices)
        )

        point = int(current_choices == possible_choices)

        test_result = TestResult.objects.get(
            user=request.user,
            test=question.test,
            state=TestResult.STATE.NEW
        )

        test_result.num_correct_answers += point
        test_result.num_incorrect_answers += (1 - point)
        test_result.current_order_number += 1
        test_result.save()

        if order_number == question.test.questions.count():
            test_result.state = TestResult.STATE.FINISHED
            test_result.save()

            return render(
                request=request,
                template_name='finish.html',
                context={
                    'test_result': test_result,
                    'test_result_score': (test_result.num_correct_answers/test_result.test.questions.count()) * 100
                }
            )

        return redirect(reverse('tests:next', args=(id, )))
