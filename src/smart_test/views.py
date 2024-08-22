from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView
from django.forms import modelformset_factory

from smart_test.forms import AnswerForm
from smart_test.models import Test, Question, Answer


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


class TestStartView(View):

    def get(self, request, id):
        # if 'current_test' not in request.session:
        #     context = {
        #         'test_id': test_id,
        #         'order_number': 1,
        #         'num_correct_answer': 0,
        #         'num_incorrect_answer': 0
        #     }
        #     request.session['current_test'] = context
        #
        # context = request.session['current_test']
        # order_number = context['order_number']
        return redirect(reverse('tests:question', args=(id, 1)))


class TestQuestionView(View):

    def get(self, request, id, order_number):

        question = Question.objects.get(test__id=id, order_number=order_number)
        answers = question.answers.all()

        answer_form_set = modelformset_factory(model=Answer, form=AnswerForm, extra=0)

        form_set = answer_form_set(queryset=answers)

        return render(
            request=request,
            template_name='question.html',
            context={
                'question': question,
                'form_set': form_set,
            }
        )

    def post(self, request, id, order_number):
        pass