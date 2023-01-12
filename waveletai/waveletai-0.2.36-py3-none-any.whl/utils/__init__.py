#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/3/11 15:40
@Author  : WaveletAI-Product-Team Janus
@license : (C) Copyright 2019-2022, Visionet(Tianjin)Information Technology Co.,Ltd.
@Site    : plus.xiaobodata.com
@File    : __init__.py
@Desc    :
"""
import functools

import mlflow
import requests
from waveletai.exceptions import ConnectionLost, Forbidden, ServerError, Unauthorized, SSLError, RequiredAppError, \
    RequiredModelError
from bravado.exception import BravadoConnectionError, BravadoTimeoutError, HTTPForbidden, \
    HTTPInternalServerError, HTTPServerError, HTTPUnauthorized, HTTPServiceUnavailable, HTTPRequestTimeout, \
    HTTPGatewayTimeout, HTTPBadGateway
import logging
import sys
import time
import uuid

_logger = logging.getLogger(__name__)

IS_WINDOWS = sys.platform == 'win32'
IS_MACOS = sys.platform == 'darwin'


def gen_id():
    str_uuid = "".join(str(uuid.uuid4()).split("-"))
    return str_uuid


def map_values(f_value, dictionary):
    return dict(
        (k, f_value(v)) for k, v in dictionary.items()
    )


def map_keys(f_key, dictionary):
    return dict(
        (f_key(k), v) for k, v in dictionary.items()
    )


def as_list(value):
    if value is None or isinstance(value, list):
        return value
    else:
        return [value]


def require_app(func):
    def wrapper(self, *args, **kwargs):
        if self.app_id:
            return func(self, *args, **kwargs)
        raise RequiredAppError()

    return wrapper


def require_model(func):
    def wrapper(self, *args, **kwargs):
        if self.model_id:
            return func(self, *args, **kwargs)
        raise RequiredModelError()

    return wrapper


def with_api_exceptions_handler(func):
    def wrapper(*args, **kwargs):
        for retry in range(0, 11):
            try:
                return func(*args, **kwargs)
            except requests.exceptions.SSLError:
                raise SSLError()
            except (BravadoConnectionError, BravadoTimeoutError,
                    requests.exceptions.ConnectionError, requests.exceptions.Timeout,
                    HTTPRequestTimeout, HTTPServiceUnavailable, HTTPGatewayTimeout, HTTPBadGateway):
                if retry >= 6:
                    _logger.warning(
                        'Experiencing connection interruptions. Reestablishing communication with WaveletAI.')
                time.sleep(2 ** retry)
                continue
            except HTTPServerError:
                raise ServerError()
            except HTTPUnauthorized:
                raise Unauthorized()
            except HTTPForbidden:
                raise Forbidden()
            except requests.exceptions.RequestException as e:
                if e.response is None:
                    raise
                status_code = e.response.status_code
                if status_code in (
                        HTTPBadGateway.status_code,
                        HTTPServiceUnavailable.status_code,
                        HTTPGatewayTimeout.status_code):
                    if retry >= 6:
                        _logger.warning(
                            'Experiencing connection interruptions. Reestablishing communication with WaveletAI.')
                    time.sleep(2 ** retry)
                    continue
                elif status_code >= HTTPInternalServerError.status_code:
                    raise ServerError()
                elif status_code == HTTPUnauthorized.status_code:
                    raise Unauthorized()
                elif status_code == HTTPForbidden.status_code:
                    raise Forbidden()
                else:
                    raise
        raise ConnectionLost()

    return wrapper


class MLflowModuleRegister:
    def __init__(self, model_name):
        self.model = model_name

    def __getattr__(self, item):
        _m = getattr(mlflow, self.model)
        return getattr(_m, item)


def set_mlflow_tracing_waveletai_store(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        mlflow.set_tracking_uri('waveletai-store://')
        return func(*args, **kwargs)

    return wrapper
