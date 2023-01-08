from datetime import timedelta
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from django.utils.timezone import now
from passwordless.defaults import PASSWORDLESS_MAX_REQUEST_AGE
from passwordless.models import AuthFailure, AuthRequest


class Command(BaseCommand):
    def handle(self, *args, **options):
        cutoff = now() - timedelta(
            seconds=getattr(
                settings,
                "PASSWORDLESS_MAX_REQUEST_AGE",
                PASSWORDLESS_MAX_REQUEST_AGE,
            )
        )

        cutoff = now()

        # clear expired and used requests
        AuthRequest.objects.filter(Q(created__lt=cutoff) | Q(is_used=True)).delete()

        # clear expired failures
        AuthFailure.objects.filter(created__lt=cutoff).delete()
