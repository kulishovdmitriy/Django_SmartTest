from django import forms

from accounts.models import User


class UserBaseForms(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'birthdate']
