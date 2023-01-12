#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import re
import traceback
from copy import deepcopy
from functools import wraps
from inspect import getfullargspec
from pathlib import Path
from time import sleep
from typing import List, Dict, Callable, Any
from urllib.parse import urljoin

import requests
from requests import Response

from .._internal import _T
from ..char import StringBuilder
from ..config import RestConfig
from ..enums import EnhanceEnum
from ..exceptions import HttpException
from ..log import LoggerFactory
from ..utils import ObjectsUtils, StringUtils

_logger = LoggerFactory.get_logger("rest")

optional_args_keys = ["params", "data", "json", "headers", "cookies", "files", "auth", "timeout", "allow_redirects",
                      "proxies", "verify", "stream", "cert", "stream", "hooks"]

pattern = re.compile(f"^http|https?:/{2}\\w.+$")


class Method(EnhanceEnum):
    """
    Http method
    """
    GET = "GET"
    OPTIONS = "OPTIONS"
    HEAD = "HEAD"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class Rest(object):
    """
    A simple http request frame.
    """
    def __init__(self, file: str = None, server_name: str = None, host: str = None, only_body: bool = True,
                 check_status: bool = False, encoding: str = "utf-8", description: str = None):
        """
        Build a request client.
        :param file: The path where the interface configuration file is stored.
                     configuration format：
                        [
                          {
                            "serverName": "s1",
                            "serverHost": "http://localhost1",
                            "desc": "",
                            "apis": [
                              {
                                "apiName": "user",
                                "apiPath": "/user",
                                "httpMethod": "post",
                                "headers": {"Content-type": "multipart/form-data"},
                                "desc": ""
                              }
                            ]
                          },
                          {
                            "serverName": "s2",
                            "serverHost": "http://localhost2",
                            "desc": "",
                            "apis": [
                              {
                                "apiName": "admin",
                                "apiPath": "/admin",
                                "httpMethod": "get",
                                "desc": ""
                              }
                            ]
                          }
                        ]
        :param server_name: Service name, which allows you to read interface information from the interface configuration file.
        """
        self.__only_body: bool = only_body
        self.__check_status: bool = check_status
        self.__encoding: str = encoding
        self.__server_name: str = server_name
        self.__server_list: List[Dict[str, str]] = []
        self.__server: Dict[str, str] = {}
        self.__host: str = host
        self.__description: str = description
        if file:
            path = Path(file)
            if not path.is_absolute():
                path = Path.cwd().joinpath(file)
            if not path.exists():
                raise RuntimeError(f"not found file: {path}")
            with open(path.absolute(), "r") as f:
                self.__server_list = json.load(f)

    @staticmethod
    def retry(number: int = 10, interval: int = 5, exit_code_range: list = None, exception_retry: bool = True,
              check_body: Callable[[Any], bool] = None):
        """
        if http request fail or exception, will retry.
        :param check_body: This parameter is a callback function, if the return value is a pure body,
        it will determine whether to continue (make) the retry by checking the key of the body
        :param number: Number of retries
        :param interval: Retry interval
        :param exit_code_range: The expected HTTP status,
        if the response status code of the HTTP request is within this range, will exit the retry. The range is closed.
        default value [200, 299].
        :param exception_retry: Whether to retry when an exception occurs. True will try again
        """

        def __inner(func):
            @wraps(func)
            def __wrapper(*args, **kwargs):

                def default_check_body_call_back(res) -> bool:
                    return res and "status" in res and resp["status"] in exit_range

                exit_range = exit_code_range
                if not exit_range:
                    exit_range = [i for i in range(200, 300)]
                _interval = interval
                number_ = number + 1
                for i in range(1, number + 2):
                    # noinspection PyBroadException
                    try:
                        resp = func(*args, **kwargs)
                        #
                        if isinstance(resp, Response):
                            if resp.status_code in exit_range:
                                return resp
                        # Compatible with only_body parameters
                        elif isinstance(resp, dict or list):
                            if isinstance(check_body, Callable):
                                check_body_call_back = check_body
                            else:
                                check_body_call_back = default_check_body_call_back
                            if check_body_call_back(resp):
                                return resp
                        if i == number_:
                            break
                        else:
                            _logger.warn(f"http request retry times: {i}")
                            sleep(interval)
                    except BaseException:
                        if exception_retry:
                            if i == number_:
                                break
                            else:
                                _logger.warn(f"http request retry times: {i}")
                                sleep(interval)
                        else:
                            return

            return __wrapper

        return __inner

    def request(self, api_name: str = None, server_name: str = None, host: str = None, api: str = None,
                method: Method or str = None, allow_redirection: bool = RestConfig.allow_redirection,
                headers: dict = None, check_status: bool = RestConfig.check_status,
                encoding: str = RestConfig.encoding, only_body: bool = RestConfig.only_body, description: str = None):
        def __inner(func):
            @wraps(func)
            def __wrapper(*args, **kwargs):
                self.__request(func=func, kwargs=kwargs, api_name=api_name, server_name=server_name, host=host, api=api,
                               method=method, allow_redirection=allow_redirection, headers=headers,
                               check_status=check_status, encoding=encoding, only_body=only_body,
                               description=description)
                return func(*args, **kwargs)

            return __wrapper

        return __inner

    def get(self, api_name: str = None, server_name: str = None, host: str = None, api: str = None,
            allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
            check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding,
            only_body: bool = RestConfig.only_body, description: str = None):
        def __inner(func):
            @wraps(func)
            def __wrapper(*args, **kwargs):
                self.__request(func=func, kwargs=kwargs, api_name=api_name, server_name=server_name, host=host, api=api,
                               method=Method.GET, allow_redirection=allow_redirection, headers=headers,
                               check_status=check_status, encoding=encoding, only_body=only_body,
                               description=description)
                return func(*args, **kwargs)

            return __wrapper

        return __inner

    def post(self, api_name: str = None, server_name: str = None, host: str = None, api: str = None,
             allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
             check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding,
             only_body: bool = RestConfig.only_body, description: str = None):
        def __inner(func):
            @wraps(func)
            def __wrapper(*args, **kwargs):
                self.__request(func=func, kwargs=kwargs, api_name=api_name, server_name=server_name, host=host, api=api,
                               method=Method.POST, allow_redirection=allow_redirection, headers=headers,
                               check_status=check_status, encoding=encoding, only_body=only_body,
                               description=description)
                return func(*args, **kwargs)

            return __wrapper

        return __inner

    def put(self, api_name: str = None, server_name: str = None, host: str = None, api: str = None,
            allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
            check_status: bool = RestConfig.check_status,
            encoding: str = RestConfig.encoding, only_body: bool = RestConfig.only_body, description: str = None):
        def __inner(func):
            @wraps(func)
            def __wrapper(*args, **kwargs):
                self.__request(func=func, kwargs=kwargs, api_name=api_name, server_name=server_name, host=host, api=api,
                               method=Method.PUT, allow_redirection=allow_redirection, headers=headers,
                               check_status=check_status, encoding=encoding, only_body=only_body,
                               description=description)
                return func(*args, **kwargs)

            return __wrapper

        return __inner

    def delete(self, api_name: str = None, server_name: str = None, host: str = None, api: str = None,
               allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
               check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding,
               only_body: bool = RestConfig.only_body, description: str = None):
        def __inner(func):
            @wraps(func)
            def __wrapper(*args, **kwargs):
                self.__request(func=func, kwargs=kwargs, api_name=api_name, server_name=server_name, host=host, api=api,
                               method=Method.DELETE, allow_redirection=allow_redirection, headers=headers,
                               check_status=check_status, encoding=encoding, only_body=only_body,
                               description=description)
                return func(*args, **kwargs)

            return __wrapper

        return __inner

    def patch(self, api_name: str = None, server_name: str = None, host: str = None, api: str = None,
              allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
              check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding,
              only_body: bool = RestConfig.only_body, description: str = None):
        def __inner(func):
            @wraps(func)
            def __wrapper(*args, **kwargs):
                self.__request(func=func, kwargs=kwargs, api_name=api_name, server_name=server_name, host=host, api=api,
                               method=Method.PATCH, allow_redirection=allow_redirection, headers=headers,
                               check_status=check_status, encoding=encoding, only_body=only_body,
                               description=description)
                return func(*args, **kwargs)

            return __wrapper

        return __inner

    def head(self, api_name: str = None, server_name: str = None, host: str = None, api: str = None,
             allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
             check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding,
             only_body: bool = RestConfig.only_body, description: str = None):
        def __inner(func):
            @wraps(func)
            def __wrapper(*args, **kwargs):
                self.__request(func=func, kwargs=kwargs, api_name=api_name, server_name=server_name, host=host, api=api,
                               method=Method.HEAD, allow_redirection=allow_redirection, headers=headers,
                               check_status=check_status, encoding=encoding, only_body=only_body,
                               description=description)
                return func(*args, **kwargs)

            return __wrapper

        return __inner

    def options(self, api_name: str = None, server_name: str = None, host: str = None, api: str = None,
                allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
                check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding,
                only_body: bool = RestConfig.only_body, description: str = None):
        def __inner(func):
            @wraps(func)
            def __wrapper(*args, **kwargs):
                self.__request(func=func, kwargs=kwargs, api_name=api_name, server_name=server_name, host=host, api=api,
                               method=Method.OPTIONS, allow_redirection=allow_redirection, headers=headers,
                               check_status=check_status, encoding=encoding, only_body=only_body,
                               description=description)
                return func(*args, **kwargs)

            return __wrapper

        return __inner

    def __request(self, func: callable, kwargs: dict, api_name: str = None, server_name: str = None, host: str = None,
                  api: str = None, method: Method or str = None, allow_redirection: bool = True, headers: dict = None,
                  check_status: bool = None, encoding: str = None, only_body: bool = True, description: str = None):
        """
        Configure the interface information
        Important: requests arguments must be keyword arguments
        :param description: api's description info
        :param only_body: only need response body, if you need origin response, set false, default true
        :param encoding: parse response's text or content encode
        :param check_status: check http response status, default false
        :param api_name: Specify the API name, if empty while use function name as api name
        :param server_name: service name, which overrides the server_name of the instance.
                            If it is blank and the instance server_name is also blank,
                            the class name is used as the server name
        :param host: interface domain name, which is used first
        :param api: service http interface, which takes precedence over this parameter when specified
        :param method: interface request method, which is used in preference after specified
        :param allow_redirection: Whether to automatically redirect, the default is
        :param headers: custom http request header, if allow_redirection parameter is included,
        the allow_redirection in the header takes precedence
        """
        spec = getfullargspec(func)
        log_builder = StringBuilder()
        self.__build_log_message(log_builder, f"{'Rest Start'.center(41, '*')}")
        if "response" not in spec.args and "response" not in spec.kwonlyargs:
            raise RuntimeError(f"function {func.__name__} need 'response' args, ex: {func.__name__}(response) "
                               f"or {func.__name__}(response=None)")
        server_name_: str = self.__build_server_name(server_name, func)
        api_name_: str = self.__build_api_name(api_name, func)
        server_dict: dict = self.__get_server_dict(server_name_)
        server_description = self.__build_server_desc(self.__description, server_dict)
        host_: str = self.__build_host(host, server_dict)
        self.__check_domain(host_)
        api_: str = self.__get_api_info(server_dict, api_name_, "apiPath")
        api_: str = ObjectsUtils.none_of_default(api_, api)
        api_description = self.__build_api_desc(description, server_dict, api_name_, "desc")
        method_: str = self.__get_api_info(server_dict, api_name_, "httpMethod", )
        method_: str = ObjectsUtils.none_of_default(method_, self.__get_request_method(method))
        headers_: dict = self.__get_api_info(server_dict, api_name_, "headers")
        headers_: dict = ObjectsUtils.none_of_default(headers_, {})
        ObjectsUtils.check_non_none(api_)
        ObjectsUtils.check_non_none(Method.get_by_value(method_.upper()))
        optional_args: dict = self.__build_optional_args(func, kwargs, self.__get_api(server_dict, api_name_))
        self.__build_header(optional_args, allow_redirection, method_.upper(), headers_, headers)
        url: str = urljoin(host_, api_)
        check_status_: bool = self.__check_status if not check_status else check_status
        encoding_: str = self.__encoding if not encoding else encoding
        only_body_: bool = self.__only_body if not only_body else only_body
        # noinspection PyBroadException
        try:
            self.__build_log_message(log_builder,
                                     f"[Server Description]: {server_description}, [Api Description]: {api_description}\n\n"
                                     f"http request => url: {url}, method: {method_.lower()}, arguments: {optional_args}")
            resp: Response or None = self.__action(method_.lower(), url, **optional_args)
        except BaseException as e:
            e.__init__(f"An exception occurred during the http request process: url is {host_}{api_}")
            _logger.error(f"An exception occurred when a request was sent without a response:\n"
                         f"{traceback.format_exc()}")
            raise

        # noinspection PyBroadException
        try:
            self.__build_log_message(log_builder, f"http response => http code: {resp.status_code}, "
                                                  f"content: {resp.content.decode(encoding_)[:50]}...")
            if check_status_:
                if 200 > resp.status_code or resp.status_code >= 300:
                    _logger.error(f"check http status code is not success: {resp.status_code}")
                    raise HttpException(f"http status code is not success: {resp.status_code}")
            if only_body_:
                kwargs["response"] = resp.json()
            else:
                kwargs["response"] = resp
        except BaseException:
            if resp:
                _logger.error(
                    f"'{url}' response can't parse dict, response: {resp.content.decode(encoding_)[:50]}, "
                    f"exception: \n{traceback.format_exc()}")
                kwargs["response"] = resp.content.decode(encoding_)
            else:
                kwargs["response"] = None
        finally:
            self.__build_log_message(log_builder, f"{'Rest End'.center(43, '*')}")
            _logger.info(log_builder)

    def __get_server_dict(self, name: str) -> dict:
        if self.__server_list:
            for server in self.__server_list:
                if server.get("serverName") == name:
                    return server
        return {}

    def __build_host(self, host: str, server_dict: dict) -> str:
        host_: str = host
        if not host_:
            host_: str = self.__host
        if not host_:
            host_: str = server_dict.get("serverHost")
        return host_

    def __build_server_name(self, server_name: str, func: callable) -> str:
        if isinstance(server_name, str) and server_name.strip() != "":
            return server_name
        if isinstance(self.__server_name, str) and self.__server_name.strip() != "":
            return self.__server_name
        return func.__qualname__.split(".")[0]

    @staticmethod
    def __get_request_method(method: Method or str) -> str:
        if isinstance(method, Method):
            return method.value
        elif isinstance(method, str):
            return Method.get_by_value(method, Method.GET).value
        else:
            return Method.GET.value

    @staticmethod
    def __action(http_method: str, url: str, **kwargs) -> Response:
        kwargs["url"] = url
        action = getattr(requests, http_method, None)
        if action:
            return action(**kwargs)
        else:
            raise HttpException(f"unknown http method '{http_method}'")

    @staticmethod
    def __get_api_info(server_dict: dict, api_name, key: str) -> _T:
        """
        Take the value from the API dictionary, and use origin when it can't
        """
        return Rest.__get_api(server_dict, api_name).get(key)

    @staticmethod
    def __get_api(server_dict: dict, api_name) -> _T:
        """
        get api info from config
        """
        if "apis" in server_dict:
            api_list: List[Dict] = server_dict.get("apis")
            if issubclass(type(api_list), List):
                for api in api_list:
                    if isinstance(api, dict) and api.get("apiName") == api_name:
                        return api
        return {}

    @staticmethod
    def __check_domain(domain):
        if not pattern.match(domain):
            raise RuntimeError(f"invalid host: {domain}")

    @staticmethod
    def __build_header(all_params: dict, allow_redirection_: bool = True, method: str = Method.GET.value,
                       headers_by_config: dict = None, headers_by_kwargs: dict = None):
        headers_: dict = all_params.get("headers")
        if method == Method.POST.value or method == Method.PUT.value or method == Method.DELETE.value:
            content_type = "application/json"
        else:
            content_type = "application/x-www-form-urlencoded"
        if not headers_:
            headers_: dict = {"Content-type": content_type}
        else:
            if "Content-type" not in headers_:
                headers_["Content-type"] = content_type
        if not allow_redirection_:
            headers_["allow_redirection"] = allow_redirection_
        if isinstance(headers_by_config, dict):
            headers_.update(headers_by_config)
        if issubclass(type(headers_by_kwargs), dict):
            headers_.update(headers_by_kwargs)
        all_params["headers"] = headers_

    @staticmethod
    def __build_optional_args(func: Callable, all_args: dict, api_info: dict) -> dict:
        spec = getfullargspec(func)
        optional_args: dict = {}
        api_info_: dict = api_info if issubclass(type(api_info), dict) else {}
        for key in optional_args_keys:
            if key in api_info_:
                optional_args[key] = api_info_.get(key)
            if key in all_args:
                optional_args[key] = all_args.get(key)
        for k in list(all_args.keys())[:]:
            if k not in spec.args and k not in spec.kwonlyargs:
                del all_args[k]
        if optional_args:
            optional_args_copy: dict = deepcopy(optional_args)
            for k, v in optional_args_copy.items():
                if not v and k in optional_args:
                    del optional_args[k]
        return optional_args

    @staticmethod
    def __build_api_name(api_name: str, func: callable) -> str:
        if isinstance(api_name, str) and api_name.strip() != "":
            return api_name
        return func.__name__

    @staticmethod
    def __build_server_desc(origin: str, server_dict: dict) -> str:
        desc: str = origin
        if not desc:
            desc: str = server_dict.get("desc")
        return desc

    @staticmethod
    def __build_api_desc(default: _T, server_dict: dict, api_name, key: str) -> _T:
        default_: dict = default
        if not default_ and "apis" in server_dict:
            api_list: List[Dict] = server_dict.get("apis")
            if not api_list:
                return default_
            for api in api_list:
                if isinstance(api, dict) and api.get("apiName") == api_name:
                    return api.get(key)
        return default_

    @staticmethod
    def __build_log_message(origin: StringBuilder, msg: str):
        origin.append(f"\n{msg}\n")

    @staticmethod
    def bulk(content: str) -> Dict:
        """
        Convert headers copied from the browser to dicts
        :param content: header from the browser
        :return: python dict object
        """
        tmp = {}
        if issubclass(type(content), str):
            for line in content.split("\r\n"):
                kvs = line.split(":")
                kv_len = len(kvs)
                if kv_len == 2:
                    tmp[StringUtils.trip(kvs[0])] = StringUtils.trip(kvs[1])
                elif kv_len == 1:
                    tmp[StringUtils.trip(kvs[0])] = ""
                elif len(kvs) > 2:
                    tmp[StringUtils.trip(kvs[0])] = StringUtils.join(kvs[1:kv_len-1], ":")
                else:
                    continue
            return tmp
        else:
            return {"content": content}


__all__ = [Rest, Method]
