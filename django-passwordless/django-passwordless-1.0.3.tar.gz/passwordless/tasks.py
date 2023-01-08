from celery import shared_task
from django.conf import settings

from .defaults import PASSWORDLESS_USE_CELERY


@shared_task
def celery_send_email(id):
    from .models import AuthRequest

    print("-----------------------")
    print(id)
    ar = AuthRequest.objects.get(id=id)
    ar.send_otp()
