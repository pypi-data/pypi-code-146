# @Time    : 2022/2/22 9:35
# @Author  : kang.yang@qizhidao.com
# @File    : request.py
import json as json_util
import logging
import sys
from urllib import parse

import requests
from deepdiff import DeepDiff

from qrunner.utils.config import config
from qrunner.utils.json_utils import formatting, get_schema
from qrunner.utils.log import logger

# 去掉requests本身的日志
urllib3_logger = logging.getLogger("urllib3")
urllib3_logger.setLevel(logging.CRITICAL)


def request(func):
    def wrapper(*args, **kwargs):
        logger.info("-------------- Request -----------------[🚀]")
        # 给接口带上默认域名
        try:
            path = list(args)[1]
        except IndexError:
            path = kwargs.get("url", "")

        if "http" not in path:
            base_url = config.get_host()
            if "http" in base_url:
                url = parse.urljoin(base_url, path)
                try:
                    args_list = list(args)
                    args_list[1] = url
                    args = tuple(args_list)
                except Exception:
                    kwargs["url"] = url
            else:
                logger.debug("请设置正确的base_url")
                sys.exit()
        else:
            url = path

        # img_file = False
        # file_type = url.split(".")[-1]
        # if file_type in IMG:
        #     img_file = True

        # 请求头处理，写入登录态
        login_status = kwargs.get("login", True)
        tmp_headers = config.get_login() if login_status is True else config.get_visit()
        if tmp_headers:
            tmp_headers.update(kwargs.pop("headers", {}))
            kwargs["headers"] = tmp_headers

        # 设置默认超时时间
        timeout_config = config.get_timeout()
        timeout_user_set = kwargs.pop("timeout", None)
        kwargs["timeout"] = (
            timeout_user_set if timeout_user_set is not None else timeout_config
        )

        # 获取日志需要的参数信息
        auth = kwargs.get("auth", "")
        cookies = kwargs.get("cookies", "")
        params = kwargs.get("params", "")
        data = kwargs.get("data", "")
        json = kwargs.get("json", "")

        # 发送请求
        r = func(*args, **kwargs)

        # 输出请求参数日志
        logger.debug(
            "[method]: {m}      [url]: {u}".format(m=func.__name__.upper(), u=url)
        )
        if auth != "":
            logger.debug(f"[auth]:\n {formatting(auth)}")
        logger.debug(f"[headers]:\n {formatting(dict(r.request.headers))}")
        if cookies != "":
            logger.debug(f"[cookies]:\n {formatting(cookies)}")
        if params != "":
            logger.debug(f"[params]:\n {formatting(params)}")
        if data != "":
            logger.debug(f"[data]:\n {formatting(data)}")
        if json != "":
            logger.debug(f"[json]:\n {formatting(json)}")

        # 保存响应结果并输出日志
        status_code = r.status_code
        headers = r.headers
        content_type = headers.get("Content-Type")
        ResponseResult.status_code = status_code
        logger.info("-------------- Response ----------------")
        logger.debug(f"[status]: {status_code}")
        logger.debug(f"[headers]: {formatting(headers)}")
        try:
            resp = r.json()
            logger.debug(f"[type]: json")
            logger.debug(f"[response]:\n {formatting(resp)}")
            ResponseResult.response = resp
        except Exception:
            # 非json响应数据，根据响应内容类型进行判断
            if "text" not in content_type:
                logger.debug(f"[type]: {content_type}")
                logger.debug(f"[response]:\n {r.content}")
                ResponseResult.response = r.content
            else:
                logger.debug(f"[type]: {content_type}")
                logger.debug(f"[response]:\n {r.text}")
                ResponseResult.response = r.text

    return wrapper


class ResponseResult:
    status_code = 200
    response = None


class HttpRequest(object):
    @request
    def get(self, url, params=None, login=True, **kwargs):
        # if "http" not in url:
        #     base_url = conf.get_item('common', 'base_url')
        #     if 'http' in base_url:
        #         url = parse.urljoin(base_url, url)
        #     else:
        #         logger.debug('请设置正确的base_url')
        #         sys.exit()
        return requests.get(url, params=params, **kwargs)

    def get_req_schema(self, *args, **kwargs):
        """get请求，检查多次请求返回的schema是否稳定"""
        exclude_paths = kwargs.pop("exclude_paths", {})
        execute_time = kwargs.pop("execute_time", 10)

        self.get(*args, **kwargs)
        schema_start = get_schema(self.response)
        diff_result = []

        for i in range(execute_time):
            logger.debug(f"第 {i+1} 次执行")
            self.get(*args, **kwargs)
            schema_ = get_schema(self.response)
            result = DeepDiff(schema_start, schema_, exclude_paths=exclude_paths)
            diff_result.append(result)

        logger.debug(f"diff结果:")
        for item in diff_result:
            for item_ in item.items():
                print(item_)

    @request
    def post(self, url, data=None, json=None, login=True, **kwargs):
        # if "http" not in url:
        #     base_url = conf.get_item('common', 'base_url')
        #     logger.debug(base_url)
        #     if 'http' in base_url:
        #         url = parse.urljoin(base_url, url)
        #     else:
        #         logger.debug('请设置正确的base_url')
        #         sys.exit()
        return requests.post(url, data=data, json=json, **kwargs)

    def post_req_schema(self, *args, **kwargs):
        """post请求，检查多次请求返回的schema是否稳定"""
        exclude_paths = kwargs.pop("exclude_paths", {})
        execute_time = kwargs.pop("execute_time", 10)

        self.post(*args, **kwargs)
        schema_start = get_schema(self.response)
        diff_result = []

        for i in range(execute_time):
            logger.debug(f"第 {i+1} 次执行")
            self.post(*args, **kwargs)
            schema_ = get_schema(self.response)
            result = DeepDiff(schema_start, schema_, exclude_paths=exclude_paths)
            diff_result.append(result)

        logger.debug(f"diff结果:")
        for item in diff_result:
            for item_ in item.items():
                print(item_)

    @request
    def put(self, url, data=None, json=None, login=True, **kwargs):
        # if "http" not in url:
        #     base_url = conf.get_item('common', 'base_url')
        #     if 'http' in base_url:
        #         url = parse.urljoin(base_url, url)
        #     else:
        #         logger.debug('请设置正确的base_url')
        #         sys.exit()
        if json is not None:
            data = json_util.dumps(json)
        return requests.put(url, data=data, **kwargs)

    @request
    def delete(self, url, login=True, **kwargs):
        # if "http" not in url:
        #     base_url = conf.get_item('common', 'base_url')
        #     if 'http' in base_url:
        #         url = parse.urljoin(base_url, url)
        #     else:
        #         logger.debug('请设置正确的base_url')
        #         sys.exit()
        return requests.delete(url, **kwargs)

    @property
    def response(self):
        """
        Returns the result of the response
        :return: response
        """
        return ResponseResult.response

    @property
    def session(self):
        """
        A Requests session.
        """
        s = requests.Session()
        return s

    @staticmethod
    def request(
        method=None,
        url=None,
        headers=None,
        files=None,
        data=None,
        params=None,
        auth=None,
        cookies=None,
        hooks=None,
        json=None,
    ):
        """
        A user-created :class:`Request <Request>` object.
        """
        req = requests.Request(
            method, url, headers, files, data, params, auth, cookies, hooks, json
        )
        return req
