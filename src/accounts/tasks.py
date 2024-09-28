from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_contact_email(subject, message, from_email):
    """
        :param subject: The subject line of the email.
        :param message: The body content of the email.
        :param from_email: The sender's email address.
        :return: None
    """
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=[settings.EMAIL_HOST_RECIPIENT],
        fail_silently=False,
    )
