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

    score = models.DecimalField(default=0.0, decimal_places=2, max_digits=5,
                                validators=[MinValueValidator(0), MaxValueValidator(100)])

    num_correct_answers = models.PositiveSmallIntegerField(default=0,
                                                           validators=[MaxValueValidator(Question.ANSWER_MAX_LIMIT)])
    num_incorrect_answers = models.PositiveSmallIntegerField(default=0,
                                                             validators=[MaxValueValidator(Question.ANSWER_MAX_LIMIT)])

    def __str__(self):
        return f"{self.test}, run by {self.user.full_name()} at {self.write_date}"
