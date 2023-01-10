import random
import time
from typing import Callable, Any, Union, List, Optional

import httpx
import requests
import urllib3
from pydantic import BaseModel

from pytailor.clients.auth import refresh_tokens
from pytailor.config import REQUEST_RETRY_COUNT
from pytailor.exceptions import BackendResponseError
from pytailor.models import TaskProcessingStatus
from pytailor.utils import get_logger

logger = get_logger("RequestHandler")

RETRY_HTTP_CODES = [
    httpx.codes.BAD_GATEWAY,
    httpx.codes.SERVICE_UNAVAILABLE,
    httpx.codes.GATEWAY_TIMEOUT,
]

RETRY_ERRORS = (
    httpx.TimeoutException,
    httpx.NetworkError,
    requests.exceptions.ConnectionError,
    urllib3.exceptions.ProtocolError,
)

MAX_SLEEP_TIME = 900


def _get_sleep_time_seconds(n):
    exp_backoff = 2 ** n
    jitter = random.randint(0, 300) / 100
    return min(exp_backoff + jitter, MAX_SLEEP_TIME)


def handle_retry(exc, no_of_retries):
    """Handle errors which qualify for retry"""
    retry = False
    no_of_retries += 1
    sleep_time = _get_sleep_time_seconds(no_of_retries)
    msg = f"Got error: {exc} Retrying in {sleep_time:.2f} secs, attempt {no_of_retries}"
    if isinstance(exc, httpx.HTTPStatusError):
        if exc.response.status_code in RETRY_HTTP_CODES:
            retry = True
        elif exc.response.status_code == httpx.codes.UNAUTHORIZED:
            refresh_tokens(no_of_retries > 1)
            retry = True
            sleep_time = 0.1
            msg = "Invalid access token, re-authenticating."
    elif isinstance(exc, RETRY_ERRORS):
        retry = True
    if retry:
        logger.warning(msg)
    return retry, no_of_retries, sleep_time


def handle_exception(exc, return_none_on, error_msg):
    """Handle errors which do not qualify for retry"""
    if isinstance(exc, httpx.HTTPStatusError):
        if exc.response.status_code in return_none_on:
            return
        error_msg += f" The response from the backend was: {exc}."
        try:
            error_msg += f" Details: {exc.response.json()['detail']}"
        except:
            pass
        raise BackendResponseError(error_msg)
    elif isinstance(exc, httpx.RequestError):
        error_msg += f" {exc}"
        raise BackendResponseError(error_msg)
    else:
        raise


def handle_file_client_call(
    client_method: Callable[..., Union[BaseModel, List[BaseModel]]],
    *args,
    error_msg: str = "Error.",
    return_none_on: Optional[List[httpx.codes]] = None,
) -> Any:
    if return_none_on is None:
        return_none_on = []

    try:
        no_of_retries = 0
        while True:
            try:
                return client_method(*args)
            except Exception as exc:
                retry, no_of_retries, sleep_time = handle_retry(exc, no_of_retries)
                if not (retry and no_of_retries < REQUEST_RETRY_COUNT):
                    raise
            time.sleep(sleep_time)

    except Exception as exc:
        handle_exception(exc, return_none_on, error_msg)


def handle_wait_retry(operation_result, no_of_retries):
    no_of_retries += 1
    sleep_time = _get_sleep_time_seconds(no_of_retries)
    retry = False
    if operation_result.processing_status is TaskProcessingStatus.PENDING:
        retry = True
    return retry, no_of_retries, sleep_time


def handle_waited_for(operation_result):
    if operation_result.processing_status is TaskProcessingStatus.PENDING:
        raise BackendResponseError("Backend processing timed out.")
    elif operation_result.processing_status is TaskProcessingStatus.FAILED:
        raise BackendResponseError(
            f"Backend processing failed with the following error message: " f"{operation_result.msg}"
        )
    elif operation_result.processing_status is TaskProcessingStatus.COMPLETED:
        return operation_result
