from .global_options import GlobalOptions
from .head_format import head_format


def optimized(func):
    def inner(*args, **kwargs):
        # headers头部参数优化
        kwargs = headers_optimized(kwargs)
        # 请求参数优化
        kwargs = data_optimized(kwargs)

        reqs = func(*args, **kwargs)
        return reqs

    return inner


def data_optimized(kwargs):
    """自动把data和params格式化成字典数据"""
    if kwargs.get('data'):  # 判断是否有data
        if isinstance(kwargs['data'], str):  # 转换字符串类型为字典
            kwargs['data'] = head_format(kwargs['data'])

    if kwargs.get('params'):  # 判断是否有data
        if isinstance(kwargs['params'], str):  # 转换字符串类型为字典
            kwargs['params'] = head_format(kwargs['params'])

    return kwargs


def headers_optimized(kwargs):
    """自动添加User-Agent  自动把字符串格式化成字典数据"""
    if kwargs.get('headers'):  # 判断是否有headers
        # isinstance 是否是什么类型
        if isinstance(kwargs['headers'], str):  # 转换字符串类型为字典
            kwargs['headers'] = head_format(kwargs['headers'].replace('user-agent', 'User-Agent'))

            if not kwargs['headers'].get('User-Agent'):  # 判断headers是否有User-Agent
                kwargs['headers'].update(GlobalOptions.headers)
    else:
        kwargs['headers'] = GlobalOptions.headers
        # 判断字典有没有headers
    return kwargs
