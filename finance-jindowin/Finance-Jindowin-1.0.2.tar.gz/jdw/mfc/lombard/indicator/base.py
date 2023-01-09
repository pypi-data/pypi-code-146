# -*- encoding:utf-8 -*-
import functools, six
from functools import partial
from collections import Iterable
import pandas as pd

if pd.__version__ >= '0.20.0':
    g_pandas_has_ewm = True
    g_pandas_has_rolling = True


def __pd_object_covert_start(iter_obj):
    """
    _pd_object_covert中进行参数检测及转换
    :param iter_obj: 将要进行操作的可迭代序列
    :return: 操作之后的返回值是否需要转换为np.array
    """
    if isinstance(iter_obj, (pd.Series, pd.DataFrame)):
        # 如果本身就是(pd.Series, pd.DataFrame)，返回对返回值不需要转换，即False
        return iter_obj, False
    # TODO Iterable和six.string_types的判断抽出来放在一个模块，做为Iterable的判断来使用
    if isinstance(iter_obj,
                  Iterable) and not isinstance(iter_obj, six.string_types):
        # 可迭代对象使用pd.Series进行包装，且返回对返回值需要转换为np.array，即True
        return pd.Series(iter_obj), True
    raise TypeError('pd_object must support Iterable!!!')


def _pd_object_covert(func):
    """针对参数序列进行pandas处理的事前，事后装饰器"""

    @functools.wraps(func)
    def wrapper(pd_object, pd_object_cm, how, *args, **kwargs):
        """事前装饰工作__pd_object_covert_start，事后根据是否需要转换为np.array工作"""
        # 事前装饰工作__pd_object_covert_start
        pd_object, ret_covert = __pd_object_covert_start(pd_object)
        ret = func(pd_object, pd_object_cm, how, *args, **kwargs)
        # 事后根据是否需要转换为np.array工作
        if ret is not None and ret_covert:
            return ret.values
        return ret

    return wrapper


@_pd_object_covert
def _pd_ewm(pd_object, pd_object_cm, how, *args, **kwargs):
    """
    被_pd_object_covert装饰，对pandas中的ewm操作，根据pandas version版本自动选择调用方式
    :param pd_object: 可迭代的序列，pd.Series, pd.DataFrame或者只是Iterable
    :param pd_object_cm: 与pd_object相同，针对需要两个pandas对象或者序列执行的操作，如corr，cov等
    :param how: 代表方法操作名称，eg. mean, std, var
    :return:
    """
    if g_pandas_has_ewm:
        """pandas版本高，使用如pd_object.ewm直接调用"""
        ewm_obj = pd_object.ewm(*args, **kwargs)
        if hasattr(ewm_obj, how):
            if pd_object_cm is None:
                return getattr(ewm_obj, how)()
            # 需要两个pd_object进行的操作
            return getattr(ewm_obj, how)(pd_object_cm)
    else:
        """pandas版本低，使用如pd.ewmstd方法调用"""
        if how == 'mean':
            # pd.ewma特殊代表加权移动平均，所以使用a替换mean
            how = 'a'
        how_func = 'ewm{}'.format(how)
        if hasattr(pd, how_func):
            if pd_object_cm is None:
                return getattr(pd, how_func)(pd_object, *args, **kwargs)
            # 需要两个pd_object进行的操作
            return getattr(pd, how_func)(pd_object, pd_object_cm, *args,
                                         **kwargs)
    raise RuntimeError('_pd_ewm {} getattr error'.format(how))


pd_ewm_mean = partial(_pd_ewm, how='mean', pd_object_cm=None)