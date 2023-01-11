from pytz import timezone

from shared.external.tools.time_utils import datetime_or_str_to_iso_utc
from datetime import datetime


def test_datetime_or_str_to_iso_utc():
    a = datetime.strptime("19700101_000000000000", "%Y%m%d_%H%M%S%f")

    pacific = timezone('US/Pacific')

    a.astimezone(pacific)
    assert a.tzinfo is None

    b = pacific.localize(a)

    assert str(b.tzinfo) == 'US/Pacific'

    assert datetime_or_str_to_iso_utc(b) == "1970-01-01T08:00:00+00:00"

    utc = timezone('UTC')

    b = utc.localize(a)

    assert datetime_or_str_to_iso_utc(b) == "1970-01-01T00:00:00+00:00"