import logging
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic.edit import ProcessFormView, FormView
from django.core.mail import send_mail
from django.conf import settings

from accounts.forms import AccountCreateForm, AccountUpdateForm, AccountProfileUpdateForm, ContactUsForm
from accounts.models import User


# Create your views here.

logger = logging.getLogger('accounts')

class UserListView(ListView):

    model = User
    template_name = "user_list.html"
    context_object_name = "users"
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        request = self.request
        params = {
            "first_name": "__icontains",
            "last_name": "__icontains",
            "email": "__icontains",

            "birth_date": "",
        }
        for param, lookup in params.items():
            value = request.GET.get(param)
            if value:
                if lookup:
                    qs = qs.filter(**{f"{param}{lookup}": value})
                else:
                    qs = qs.filter(**{param: value})

        return qs


class AccountCreateView(CreateView):

    model = User
    template_name = "registration.html"
    form_class = AccountCreateForm
    success_url = reverse_lazy("accounts:login")


class AccountLoginView(LoginView):

    template_name = "login.html"

    def get_redirect_url(self):
        if self.request.GET.get("next"):
            return self.request.GET.get("next")
        return reverse("core:index")

    def form_valid(self, form):
        result = super().form_valid(form)
        messages.info(self.request, f'User {self.request.user} has been successfully logged in')
        return result


class AccountLogoutView(LogoutView):

    template_name = "logout.html"


class AccountUpdateView(LoginRequiredMixin, ProcessFormView):

    def get(self, request, *args, **kwargs):

        user = self.request.user
        profile = self.request.user.profile

        user_form = AccountUpdateForm(instance=user)
        profile_form = AccountProfileUpdateForm(instance=profile)

        return render(
            request,
            "profile.html",
            {
                "user_form": user_form,
                "profile_form": profile_form,
            }
        )

    def post(self, request, *args, **kwargs):

        user = self.request.user
        profile = self.request.user.profile

        user_form = AccountUpdateForm(data=request.POST, instance=user)
        profile_form = AccountProfileUpdateForm(data=request.POST, files=request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(reverse("accounts:profile"))

        return render(
            request,
            "profile.html",
            {
                "user_form": user_form,
                "profile_form": profile_form,
            }
        )


class ContactUsView(LoginRequiredMixin, FormView):
    template_name = "contact_us.html"
    extra_content = {"title": "Send us a message!"}
    success_url = reverse_lazy("core:index")
    form_class = ContactUsForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            try:
                logger.info("Email sent")
                send_mail(
                    subject=form.cleaned_data["subject"],
                    message=form.cleaned_data["message"],
                    from_email=request.user.email,
                    recipient_list=[settings.EMAIL_HOST_RECIPIENT],
                    fail_silently=False,
                )
                logger.info(f"Email sent successfully to {settings.EMAIL_HOST_RECIPIENT} from {request.user.email}")
            except Exception as e:
                logger.error(f"Error sending email: {e}")
            return self.form_valid(form)
        else:
            return self.form_invalid(form)