from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, HttpResponse
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.db import transaction

from smart_test.forms import AnswerFormSet, TestForm, QuestionFormSet
from smart_test.models import Test, Question, TestResult
from smart_test.services import TestRunner
from smart_test.utils import test_result_for_user


# Create your views here.

class TestListView(ListView):
    model = Test
    template_name = 'list.html'
    context_object_name = 'tests'
    paginate_by = 10


class TestDetailView(LoginRequiredMixin, DetailView):
    model = Test
    template_name = 'details.html'
    context_object_name = 'test'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        test_id = self.kwargs['id']
        context['best_result'] = TestResult.best_result(test_id)
        context['last_run'] = TestResult.last_run(test_id)
        context['continue_flag'] = TestResult.objects.filter(
            user=self.request.user,
            state=TestResult.STATE.NEW,
            test=self.get_object(),
        ).count()

        return context


class TestStartView(LoginRequiredMixin, View):

    def get(self, request, id):
        try:
            test = Test.objects.get(id=id)
        except Test.DoesNotExist:
            return HttpResponse("Test not found", status=404)

        TestResult.objects.get_or_create(
            user=request.user,
            state=TestResult.STATE.NEW,
            test=test,
            defaults={
                'num_correct_answers': 0,
                'num_incorrect_answers': 0,
                'current_order_number': 1,
            }
        )

        return redirect(reverse('tests:next', args=(id, )))

    @staticmethod
    def on_next(context, test_result):
        request = context['request']
        if test_result.state == TestResult.STATE.NEW:
            return redirect(reverse('tests:next', args=(test_result.test.id,)))

        elif test_result.state == TestResult.STATE.FINISHED:
            return render(
                request=request,
                template_name='finish.html',
                context={
                    'test_result': test_result,
                    'test_result_score': (test_result.num_correct_answers / test_result.test.questions.count()) * 100
                }
            )

        return HttpResponse(f'Unexpected state {test_result.state}!', status=500)


class TestQuestionView(LoginRequiredMixin, View):

    def get(self, request, id):

        test_result = test_result_for_user(request.user, id)

        if test_result.count() == 0:
            return redirect(reverse('tests:details', args=(id,)))

        test_result = test_result.first()

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

        if test_result.count() == 0:
            return redirect(reverse('tests:details', args=(id,)))

        test_result = test_result.first()

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
            messages.error(request, extra_tags='danger', message='ERROR: You cant select ALL answer')
            return redirect(reverse('tests:next', args=(id, )))

        test_runner = TestRunner(
            on_next=TestStartView.on_next,
            test_result=test_result
        )

        result = test_runner.next(
            context={
                'request': request,
                'selected_choices': selected_choices
            }
        )

        return result


class TestCreateView(CreateView):
    model = Test
    form_class = TestForm
    template_name = 'test_form.html'
    success_url = '/tests/'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['questions'] = QuestionFormSet(self.request.POST)
        else:
            data['questions'] = QuestionFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        questions = context['questions']
        with transaction.atomic():
            response = super().form_valid(form)
            if questions.is_valid():
                questions.instance = self.object
                questions.save()
        return response


class TestUpdateView(UpdateView):
    model = Test
    form_class = TestForm
    template_name = 'test_form.html'
    success_url = '/tests/'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['questions'] = QuestionFormSet(self.request.POST, instance=self.object)
        else:
            data['questions'] = QuestionFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        questions = context['questions']
        with transaction.atomic():
            response = super().form_valid(form)
            if questions.is_valid():
                questions.instance = self.object
                questions.save()
        return response
