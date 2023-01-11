from contextlib import contextmanager
from unittest.mock import patch

from w.services.technical.date_service import DateService


@contextmanager
def today_is(d):
    with patch("django.utils.timezone.now", return_value=DateService.to_datetime(d)):
        with patch("arrow.utcnow", return_value=DateService.get(d)) as m:
            yield m
