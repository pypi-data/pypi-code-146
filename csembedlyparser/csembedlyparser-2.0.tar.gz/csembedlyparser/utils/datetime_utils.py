import pytz
from datetime import datetime
from django.conf import settings

def get_datetime_now_utc():
    if getattr(settings, 'USE_TZ', False):
        u=datetime.utcnow()
        return u.replace(tzinfo=pytz.utc)
    else:
        return datetime.now()

def to_utc(date):
    utc = pytz.utc
    return utc.localize(date)
