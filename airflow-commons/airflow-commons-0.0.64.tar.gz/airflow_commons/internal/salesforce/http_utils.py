from airflow_commons.internal.salesforce.constants import (
    ASYNC_PATH,
    DATA_EXTENSION_KEY_PATH,
    ASYNC_JOB_RESULT_PATH,
    ASYNC_JOB_STATUS_PATH,
    DATA_PATH,
    CUSTOM_OBJECT_DATA_PATH,
    FILTER_QUERY,
    SYNC_PATH,
    DATA_EVENT_KEY_PATH,
)
from airflow_commons.resources.glossary import QUESTION_MARK


def get_headers(access_token: str):
    """
    Builds a request header with given token.
    :param access_token: Active access token
    :return:
    """
    return {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + access_token,
    }


def get_async_operation_url(base_url: str, key: str):
    """
    Builds an async operation url
    :param base_url:
    :param key:
    :return:
    """
    return base_url + ASYNC_PATH + DATA_EXTENSION_KEY_PATH.format(key=key)


def get_async_operation_result_url(base_url: str, request_id: str):
    """
    Builds an async operation result url
    :param base_url:
    :param request_id:
    :return:
    """
    return base_url + ASYNC_PATH + ASYNC_JOB_RESULT_PATH.format(request_id=request_id)


def get_async_operation_status_url(base_url: str, request_id: str):
    """
    Builds an async operation status url
    :param base_url:
    :param request_id:
    :return:
    """
    return base_url + ASYNC_PATH + ASYNC_JOB_STATUS_PATH.format(request_id=request_id)


def get_fetch_operation_url(base_url: str, key: str, filter: str = None):
    """
    Builds a get operation url
    :param base_url:
    :param key:
    :param filter: optional filter of search query
    :return:
    """
    url = base_url + DATA_PATH + CUSTOM_OBJECT_DATA_PATH.format(key=key)
    if filter:
        url = url + QUESTION_MARK + FILTER_QUERY.format(filter=filter)

    return url


def get_sync_operation_url(base_url: str, key: str):
    """
    Builds a sync operation url
    :param base_url:
    :param key:
    :return:
    """
    return base_url + SYNC_PATH + DATA_EVENT_KEY_PATH.format(key=key)
