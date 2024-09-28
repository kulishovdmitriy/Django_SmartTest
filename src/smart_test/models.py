import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from accounts.models import User
from core.models import BaseModel


# Create your models here.


class Topic(models.Model):
    """
        Topic model represents a topic entity with a name attribute.

        Attributes:
            name (str): The name of the topic, with a maximum length of 128 characters.

        Methods:
            __str__(self):
                Returns the string representation of the Topic instance, which is the name of the topic.
    """

    name = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.name}"


class Test(models.Model):
    """
        Test model represents a collection of information regarding a particular test entity. This model is part of the Django application
        and includes details such as title, description, level, and an associated image.

        Attributes:
            QUESTION_MIN_LIMIT (int): Minimum number of questions allowed in the test.
            QUESTION_MAX_LIMIT (int): Maximum number of questions allowed in the test.

            LEVEL_CHOICES (class): A class to define level choices for the test.
                BASIC (int): Represents the basic level.
                MIDDLE (int): Represents the middle level.
                ADVANCED (int): Represents the advanced level.

            topic (ForeignKey): A foreign key relationship to the Topic model.
            title (CharField): Title of the test, with a maximum length of 128 characters.
            description (TextField): Description of the test, with a maximum length of 1024 characters.
            level (PositiveSmallIntegerField): Level of the test, selected from LEVEL_CHOICES.
            image (ImageField): An image associated with the test, with a default image if not provided.

        Methods:
            __str__: Returns the title of the test as its string representation.

        Meta:
            ordering (list): Specifies default ordering of test objects by title.
    """

    QUESTION_MIN_LIMIT = 3
    QUESTION_MAX_LIMIT = 20

    class LEVEL_CHOICES(models.IntegerChoices):
        """
            class LEVEL_CHOICES(models.IntegerChoices):
                A class to define the choices for different levels with integer values.

                Attributes
                ----------
                BASIC : int
                    Represents the basic level with a value of 0.
                MIDDLE : int
                    Represents the middle level with a value of 1.
                ADVANCED : int
                    Represents the advanced level with a value of 2.
        """

        BASIC = 0, "Basic"
        MIDDLE = 1, "Middle"
        ADVANCED = 2, "Advanced"

    topic = models.ForeignKey(to=Topic, related_name="tests", null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=128, null=True)
    description = models.TextField(max_length=1024, null=True, blank=True)
    level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES.choices, default=LEVEL_CHOICES.MIDDLE)
    image = models.ImageField(upload_to="covers/", default="covers/default.png")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        ordering = ['title']


class Question(models.Model):
    """
        A Django model representing a question within a test.

        Class-level constants:
        - ANSWER_MIN_LIMIT (int): Minimum number of answers allowed.
        - ANSWER_MAX_LIMIT (int): Maximum number of answers allowed.

        Fields:
        - test (ForeignKey): The associated test that this question belongs to.
        - order_number (PositiveSmallIntegerField): The question's order number in the test.
        - text (CharField): The text of the question.

        Methods:
        - __str__(self): Returns a string representation of the question text.
    """

    ANSWER_MIN_LIMIT = 3
    ANSWER_MAX_LIMIT = 6

    test = models.ForeignKey(to=Test, related_name="questions", on_delete=models.CASCADE)
    order_number = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(Test.QUESTION_MAX_LIMIT)])
    text = models.CharField(max_length=512, null=True)

    def __str__(self):
        return f"{self.text}"


class Answer(models.Model):
    """
        Represents an answer to a question in a quiz or survey application.

        Attributes:
        - question: ForeignKey linking the answer to a specific question.
        - text: A CharField to store the text of the answer.
        - is_correct: A BooleanField indicating whether the answer is correct.

        Methods:
        - __str__: Returns the text of the answer.
    """

    question = models.ForeignKey(to=Question, related_name="answers", on_delete=models.CASCADE)
    text = models.CharField(max_length=128, null=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text}"


