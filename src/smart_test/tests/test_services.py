from django.test import TestCase

from accounts.models import User
from smart_test.models import TestResult, Test
from smart_test.services import TestRunner


def on_next_callback(contex, test_result):
    """
        :param contex: The context in which the callback is executed.
        :param test_result: The result of the test that includes its state.
        :return: The state of the test if it is either NEW or FINISHED, otherwise False.
    """

    result = False

    if test_result.state == TestResult.STATE.NEW:
        result = test_result.state

    elif test_result.state == TestResult.STATE.FINISHED:
        result = test_result.state

    return result


class TestResultModelTests(TestCase):
    """
        This is a suite of unit tests for the `TestResultModel`.

        fixtures
            List of fixture file names that provide initial data for the tests.

        setUp
            Initializes an instance variable `self.test` with the first `Test` object from the database.

        test_points
            Asserts that the `points` method of all `TestResult` objects related to `self.test` returns a value less than or equal to 100.

        test_score
            Asserts that the `score` method of all `TestResult` objects related to `self.test` returns a value less than or equal to 100.
    """

    fixtures = [
        'dump.json'
    ]

    def setUp(self):
        """
            Sets up the initial conditions for the test case by assigning the first Test object to the instance variable.

            :return: None
        """

        self.test = Test.objects.first()

    def test_points(self):
        """
            Checks if all test results' points are less than or equal to 100.

            :return: None
        """

        for test_result in self.test.test_results.all():
            self.assertEqual(test_result.points() <= 100, True)

    def test_score(self):
        """
            Validates that the score for each test result is less than or equal to 100.

            :return: None
        """

        for test_result in self.test.test_results.all():
            self.assertEqual(test_result.score() <= 100, True)


class TestResultModelServicesTests(TestCase):
    """
        TestResultModelServicesTests is a test case class designed to verify the functionality of the TestResult and TestRunner components.

        fixtures:
            Specifies the initial data to load from 'dump.json' to the database before test cases are executed.

        setUp:
            Sets up the initial test environment for each test case by retrieving the first Test and User instances from the database.

        test_basic_flow:
            Validates the basic flow of processing a test with the TestRunner. It creates or retrieves a TestResult instance in a NEW state,
            iterates through all questions and simulates answering them with selected choices. It asserts that the final state of the test is FINISHED.

        test_success_flow:
            Validates the success flow of a test where every selected choice is correct. It creates or retrieves a TestResult instance in a NEW state,
            iterates through all questions and simulates answering them correctly. It asserts that the final test state is FINISHED, the score is 100,
             and the total points equal the number of questions.
    """

    fixtures = [
        'dump.json'
    ]

    def setUp(self):
        """
            Sets up initial test and user objects for the test case.

            :return: None
        """

        self.test = Test.objects.first()
        self.user = User.objects.first()

    def test_basic_flow(self):
        """
            Handles the basic flow of a test by initializing a test result if it doesn't exist, creating a TestRunner instance,
            iterating through all questions, selecting all choices for each question, and advancing to the next question using the runner.
            Finally, asserts if the test result state is FINISHED.

            :return: None
        """

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
        """
            Executes the success flow for a test, where a test is run and evaluated. The function:

            - Retrieves or creates a `TestResult` instance associated with the test and user.
            - Initializes a `TestRunner` with the test result and a callback for the `on_next` event.
            - Iterates through all questions in the test.
            - For each question, simulates selecting the correct answers.
            - Advances the test runner to the next question until all questions are answered.
            - Asserts that the test result state transitions to `FINISHED`.
            - Asserts that the test score is 100%.
            - Asserts that the points accumulated equals the number of questions in the test.

            :return: None
        """

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
