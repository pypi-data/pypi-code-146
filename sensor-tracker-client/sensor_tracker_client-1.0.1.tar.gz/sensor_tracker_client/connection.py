import requests

import time
from requests.exceptions import ConnectionError, ReadTimeout, RequestException

from .setting import setting
from .decorator import request_error_logging
from .authentication import authentication
from .util import api_keyword_to_url


@request_error_logging
def get_request(api_keyword, payload):
    url = api_keyword_to_url(api_keyword)
    try:
        if api_keyword is "deployment_hierarchy":
            r = requests.get(url, payload, timeout=(setting.CONNECT_TIMEOUT, setting.HIERARCHY_TIMEOUT))
        else:
            r = requests.get(url, payload, timeout=(setting.CONNECT_TIMEOUT, setting.READ_TIMEOUT))
    except ConnectionError as e:
        raise ConnectionError(e)
    except ReadTimeout as e:
        raise ReadTimeout(e)
    except RequestException as e:
        raise RequestException(e)
    return r


@request_error_logging
def get_request_int(api_keyword, obj_id):
    url = api_keyword_to_url(api_keyword)
    if not url.endswith('/'):
        url = url + '/'
    url = url + str(obj_id) + "/"
    try:
        r = requests.get(url, timeout=(setting.CONNECT_TIMEOUT, setting.READ_TIMEOUT))
    except ConnectionError as e:
        raise ConnectionError(e)
    except ReadTimeout as e:
        raise ReadTimeout(e)
    except RequestException as e:
        raise RequestException(e)
    return r


@request_error_logging
def get_request_by_pk(api_keyword, pk):
    url = api_keyword_to_url(api_keyword)
    if not url.endswith('/'):
        url = url + '/'
    url = url + pk + '/'
    try:
        r = requests.post(url, timeout=(setting.CONNECT_TIMEOUT, setting.READ_TIMEOUT))
    except ConnectionError as e:
        raise ConnectionError(e)
    except ReadTimeout as e:
        raise ReadTimeout(e)
    except RequestException as e:
        raise RequestException(e)
    return r


@request_error_logging
def post_request_with_token(api_keyword, payload):
    request_header = authentication.get_post_header()
    url = api_keyword_to_url(api_keyword)
    if not url.endswith("/"):
        url = url + "/"
    try:
        r = requests.post(url, payload, headers=request_header)
    except ConnectionError as e:
        raise ConnectionError(e)
    except ReadTimeout as e:
        raise ReadTimeout(e)
    except RequestException as e:
        raise RequestException(e)
    return r


@request_error_logging
def patch_request_with_token(api_keyword, target_obj_id, payload):
    request_header = authentication.get_post_header()
    url = api_keyword_to_url(api_keyword)
    if not url.endswith("/"):
        url = url + "/"
    url = url + str(target_obj_id) + "/"
    try:
        r = requests.patch(url, payload, headers=request_header)
    except ConnectionError as e:
        raise ConnectionError(e)
    except ReadTimeout as e:
        raise ReadTimeout(e)
    except RequestException as e:
        raise RequestException(e)
    return r
