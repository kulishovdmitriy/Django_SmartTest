from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import User, Profile
from accounts.views import logger


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    """
        Creates a profile object after a user is created.
        The profile is saved to the database.
    """

    if created:
        Profile.objects.create(user=instance)
        logger.info(f"Profile created for user {instance.username}")
