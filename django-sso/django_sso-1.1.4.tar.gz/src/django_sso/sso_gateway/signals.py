import logging

from django.contrib.auth import get_user_model, user_logged_out
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Service

user_model = get_user_model()


@receiver(post_save, sender=user_model)
def push_update_user_event(sender, instance, **kwargs):
    for service in Service.objects.filter(enabled=True):
        try:
            service.update_account(instance)
        except Exception as e:
            logging.critical(f"Django SSO event dispatching error: {e}")


@receiver(user_logged_out)
def push_deauthenticate_user_event(user=None, *args, **kwargs):
    if user:
        for service in Service.objects.filter(enabled=True):
            try:
                service.deauthenticate(user)
            except Exception as e:
                logging.critical(f"Django SSO event dispatching error: {e}")
