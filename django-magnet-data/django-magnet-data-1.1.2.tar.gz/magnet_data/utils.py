import datetime
from django.utils import timezone


def today() -> datetime.date:
    """
    This method obtains today's date in local time
    """
    return timezone.localtime(timezone.now()).date()
