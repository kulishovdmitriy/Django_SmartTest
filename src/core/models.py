from django.db import models

# Create your models here.


class BaseModel(models.Model):
    """
        BaseModel serves as an abstract base class for other Django models,
        providing common fields for tracking creation and update times.

        Meta:
            - abstract: Specify that this model is an abstract base class.

        Attributes:
            - create_date: A date-time field that records when the record was created.
              Automatically set the field to now when the object is first created.
            - write_date: A date-time field that updates itself to the current date and time every time the record is saved.
    """

    class Meta:
        abstract = True

    create_date = models.DateTimeField(null=True, auto_now_add=True)
    write_date = models.DateTimeField(null=True, auto_now=True)
