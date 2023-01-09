from django.db.models import Q
from typing import Optional
from scrobbles.models import Scrobble

from django.utils import timezone
from datetime import datetime, timedelta


def reset_to_midnight(date):
    return datetime.combine(date.date(), datetime.min.time(), date.tzinfo)


def artist_scrobble_count(artist_id: int, filter: Optional[str] = None) -> int:
    now = timezone.now()
    today = reset_to_midnight(now)
    last_90_days = reset_to_midnight(now - timedelta(days=90))
    last_week = reset_to_midnight(now - timedelta(days=7))
    last_month = reset_to_midnight(now - timedelta(days=30))

    time_filter = Q(timestamp__gte=now - timedelta(days=90))
    if filter == 'today':
        time_filter = Q(timestamp__gte=today)
    if filter == 'week':
        time_filter = Q(timestamp__gte=last_week)
    if filter == 'month':
        time_filter = Q(timestamp__gte=last_month)
    return (
        Scrobble.objects.filter(track__artist=artist_id)
        .filter(time_filter)
        .count()
    )
