import logging

from smart_test.models import TestResult, Question


logger = logging.getLogger('smart_test')


class TestRunner:
    """
        Class to manage the execution flow of a test, including transitioning
        between different states of the test and handling the scoring.

        :param test_result: The current result state of the test.
        :type test_result: TestResult
        :param on_next: Optional function to call after handling the current state.
        :type on_next: callable, optional
    """

    def __init__(self, test_result, on_next=None):
        self.test_result = test_result
        self.on_next = on_next
        self.points = 0

    def next(self, context):
        """
            :param context: The context in which the method is being called. This may include various runtime information necessary for processing.
            :return: The result of the on_next method if it is defined, otherwise None.
        """

        logger.info('Метод next вызван')
        if self.test_result.state == TestResult.STATE.NEW:
            self.on_new(context)
        elif self.test_result.state == TestResult.STATE.FINISHED:
            self.on_finish(context)
        if self.on_next:
            logger.info('Вызов on_next')
            return self.on_next(context, self.test_result)

    def on_new(self, context):
        """
            :param context: Dictionary containing the user's selected choices for the current question.
            :return: Updates the test result metrics based on the user's answers. Finishes the test if all questions are answered,
            otherwise moves to the next question.
        """

        selected_choices = context['selected_choices']
        question = Question.objects.get(
            test=self.test_result.test,
            order_number=self.test_result.current_order_number
        )

        answers = question.answers.all()

        current_choices = sum(
            answer.is_correct == choice
            for answer, choice in zip(answers, selected_choices)
        )

        self.points = int(current_choices == len(answers))

        self.test_result.num_correct_answers += self.points
        self.test_result.num_incorrect_answers += (1 - self.points)

        if self.test_result.current_order_number == self.test_result.test.questions.count():
            self.test_result.state = TestResult.STATE.FINISHED

        else:
            self.test_result.current_order_number += 1

        self.test_result.save()

    def on_finish(self, context):
        """
            :param context: The context object containing information about the execution state.
            :return: None
        """

        self.test_result.state = TestResult.STATE.FINISHED
        self.test_result.save()
