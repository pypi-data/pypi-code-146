# -*- coding: utf-8 -*-
"""
===============================
@author     : yaoruiqi

@Time       : 2021/10/10 10:00

@version    : V0.1

@introduce  : 重试模块

@change     : 
===============================
"""
import time
from loguru import logger


class MyRetry:

    def __init__(self, times=1, sleep_time=0, custom_return=(False, False), return_msg=False, show_params=False, show_process=True):
        """
        重试模块
        :param times: 重试次数
        :param sleep_time: 重试间隔时间
        :param custom_return: 自定义返回内容 当custom_return[0]为True时，返回custom_return[1]
        :param return_msg: 重试失败后打印的字符串
        :param show_params: 重试失败后是否打印传入的参数
        :param show_process: 是否打印重试过程
        """
        self.times = times
        self.sleep_time = sleep_time
        self.custom_return = custom_return
        self.return_msg = return_msg
        self.show_params = show_params
        self.show_process = show_process

    def __call__(self, fun):
        retry_time = self.times
        sleep_time = self.sleep_time
        custom_return = self.custom_return
        return_msg = self.return_msg
        show_params = self.show_params
        show_process = self.show_process

        def retry_handle(*args, **kwargs):
            msg = f'函数: {fun.__name__} 重试{retry_time}次后发生异常\n'
            for t in range(retry_time):
                try:
                    fun_res = fun(*args, **kwargs)
                except Exception as e:
                    if t == retry_time - 1:
                        # 重试失败
                        if return_msg:
                            msg += f'MESSAGE: {return_msg}\n'
                        if show_params:
                            msg += f'PARAMS: {args}  {kwargs}\n'
                        logger.exception(msg)
                        if custom_return[0]:
                            return custom_return[1]
                        else:
                            raise AssertionError(e)
                    else:
                        if show_process:
                            logger.warning(f'函数: {fun.__name__} 发生异常，第{t + 1}次重试')
                        if sleep_time:
                            time.sleep(sleep_time)

                else:
                    return fun_res

        return retry_handle
