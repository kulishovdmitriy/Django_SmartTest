import logging
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic.edit import ProcessFormView, FormView
from django.conf import settings

from accounts.forms import AccountCreateForm, AccountUpdateForm, AccountProfileUpdateForm, ContactUsForm
from accounts.models import User
from accounts.tasks import send_contact_email


# Create your views here.

logger = logging.getLogger('accounts')


class AccountsListView(LoginRequiredMixin, ListView):
    """
        AccountsListView class displays a paginated list of user accounts filtered by query parameters.

        Inherits from:
            LoginRequiredMixin: Ensures the viewer is authenticated.
            ListView: Provides a generic view for displaying a list of objects.

        Attributes:
            model (User): The model to retrieve data from.
            template_name (str): The name of the template to render.
            context_object_name (str): The context name to use for the list of objects.
            paginate_by (int): The number of objects per page.

        Methods:
            get_queryset:
                Filters the user list based on query parameters: 'first_name', 'last_name', 'email', and 'birth_date'.

                Returns:
                    QuerySet: A filtered queryset of users.
    """

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
    """
        AccountCreateView: A Django CBV (Class-Based View) for creating a new User account.

        Attributes:
            model (Model): The model associated with this view. In this case, the User model.
            template_name (str): The path of the template to render for this view.
            form_class (Form): The form class used to create a new User. Here it is AccountCreateForm.
            success_url (str): The URL to redirect to after a successful form submission.
                               Here it is set to the login view of the accounts application.
    """

    model = User
    template_name = "registration.html"
    form_class = AccountCreateForm
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        result = super().form_valid(form)
        user = form.instance
        messages.info(self.request,
                      f'Your account "{user.username}" has been successfully created. You can now log in.')
        return result


class AccountLoginView(LoginView):
    """
        AccountLoginView is a subclass of LoginView that handles user login actions.

        Attributes:
            template_name (str): Specifies the template to be used for rendering the login view.

        Methods:
            get_redirect_url:
                Determines the URL to redirect after a successful login.
                Returns the URL specified in the "next" GET parameter if present, otherwise redirects to the "core:index" URL.

            form_valid:
                Processes the valid form for user login.
                Adds an informational message indicating successful login of the user.
                Calls the form_valid method of the superclass and returns its result.
    """

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
    """
        Handles the user logout process and renders the specified logout template.

        Attributes:
            template_name (str): The path to the template that should be rendered upon logging out.
    """
    template_name = "logout.html"


class AccountUpdateView(LoginRequiredMixin, ProcessFormView):
    """
        AccountUpdateView handles the display and processing of user account update forms.

        The view is responsible for rendering the user's account update forms and handling
        the form submission for updating both the user and profile instances.

        Methods
        -------
        get(request, *args, **kwargs)
            Renders the user and profile update forms on 'profile.html'.

        post(request, *args, **kwargs)
            Processes the submitted user and profile update forms, saves the data if valid,
            and redirects to the profile page.
    """

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
    """
        ContactUsView handles requests for the contact us page.

        Inherits:
            LoginRequiredMixin: Mixin to ensure the user is authenticated.
            FormView: Generic view that displays and processes a form.

        Attributes:
            template_name: The template name used to render the contact us page.
            extra_content: Dictionary containing extra content to pass to the template.
            success_url: The URL to redirect to after successful form submission.
            form_class: The form class used to validate and process the contact us form.

        Methods:
            post(self, request, *args, **kwargs)
                Handles POST requests to the view.

                Args:
                    request: The HTTP request object.
                    *args: Variable length argument list.
                    **kwargs: Additional keyword arguments.

                Returns:
                    HTTP response object indicating the result of processing the form.

                If the form is valid, it tries to send a contact email asynchronously
                and logs the success or failure of the email sending process. Returns
                the appropriate response based on whether the form is valid or not.
    """

    template_name = "contact_us.html"
    extra_content = {"title": "Send us a message!"}
    success_url = reverse_lazy("core:index")
    form_class = ContactUsForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            try:
                logger.info("Email sent")

                send_contact_email.delay(
                    subject=form.cleaned_data["subject"],
                    message=form.cleaned_data["message"],
                    from_email=request.user.email
                )

                logger.info(f"Email sent successfully to {settings.EMAIL_HOST_RECIPIENT} from {request.user.email}")
            except Exception as e:
                logger.error(f"Error sending email: {e}")
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    html_email_template_name = 'password_reset_email.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = 'password_reset_subject.txt'
