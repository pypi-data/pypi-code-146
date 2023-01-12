import logging

from rest_framework.exceptions import NotAuthenticated
from rest_framework.views import exception_handler

from .exceptions import UnprocessableEntityError

logger = logging.getLogger(__name__)
exceptions_to_info = (
    NotAuthenticated,
    UnprocessableEntityError,
)


def exception_logger(exception: Exception, context):
    """Log given exception (because it is not done by default handler).

    Exceptions defined in `exceptions_to_info` are logged at the INFO level.
    Exceptions handled by the default `exception_handler` with `status_code`
    < 500 are logged at the WARNING level. Any other exception is logged at
    the ERROR level.
    """
    response = exception_handler(exception, context)
    if exception and isinstance(exception, exceptions_to_info):
        logger.info(exception)
    elif response is not None and response.status_code < 500:
        logger.warning(exception)
    else:
        logger.error(exception)
    return response
