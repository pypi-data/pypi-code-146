# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""

This module defines exceptions for Canner operations. It follows the structure
defined in pep-0249.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import functools
import random
import time
from enum import Enum
from typing import Callable, Any
import canner.logging

logger = canner.logging.get_logger(__name__)


class CannerErrorStatus(Enum):
    SQL_SYNTAX_FAILED = "Execute SQL failed"
    DATA_INCORRECT = "Cannot get data correctly, please run query.wait_for_finish(timeout=seconds,period=seconds) first"


class ConnectionError(Exception):
    def __init__(self, message: str):
        self._message = message

    @property
    def message(self):
        return self._message

    def __repr__(self):
        return '(name: "{}", message: "{}")'.format(
            self.__class__.__name__,
            self.message,
        )

    def __str__(self):
        return repr(self)


class CannerError(Exception):
    def __init__(self, error_code: str, message: str):
        self._error_code = error_code
        self._message = message

    @property
    def error_code(self):
        return self._error_code

    @property
    def message(self):
        return self._message

    def __repr__(self):
        return '(name: "{}", error_code: "{}", message: "{}")'.format(
            self.__class__.__name__,
            self.error_code,
            self.message,
        )

    def __str__(self):
        return repr(self)


class CannerQueryError(Exception):
    def __init__(self, error, query_id=None):
        self._error = error
        self._query_id = query_id

    @property
    def error_code(self):
        return self._error.get("errorCode", None)

    @property
    def error_name(self):
        return self._error.get("errorName", None)

    @property
    def error_type(self):
        return self._error.get("errorType", None)

    @property
    def error_exception(self):
        return self.failure_info.get("type", None) if self.failure_info else None

    @property
    def failure_info(self):
        return self._error.get("failureInfo", None)

    @property
    def message(self):
        return self._error.get("message", "Canner did no return an error message")

    @property
    def error_location(self):
        location = self._error["errorLocation"]
        return (location["lineNumber"], location["columnNumber"])

    @property
    def query_id(self):
        return self._query_id

    def __repr__(self):
        return '{}(type={}, name={}, message="{}", query_id={})'.format(
            self.__class__.__name__,
            self.error_type,
            self.error_name,
            self.message,
            self.query_id,
        )

    def __str__(self):
        return repr(self)


def retry_with(handle_retry, exceptions, conditions, max_attempts):
    def wrapper(func):
        @functools.wraps(func)
        def decorated(*args, **kwargs):
            error = None
            result = None
            for attempt in range(1, max_attempts + 1):
                try:
                    result = func(*args, **kwargs)
                    if any(guard(result) for guard in conditions):
                        handle_retry.retry(func, args, kwargs, None, attempt)
                        continue
                    return result
                except Exception as err:
                    error = err
                    if any(isinstance(err, exc) for exc in exceptions):
                        handle_retry.retry(func, args, kwargs, err, attempt)
                        continue
                    break
            logger.info("failed after {} attempts".format(attempt))
            if error is not None:
                raise error
            return result

        return decorated

    return wrapper


class DelayExponential(object):
    def __init__(
        self, base=0.1, exponent=2, jitter=True, max_delay=2 * 3600  # 100ms  # 2 hours
    ):
        self._base = base
        self._exponent = exponent
        self._jitter = jitter
        self._max_delay = max_delay

    def __call__(self, attempt):
        delay = float(self._base) * (self._exponent ** attempt)
        if self._jitter:
            delay *= random.random()
        delay = min(float(self._max_delay), delay)
        return delay


class RetryWithExponentialBackoff(object):
    def __init__(
        self, base=0.1, exponent=2, jitter=True, max_delay=2 * 3600  # 100ms  # 2 hours
    ):
        self._get_delay = DelayExponential(base, exponent, jitter, max_delay)

    def retry(self, func, args, kwargs, err, attempt):
        delay = self._get_delay(attempt)
        time.sleep(delay)


# The decorator for catching and show message
def handle_exception(func: Callable[..., Any]):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
            return response
        except CannerError as err:
            logger.error(
                f"Error occurred => code: {err.error_code}, message: {err.message}"
            )
            raise err
        except Exception as err:
            # Connection error (exceptions from requests package.)
            logger.error(f"Error occurred => {err}")
            raise err

    return wrapper
