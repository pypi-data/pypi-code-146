import functools
import logging
from contextlib import contextmanager

from sqlalchemy.exc import IntegrityError

from reljicd_utils.config.env_vars import LOGGING_LEVEL
from reljicd_utils.rdbms.scoped_session import Session
from reljicd_utils.logger.logger import get_logger

LOGGER = get_logger(__name__)


def transaction(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        Session.close()

        try:
            result = func(*args, **kwargs)
            Session.commit()
        except Exception as e:
            Session.rollback()
            raise
        finally:
            Session.close()
        return result

    return wrapper


@contextmanager
def transaction_scope(
        print_exceptions: bool = True if LOGGING_LEVEL == 'debug' else False,
        error_message: str = None,
        skip_message: str = None,
        skip_on_integrity_error: bool = False,
        logger: logging.Logger = None):
    if logger is None:
        logger = LOGGER

    try:
        yield
        Session.commit()
    except IntegrityError as e:
        if print_exceptions:
            logger.error(e)
        Session.rollback()
        if error_message:
            logger.info(e)
        if skip_on_integrity_error:
            if skip_message:
                logger.info(skip_message)
        else:
            raise
    except Exception as e:
        if print_exceptions:
            logger.error(e)
        Session.rollback()
        if error_message:
            logger.info(e)
        raise
