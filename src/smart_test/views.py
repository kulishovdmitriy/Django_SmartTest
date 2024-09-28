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
    """
        A view for displaying a list of Test objects.

        Attributes:
            model (Test): Specifies the model to use for the list view.
            template_name (str): The template to use for rendering the list.
            context_object_name (str): The context variable name for the list of objects.
            paginate_by (int): The number of items to display per page.
    """

    model = Test
    template_name = 'list.html'
    context_object_name = 'tests'
    paginate_by = 10


class TestDetailView(LoginRequiredMixin, DetailView):
    """
        TestDetailView is a view that displays the details of a Test instance.
        This view requires the user to be logged in and provides a context
        containing the best result, the last run, and a continue flag based
        on the current user and test state.

        Attributes:
            model: The model that this view will be displaying.
            template_name: The name of the template to use for rendering the view.
            context_object_name: The name of the context variable to use for the object being displayed.
            pk_url_kwarg: The URL keyword argument that will be used to retrieve the primary key of the model instance.

        Methods:
            get_context_data(self, **kwargs):
                Adds additional context to the template, including the best result,
                the last run, and a continue flag based on the current user and test state.
    """

    model = Test
    template_name = 'details.html'
    context_object_name = 'test'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        """
            :param kwargs: Additional keyword arguments passed to the method.
            :return: A context dictionary containing the best test result, the last run of the test, and the count of new test results for the current user.
        """

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
    """
        A view responsible for starting a test and managing test result logic.

        This view requires the user to be logged in and provides functionality to
        initialize a new test result, redirect users through the test process, and
        handle the completed state of a test.

        Methods:
            get(request, id):
                Retrieves the specified test by id and initializes a new test result
                for the logged-in user, then redirects to the next segment of the test.

            on_next(context, test_result):
                Redirects the user to the next part of the test based on the current
                state of the test result, or renders the final score upon completion.
    """

    def get(self, request, id):
        """
            :param request: The HTTP request object containing metadata about the request and the user performing the action.
            :param id: The unique identifier for the Test object being accessed.
            :return: An HTTP response that redirects to the 'next' view in the 'tests' app if successful, or an HTTP 404 response
            if the Test object is not found.
        """

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
        """
            :param context: A dictionary containing the context of the current request. Expected to have a key 'request' with
            the value being the current HTTP request object.
            :param test_result: An instance of TestResult that contains information about the current test's state, number of
            correct answers, and associated test details.
            :return: Depending on the state of the test_result, returns an appropriate HTTP response. It could be a redirection
            to the next test question, rendering the finish page, or an error response for unexpected states.
        """

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
    """
        class:: TestQuestionView

           The TestQuestionView class handles GET and POST requests related to a specific test's question for a user.

           The view requires the user to be logged in and handles retrieving test questions, submitting answers, and validating user input.

           method:: get(self, request, id)

              Handles the retrieval of a test question for the user.

              :param request: The HTTP request object.
              :param id: The ID of the test.
              :returns: An HTTP redirect to the test details page if no result for the user, else renders the question page.

           method:: post(self, request, id)

              Handles the submission and validation of a test question's answers.

              :param request: The HTTP request object.
              :param id: The ID of the test.
              :returns: An HTTP redirect to the next question page, with error messages if the validation fails, else proceeds to the next test step.
    """

    def get(self, request, id):
        """
            :param request: The HTTP request object
            :param id: The ID of the specific test
            :return: An HTTP response, redirecting to the test details if no results are found or rendering the question page with its answers otherwise
        """

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
        """
            :param request: The HTTP request object containing metadata about the request.
            :param id: The identifier for the test instance being accessed.
            :return: Redirects to different views based on the test results and selected choices.
        """

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


class TestCreateView(LoginRequiredMixin, CreateView):
    """
        TestCreateView is a Django class-based view for creating Test instances.

        Attributes:
            model: Specifies the model class to use for the view.
            form_class: Specifies the form class to use for the view.
            template_name: The path to the template to render this view.
            success_url: URL to redirect to upon successful form submission.

        Methods:
            get_context_data(**kwargs):
                Adds the 'questions' formset to the context data. Handles both
                GET and POST requests to populate the formset appropriately.

            form_valid(form):
                Handles the form submission when the form is valid. It uses a
                database transaction to save the Test instance and associated
                Question formset data.
    """

    model = Test
    form_class = TestForm
    template_name = 'test_form.html'
    success_url = '/tests/'

    def get_context_data(self, **kwargs):
        """
             :param kwargs: Arbitrary keyword arguments passed from the view.
            :return: Context data dictionary with added 'questions' key containing a QuestionFormSet instance. The instance
            is populated with POST data if present, otherwise it is empty.
        """

        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['questions'] = QuestionFormSet(self.request.POST)
        else:
            data['questions'] = QuestionFormSet()
        return data

    def form_valid(self, form):
        """
            :param form: The form instance that contains the validated data.
            :return: An HTTP response object after processing the form and saving related questions data within an atomic transaction.
        """

        context = self.get_context_data()
        questions = context['questions']
        with transaction.atomic():
            response = super().form_valid(form)
            if questions.is_valid():
                questions.instance = self.object
                questions.save()
        return response


class TestUpdateView(LoginRequiredMixin, UpdateView):
    """
        Class TestUpdateView

        A Django view for updating Test instances that requires the user to be logged in.
        Inherits from LoginRequiredMixin and UpdateView.

        Attributes:
            model: References the Test model.
            form_class: Uses the TestForm for the form.
            template_name: Specifies the template used for rendering the form.
            success_url: Redirects to this URL upon successful form submission.
            pk_url_kwarg: Keyword argument for the primary key in the URL.

        Methods:
            get_context_data(**kwargs):
                Extends the context data with a QuestionFormSet. If POST data is present, initializes with POST data; otherwise,
                initializes with the instance data.
            form_valid(form):
                Handles a valid form submission. Saves related QuestionFormSet data in an atomic transaction.
    """

    model = Test
    form_class = TestForm
    template_name = 'test_form.html'
    success_url = '/tests/'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        """
            :param kwargs: Additional keyword arguments passed to the method.
            :return: Context data dictionary containing formset for questions. If the request method is POST, formset is initialized
            with POST data, otherwise it is initialized with an instance of the object.
        """

        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['questions'] = QuestionFormSet(self.request.POST, instance=self.object)
        else:
            data['questions'] = QuestionFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        """
            :param form: The form instance that has been validated.
            :return: An HTTP response object resulting from a successful form submission.
        """
        context = self.get_context_data()
        questions = context['questions']
        with transaction.atomic():
            response = super().form_valid(form)
            if questions.is_valid():
                questions.instance = self.object
                questions.save()
        return response
