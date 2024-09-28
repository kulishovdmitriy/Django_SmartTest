from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import Profile
from accounts.views import logger


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    """
        :param sender: The model class that sent the signal
        :param instance: The instance of the model that was saved
        :param created: A boolean indicating if a new record was created
        :param kwargs: Additional keyword arguments
        :return: None
    """

    if created:
        Profile.objects.create(user=instance)
        logger.info(f"Profile created for user {instance.username}")
    else:
        instance.profile.save()
        logger.info(f"Profile updated for user {instance.username}")
