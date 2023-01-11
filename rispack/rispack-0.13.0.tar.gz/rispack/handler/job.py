from functools import wraps

from .record import RecordBuilder
from rispack.logger import logger

def job(func):
    @wraps(func)
    def wrapper(event, context):
        logger.debug('job event', event)
        logger.debug('job context', event)

        items = event.get("Records") or [event]

        for item in items:
            record = RecordBuilder(item).build()

            func(record)

    return wrapper
