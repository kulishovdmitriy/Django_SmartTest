from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.


class User(AbstractUser):
    """
        A custom user model that extends Django's AbstractUser.

        Attributes:
        -----------
        school : str
            The name of the school associated with the user. This field is optional and can be left blank.

        user_class : str
            The class or grade of the user. This field is optional and can be left blank.

        phone : str
            The phone number of the user. This field is optional and can be left blank.

        birth_date : datetime.date
            The birth date of the user. This field is optional and can be left blank.

        rating : decimal.Decimal
            The rating of the user. Default value is 0.0. The rating has a maximum of 5 digits, with 2 decimal places,
            and is validated to ensure it is between 0 and 100.
    """

    school = models.CharField(max_length=255, blank=True)
    user_class = models.CharField(max_length=10, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    rating = models.DecimalField(default=0.0, decimal_places=2, max_digits=5,
                                 validators=[MinValueValidator(0), MaxValueValidator(100)])


class UserAction(models.Model):
    """
        UserAction model represents a record of activities performed by a user in the system.

        USER_ACTION is an enumeration of possible actions a user can perform:

        - LOGIN: User logs into the platform.
        - LOGOUT: User logs out of the platform.
        - CHANGE_PASSWORD: User changes their password.
        - CHANGE_PROFILE: User updates their profile information.
        - CHANGE_PROFILE_IMAGE: User changes their profile image.

        Attributes:
        - user (ForeignKey): Reference to the User who performed the action. On deletion of the user, the action is also deleted.
        - write_date (DateTimeField): The date and time when the action was performed. Automatically set to the current date and
        time when a new record is created.
        - action (PositiveSmallIntegerField): The type of action performed by the user, represented by values from the USER_ACTION enumeration.
        - info (CharField): Additional information about the action, optional and can have a maximum length of 128 characters.
    """

    class USER_ACTION(models.IntegerChoices):
        LOGIN = 0, "Login"
        LOGOUT = 1, "Logout"
        CHANGE_PASSWORD = 2, "Change Password"
        CHANGE_PROFILE = 3, "Change Profile"
        CHANGE_PROFILE_IMAGE = 4, "Change Profile image"

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    write_date = models.DateTimeField(auto_now_add=True)
    action = models.PositiveSmallIntegerField(choices=USER_ACTION.choices)
    info = models.CharField(max_length=128, null=True)


class Profile(models.Model):
    """
        This class defines a Profile model that extends Django's base Model class.
        It associates additional information with a user, including an image and a list of interests.

        Attributes:
            user (OneToOneField): A one-to-one relationship to the User model, which ensures that each user
                                  has only one associated profile. The profile is deleted if the user is
                                  removed.
            image (ImageField): An optional image associated with the user profile. If no image is provided,
                                a default image ('pictures/default.jpg') is used. The images are uploaded to
                                the 'pictures/' directory.
            interests (CharField): An optional text field to store the user's interests, with a maximum length
                                   of 128 characters.
    """

    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(null=True, default='pictures/default.jpg', upload_to='pictures/')
    interests = models.CharField(max_length=128, null=True)
