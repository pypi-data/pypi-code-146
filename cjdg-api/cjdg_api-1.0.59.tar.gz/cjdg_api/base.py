# 开放平台接口基类
from loguru import logger
import requests


def get_up_token(cjdg_access_token):
    """
    七牛上传令牌
    """
    url = "http://bms.chaojidaogou.com/shopguide/api/file/qiniu/getUpToken"
    params = {
        "accessToken": cjdg_access_token
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    params["response"] = response
    params["response_raw"] = response.content
    logger.error(params)


def request_accesstoken(acc: str, pwd: str, safe=False, domain=True, **kwargs) -> str:
    # 请求accesstooke函数
    protocol = "https" if safe else "http"
    domain_name = "bms.chaojidaogou.com" if domain else "it.xxynet.com"
    url = f"{protocol}://{domain_name}/shopguide/api/auth/logon"
    data = {}
    data["loginName"] = acc
    data["password"] = pwd
    data["version"] = "1"
    response = requests.get(url, data)
    if response.status_code == 200:
        accessToken = response.json().get("accessToken")
        return accessToken


def request_accesstoken_pc(acc: str, pwd: str, safe=False, domain=True, **kwargs) -> str:
    # 请求accesstooke函数
    protocol = "https" if safe else "http"
    domain_name = "bms.chaojidaogou.com" if domain else "it.xxynet.com"
    url = f"{protocol}://{domain_name}/shopguide/api/auth/logonweb"
    data = {}
    data["loginName"] = acc
    data["password"] = pwd
    data["version"] = "1"
    response = requests.get(url, data)
    if response.status_code == 200:
        accessToken = response.json().get("token")
        return accessToken


class base:
    def __init__(self, token, app_secret=None):
        """[summary]

        Args:
            token ([type]): [description]
            app_secret ([type], optional): [description]. Defaults to None.
        """
        self.token = token
        self.app_secret = app_secret

    def request(self, api_name=None, method="GET",url=None, api_prefix="api/", safe=False, domain=True,**kwargs):
        protocol = "https" if safe else "http"
        domain_name = "bms.chaojidaogou.com" if domain else "it.xxynet.com"
        host_name = f"{protocol}://{domain_name}/shopguide/"
        if not url:
            url = f"{host_name}{api_prefix}{api_name}" 
        # params
        params = kwargs.get("params", {})
        params["accessToken"] = self.token
        params["appSecret"] = self.app_secret
        kwargs["params"] = params
        # cookies
        cookies = kwargs.get("cookies", {})
        cookies["accessToken"] = self.token
        kwargs["cookies"] = cookies
        logger.debug(url)
        logger.debug(kwargs)
        response = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        if response.status_code == 200:
            return self.response(response.json())
        logger.error(response.text)

    def response(self, response_raw):

        return response_raw


class baseT:
    def __init__(self, token, app_secret=None):
        """[summary]

        Args:
            token ([type]): [description]
            app_secret ([type], optional): [description]. Defaults to None.
            这个base 解决 域名不一致的问题， 直接取域名。
        """
        self.token = token
        self.app_secret = app_secret

    def request(self, api_name=None, method="GET", url=None, api_prefix="api/", safe=False, domain=True, convert=False, **kwargs):
        protocol = "https" if safe else "http"
        domain_name = "bms.chaojidaogou.com" if domain else "it.xxynet.com"
        host_name = f"{protocol}://{domain_name}/"
        if not url:
            # url is None:generate url use hostname+api_prefix+apiname
            url = f"{host_name}{api_prefix}{api_name}" if convert else f"{host_name}{api_name}"
        # params
        params = kwargs.get("params", {})
        params["accessToken"] = self.token
        params["appSecret"] = self.app_secret
        kwargs["params"] = params
        # cookies
        cookies = kwargs.get("cookies", {})
        cookies["accessToken"] = self.token
        kwargs["cookies"] = cookies
        logger.debug(url)
        logger.debug(kwargs)
        response = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        if response.status_code == 200:
            return self.response(response.json())
        logger.error(response.text)

    def response(self, response_raw):

        return response_raw


class baseSub:
    def __init__(self, token, app_secret=None):
        """[summary]

        Args:
            token ([type]): [description]
            app_secret ([type], optional): [description]. Defaults to None.
            这个base 解决 域名不一致的问题， 直接取域名。
        """
        self.token = token
        self.app_secret = app_secret

    def request(self, api_name=None, method="GET", url=None, api_prefix="api/", safe=False, domain=True, convert=False, **kwargs):
        protocol = "https" if safe else "http"
        domain_name = "sub.chaojidaogou.com" if domain else "it.xxynet.com"
        host_name = f"{protocol}://{domain_name}/"
        if not url:
            # url is None:generate url use hostname+api_prefix+apiname
            url = f"{host_name}{api_prefix}{api_name}" if convert else f"{host_name}{api_name}"
        # params
        params = kwargs.get("params", {})
        params["accessToken"] = self.token
        params["appSecret"] = self.app_secret
        kwargs["params"] = params
        # cookies
        cookies = kwargs.get("cookies", {})
        cookies["accessToken"] = self.token
        kwargs["cookies"] = cookies
        logger.debug(url)
        logger.debug(kwargs)
        response = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        if response.status_code == 200:
            return self.response(response.json())
        logger.error(response.text)

    def response(self, response_raw):

        return response_raw


class baseCient:
    def __init__(self, token, app_secret=None):
        """[summary]

        Args:
            token ([type]): [description]
            app_secret ([type], optional): [description]. Defaults to None.
            这个base 解决 域名不一致的问题， 直接取域名。
        """
        self.token = token
        self.app_secret = app_secret

    def request(self, api_name=None, method="GET", url=None, api_prefix="api/", safe=False, domain=True, **kwargs):
        protocol = "https" if safe else "http"
        domain_name = "cient.chaojidaogou.com" if domain else "it.xxynet.com"
        host_name = f"{protocol}://{domain_name}/"
        if not url:
            # url is None:generate url use hostname+api_prefix+apiname
            url = f"{host_name}{api_prefix}{api_name}" 
        # params
        params = kwargs.get("params", {})
        params["accessToken"] = self.token
        params["appSecret"] = self.app_secret
        kwargs["params"] = params
        # cookies
        cookies = kwargs.get("cookies", {})
        cookies["accessToken"] = self.token
        kwargs["cookies"] = cookies
        logger.debug(url)
        logger.debug(kwargs)
        response = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        if response.status_code == 200:
            return self.response(response.json())
        logger.error(response.text)

    def response(self, response_raw):

        return response_raw




class baseApi:
    def __init__(self, token, app_secret=None):
        """[summary]

        Args:
            token ([type]): [description]
            app_secret ([type], optional): [description]. Defaults to None.
            这个base 解决 域名不一致的问题， 直接取域名。
        """
        self.token = token
        self.app_secret = app_secret

    def request(self, api_name=None, method="GET", url=None, api_prefix="api/", safe=False, domain=True, **kwargs):
        protocol = "https" if safe else "http"
        domain_name = "api.chaojidaogou.com" if domain else "it.xxynet.com"
        host_name = f"{protocol}://{domain_name}/"
        if not url:
            # url is None:generate url use hostname+api_prefix+apiname
            url = f"{host_name}{api_prefix}{api_name}" 
        # params
        params = kwargs.get("params", {})
        params["accessToken"] = self.token
        params["appSecret"] = self.app_secret
        kwargs["params"] = params
        # cookies
        cookies = kwargs.get("cookies", {})
        cookies["accessToken"] = self.token
        kwargs["cookies"] = cookies
        logger.debug(url)
        logger.debug(kwargs)
        response = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        if response.status_code == 200:
            return self.response(response.json())
        logger.error(response.text)

    def response(self, response_raw):

        return response_raw
