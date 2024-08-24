import logging

from smart_test.models import TestResult, Question


logger = logging.getLogger('smart_test')


class TestRunner:

    def __init__(self, test_result, on_next=None):
        self.test_result = test_result
        self.on_next = on_next
        self.points = 0

    def next(self, context):

        logger.info('Метод next вызван')
        if self.test_result.state == TestResult.STATE.NEW:
            self.on_new(context)
        elif self.test_result.state == TestResult.STATE.FINISHED:
            self.on_finish(context)
        if self.on_next:
            logger.info('Вызов on_next')
            return self.on_next(context, self.test_result)

    def on_new(self, context):

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
        self.test_result.state = TestResult.STATE.FINISHED
        self.test_result.save()
