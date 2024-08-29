from django.test import TestCase

from accounts.models import User
from smart_test.models import TestResult, Test
from smart_test.services import TestRunner


def on_next_callback(contex, test_result):
    result = False

    if test_result.state == TestResult.STATE.NEW:
        result = test_result.state

    elif test_result.state == TestResult.STATE.FINISHED:
        result = test_result.state

    return result


class TestResultModelTests(TestCase):

    fixtures = [
        'dump.json'
    ]

    def setUp(self):
        self.test = Test.objects.first()

    def test_points(self):
        for test_result in self.test.test_results.all():
            self.assertEqual(test_result.points() <= 100, True)

    def test_score(self):
        for test_result in self.test.test_results.all():
            self.assertEqual(test_result.score() <= 100, True)


class TestResultModelServicesTests(TestCase):

    fixtures = [
        'dump.json'
    ]

    def setUp(self):
        self.test = Test.objects.first()
        self.user = User.objects.first()

    def test_basic_flow(self):

        test_result, _ = TestResult.objects.get_or_create(
            user=self.user,
            state=TestResult.STATE.NEW,
            test=self.test,
            defaults=dict(
                num_correct_answers=0,
                num_incorrect_answers=0,
                current_order_number=1
            )
        )

        test_runner = TestRunner(
            on_next=on_next_callback,
            test_result=test_result
        )

        result = None
        for question in self.test.questions.all():
            selected_choices = [
                True
                for _ in question.answers.all()
            ]

            result = test_runner.next(
                context={
                    'selected_choices': selected_choices
                }
            )

        self.assertEqual(result, TestResult.STATE.FINISHED)

    def test_success_flow(self):

        test_result, _ = TestResult.objects.get_or_create(
            user=self.user,
            state=TestResult.STATE.NEW,
            test=self.test,
            defaults=dict(
                num_correct_answers=0,
                num_incorrect_answers=0,
                current_order_number=1
            )
        )

        test_runner = TestRunner(
            on_next=on_next_callback,
            test_result=test_result
        )

        result = None
        for question in self.test.questions.all():
            selected_choices = [
                answer.is_correct
                for answer in question.answers.all()
            ]

            result = test_runner.next(
                context={
                    'selected_choices': selected_choices
                }
            )

        self.assertEqual(result, TestResult.STATE.FINISHED)
        self.assertEqual(test_result.score(), 100)
        self.assertEqual(test_result.points(), self.test.questions.count())
