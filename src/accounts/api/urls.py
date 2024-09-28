from django.urls import path

from accounts.api.views import RegistrationView, AccountView


app_name = 'api_registration'

urlpatterns = [
    path('registrations', RegistrationView.as_view(), name='registration'),
    path('users', AccountView.as_view(), name='accounts_list'),
]
