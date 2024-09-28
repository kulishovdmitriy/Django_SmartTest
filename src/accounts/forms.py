from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

from accounts.models import User, Profile


class UserBaseForms(forms.ModelForm):
    """
        A base form class for the User model, inheriting from Django's ModelForm.

        This form includes fields for `first_name`, `last_name`, `email`, and `birth_date`.
        It leverages the default behaviors and validations provided by Django's ModelForm.

        Attributes:
        - model: Specifies the model associated with the form (User).
        - fields: List of field names to include in the form.
    """

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'birth_date']


class AccountCreateForm(UserCreationForm):
    """
    AccountCreateForm(UserCreationForm)
        A form for creating new accounts using the custom user model.

    Meta
        A nested class that provides metadata for the form.

        Attributes:
            model (User): Specifies the model to use for the form.
            fields (list): List of fields that will be used in the form.

    __init__(*args, **kwargs)
        Initializes a new instance of AccountCreateForm.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Deletes the 'usable_password' field from the form if it exists.
    """

    class Meta:
        model = User
        fields = ["username", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'usable_password' in self.fields:
            del self.fields['usable_password']


class AccountUpdateForm(UserChangeForm):
    """
    AccountUpdateForm is a subclass of UserChangeForm.
    It enables customized user account updates, specifically targeting the fields:
    'username', 'first_name', 'last_name', and 'email'.

    Meta:
        This inner Meta class inherits from UserChangeForm.Meta
        and defines the model fields to be included in the form.
    Fields:
        username: The username of the user.
        first_name: The first name of the user.
        last_name: The last name of the user.
        email: The email address of the user.
    """

    class Meta(UserChangeForm.Meta):
        fields = ["username", "first_name", "last_name", "email"]


class AccountProfileUpdateForm(ModelForm):
    """
        AccountProfileUpdateForm
        A Django form for updating user profile information.

        Meta:
            model (django.db.models.Model): The model associated with this form.
            fields (list): Specifies which fields to include in the form.
                           In this case, "image" and "interests" are included.
    """

    class Meta:
        model = Profile
        fields = ["image", "interests"]


class ContactUsForm(forms.Form):
    """
    A Django Form class to handle the "Contact Us" form data.

    This form captures the subject and message from the user,
    which can be processed or stored as needed.

    Attributes
    ----------
    subject: CharField
        The subject of the message, limited to 256 characters, with a default initial value.
    message: CharField
        The main text content of the message, displayed as a Textarea widget.

    Methods
    -------
    None
    """

    subject = forms.CharField(max_length=256, initial="Message from Smart_Test")
    message = forms.CharField(widget=forms.Textarea)
