from functools import partial
import importlib
import inspect
import logging
from unicodedata import east_asian_width


logger = logging.getLogger(__name__)


class ArgsError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def make_partial(func, **kwargs):
    if func is not None:
        parameters = inspect.signature(func).parameters
        func_args = []
        func_kwargs = {}
        first_arg = None
        for idx, (key, value) in enumerate(parameters.items()):
            if idx == 0:
                first_arg = key
            if value._default is inspect._empty:
                func_args.append(key)
            else:
                func_kwargs[key] = value.default
        
        # 함수 파라미터
        len_func_args = len(func_args)
        len_func_kwargs = len(func_kwargs)
        all_func_parameters = func_args + list(func_kwargs.keys())

        # 키워드 인자 재설정
        new_kwargs = {}
        for key, value in kwargs.items():
            if key in all_func_parameters:
                if key != first_arg:
                    new_kwargs[key] = value
                else:
                    logger.warning(f"{key}는 kwargs로 사용할 수 없습니다.")
        
        # 부족한 인자 확인
        not_enough_args = []
        for key in all_func_parameters:
            if not key in new_kwargs and key != first_arg and key not in func_kwargs:
                not_enough_args.append(key)
                
        if not not_enough_args:
            return partial(func, **new_kwargs)
        else:
            func_name = func.__name__
            raise ArgsError(f"{func_name}를 실행하는데 필요한 인자가 충분하지 않습니다. 필요한 인자 = {not_enough_args}")
    return None


def is_available(package: str):
    return importlib.util.find_spec(package) is not None


def width(text: str):
    if not isinstance(text, str):
        text = str(text)
    l = 0
    for s in text:
        if east_asian_width(s) in ['F', 'W']:
            l += 2
        else:
            l += 1
    return l