from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

from accounts.models import User, Profile


class UserBaseForms(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'birth_date']


class AccountCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'usable_password' in self.fields:
            del self.fields['usable_password']


class AccountUpdateForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        fields = ["username", "first_name", "last_name", "email"]


class AccountProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["image", "interests"]
