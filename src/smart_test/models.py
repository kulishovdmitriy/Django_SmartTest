import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from accounts.models import User
from core.models import BaseModel


# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.name}"


class Test(models.Model):
    QUESTION_MIN_LIMIT = 3
    QUESTION_MAX_LIMIT = 20

    class LEVEL_CHOICES(models.IntegerChoices):
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
    ANSWER_MIN_LIMIT = 3
    ANSWER_MAX_LIMIT = 6

    test = models.ForeignKey(to=Test, related_name="questions", on_delete=models.CASCADE)
    order_number = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(Test.QUESTION_MAX_LIMIT)])
    text = models.CharField(max_length=512, null=True)

    def __str__(self):
        return f"{self.text}"


class Answer(models.Model):
    question = models.ForeignKey(to=Question, related_name="answers", on_delete=models.CASCADE)
    text = models.CharField(max_length=128, null=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text}"


class TestResult(BaseModel):
    class STATE(models.IntegerChoices):
        NEW = 0, "New"
        FINISHED = 1, "Finished"

    user = models.ForeignKey(to=User, related_name="test_results", on_delete=models.CASCADE)
    test = models.ForeignKey(to=Test, related_name="test_results", on_delete=models.CASCADE)
    state = models.PositiveSmallIntegerField(default=STATE.NEW, choices=STATE.choices)

    num_correct_answers = models.PositiveSmallIntegerField(default=0,
                                                           validators=[MaxValueValidator(Question.ANSWER_MAX_LIMIT)])
    num_incorrect_answers = models.PositiveSmallIntegerField(default=0,
                                                             validators=[MaxValueValidator(Question.ANSWER_MAX_LIMIT)])

    current_order_number = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(Test.QUESTION_MAX_LIMIT)])

    def time_spent(self):
        time_spent = self.write_date - self.create_date
        return time_spent - datetime.timedelta(microseconds=time_spent.microseconds)

    # def point(self):
    #     return max(0, self.num_correct_answers - self.num_incorrect_answers)

    def __str__(self):
        return f"{self.test}, run by {self.user.get_full_name()} at {self.write_date}"
