from requests import sessions

from .MetaSession import my_session
from .optimized import optimized
from .response_optimized import response_optimized


@response_optimized
def get(url, params=None, headers=None, **kwargs):
    """get请求"""
    return request("GET", url, params=params, headers=headers, **kwargs)


@response_optimized
def post(url, data=None, headers=None, **kwargs):
    """post请求"""
    return request("POST", url, data=data, headers=headers, **kwargs)


@response_optimized
def session_get(url, params=None, headers=None, **kwargs):
    """session的get请求"""
    return my_session.meta_session('GET', url, params=params, headers=headers, **kwargs)


@response_optimized
def session_post(url, data=None, headers=None, **kwargs):
    """session的post请求"""
    return my_session.meta_session('POST', url, data=data, headers=headers, **kwargs)


@optimized
def request(method, url, **kwargs):
    # headers 数据优化
    print(kwargs)
    with sessions.Session() as session:
        return session.request(method=method, url=url, **kwargs)
