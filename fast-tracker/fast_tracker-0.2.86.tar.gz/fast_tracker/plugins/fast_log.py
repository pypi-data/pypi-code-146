#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by FAST-DEV 2021/4/6
"""
import logging
from fast_tracker import Layer, ComponentType, Log, LogItem, config
from fast_tracker.trace.context import get_context
from fast_tracker.utils import functions

log_level = {"NOTSET": 0, "DEBUG": 10, "INFO": 20, "WARNING": 30, "ERROR": 40, "CRITICAL": 50}


def install():
    """
    python日志拦截器
    lib/python3.8/loggin/__init__.py中已定义日志等级:
    CRITICAL = 50
    FATAL = CRITICAL
    ERROR = 40
    WARNING = 30
    WARN = WARNING
    INFO = 20
    DEBUG = 10
    NOTSET = 0
    :return:
    """
    _handle = logging.Logger._log

    def params_tostring(msg, level):
        level_names = {v: k for k, v in log_level.items()}
        return {"err_msg": msg, "err_type": level_names.get(level, "UNKNOWN"), "err_trace": ""}

    def _fast_py38_handle(
        this: logging.Logger, level, msg, args, exc_info=None, extra=None, stack_info=False, stacklevel=1
    ):
        # 当gunicorn模式启动时，gunicorn会自行上报log信息，也会被此插件拦截，故需剔除gunicorn的log上报 eg：<Logger gunicorn.error (INFO)>
        # uwsgi 不需要拦截，因其无错误log调用
        err_log = this.__str__()
        if "gunicorn" in err_log or "kafka" in err_log or "tornado" in err_log or "werkzeug" in err_log:
            res = _handle(this, level, msg, args, exc_info=exc_info, extra=extra, stack_info=stack_info, stacklevel=stacklevel)

            return res

        if config.debug and log_level.get(config.logging_level) <= level:
            context = get_context()
            with context.new_local_span(op="Log") as span:
                span.layer = Layer.Local
                span.component = ComponentType.Log

                data = params_tostring(msg, level)
                span.logs.append(Log(items=[LogItem(key=ComponentType.Log, val=data)]))

                res = _handle(this, level, msg, args, exc_info=exc_info, extra=extra, stack_info=stack_info, stacklevel=stacklevel)

                return res
        else:
            # 当配置文件中的配置的日记级别高于当前上报日志级别，则不做探针上报，也就是说拦截器什么都不做，只负责调用日志原始处理器
            res = _handle(this, level, msg, args, exc_info=exc_info, extra=extra, stack_info=stack_info, stacklevel=stacklevel)

            return res

    def _fast_py35_handle(this: logging.Logger, level, msg, args, exc_info=None, extra=None, stack_info=None):
        # 当gunicorn模式启动时，gunicorn会自行上报log信息，也会被此插件拦截，故需剔除gunicorn的log上报 eg：<Logger gunicorn.error (INFO)>
        # uwsgi 不需要拦截，因其无错误log调用
        err_log = this.__str__()
        if "gunicorn" in err_log or "kafka" in err_log or "tornado" in err_log or "werkzeug" in err_log:
            res = _handle(this, level, msg, args, exc_info=exc_info, extra=extra, stack_info=stack_info)

            return res

        if config.debug and log_level.get(config.logging_level) <= level:
            context = get_context()
            with context.new_local_span(op="Log") as span:
                span.layer = Layer.Local
                span.component = ComponentType.Log

                data = params_tostring(msg, level)
                span.logs.append(Log(items=[LogItem(key=ComponentType.Log, val=data)]))

                res = _handle(this, level, msg, args, exc_info=exc_info, extra=extra, stack_info=stack_info)

                return res
        else:
            # 当配置文件中的配置的日记级别高于当前上报日志级别，则不做探针上报，也就是说拦截器什么都不做，只负责调用日志原始处理器
            res = _handle(this, level, msg, args, exc_info=exc_info, extra=extra, stack_info=stack_info)

            return res

    from sys import version_info

    python_version = version_info[:2]
    if python_version >= (3, 8):
        functions.log("minor python version is:%r", version_info[:2])
        logging.Logger._log = _fast_py38_handle
    else:
        functions.log("python version is:%r", version_info[:2])
        logging.Logger._log = _fast_py35_handle