class TestResult(BaseModel):
    """
        Represents the results of a user taking a test.

        Attributes
        ----------
        user : ForeignKey
            A reference to the user who took the test.
        test : ForeignKey
            A reference to the test that was taken.
        state : PositiveSmallIntegerField
            The state of the test result, indicating whether it is new or finished.
        num_correct_answers : PositiveSmallIntegerField
            The number of correct answers given by the user.
        num_incorrect_answers : PositiveSmallIntegerField
            The number of incorrect answers given by the user.
        current_order_number : PositiveSmallIntegerField
            The current order number of the question being answered, with validation.

        Methods
        -------
        time_spent()
            Calculates the total time spent on the test, excluding microseconds.
        points()
            Calculates the points obtained by the user, which is the number of correct answers minus incorrect answers.
        score()
            Calculates the score as a percentage of correct answers out of the total questions in the test.
        __str__()
            Returns a string representation of the test result, including the test, user, and write date.
        best_result(test_id)
            Returns the best result for a given test ID, including user information and points scored.
        last_run(test_id)
            Returns the write date of the most recent run for a given test ID, or a message if not yet run.
    """

    class STATE(models.IntegerChoices):
        """
            Represents the state of an object with two possible choices for status.

            Attributes:
                NEW (int): Indicates that the object is in a new state.
                FINISHED (int): Indicates that the object is in a finished state.
        """

        NEW = 0, "New"
        FINISHED = 1, "Finished"

    user = models.ForeignKey(to=User, related_name="test_results", on_delete=models.CASCADE)
    test = models.ForeignKey(to=Test, related_name="test_results", on_delete=models.CASCADE)
    state = models.PositiveSmallIntegerField(default=STATE.NEW, choices=STATE.choices)

    num_correct_answers = models.PositiveSmallIntegerField(default=0,
                                                           validators=[MaxValueValidator(Test.QUESTION_MAX_LIMIT)])
    num_incorrect_answers = models.PositiveSmallIntegerField(default=0,
                                                             validators=[MaxValueValidator(Test.QUESTION_MAX_LIMIT)])

    current_order_number = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(Test.QUESTION_MAX_LIMIT)])

    def time_spent(self):
        """
            Calculate the time spent from the object's creation date to its write date.

            :return: Time spent as a timedelta object, with microseconds removed.
        """

        time_spent = self.write_date - self.create_date
        return time_spent - datetime.timedelta(microseconds=time_spent.microseconds)

    def points(self):
        """
            :return: The calculated points of the user, which is the number of correct answers minus the number of incorrect answers.
            The result is never less than zero.
        """

        return max(0, self.num_correct_answers - self.num_incorrect_answers)

    def score(self):
        """
         :return: The score as a percentage, calculated from the number of correct answers divided by the total number of questions in the test.
        """

        return (self.num_correct_answers/self.test.questions.count())*100

    def __str__(self):
        return f"{self.test}, run by {self.user.get_full_name()} at {self.write_date}"

    @staticmethod
    def best_result(test_id):
        """
            :param test_id: The identifier of the test for which the best result is sought.
            :return: A string representing the user with the highest score and their points, or a message indicating that no one has completed the test.
        """

        queryset = TestResult.objects.filter(test=test_id)
        if queryset.count() > 0:
            obj = queryset.extra(select={
                'points': 'num_correct_answers - num_incorrect_answers', 'duration': 'write_date - create_date'},
                order_by=['-points', 'duration'])[0]
            result = f'{obj.user} scored {obj.num_correct_answers} points'
            return result
        else:
            result = 'No one has done this test yet'
            return result

    @staticmethod
    def last_run(test_id):
        """
            :param test_id: The identifier for the test whose last run date is to be fetched.
            :return: The date of the last run of the specified test if it exists, otherwise a message stating no runs.
        """

        if TestResult.objects.filter(test=test_id).count() > 0:
            ob = TestResult.objects.filter(test=test_id).order_by('-write_date').first()
            result = ob.write_date
            return result
        else:
            result = 'No one has run this test yet'
            return result
