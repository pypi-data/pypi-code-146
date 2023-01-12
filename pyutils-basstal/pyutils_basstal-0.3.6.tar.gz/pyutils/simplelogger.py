import os
import logging
import pyutils.shorthand as shd

######################
######################
#       Log          #
######################
######################

ErrorRaiseExcpetion = False

logging.basicConfig(level=logging.INFO, datefmt='%y-%m-%d %H:%M:%S', format='%(message)s')
logger = logging.getLogger()


class SimpleLogger(object):
    @staticmethod
    def _color_message(message, color_code, bold=False):
        if shd.is_win():
            os.system('')
        bold_code = '\033[1m' if bold else ''
        return f'{bold_code}\033[{color_code}m{message}\033[0m'

    @staticmethod
    def _preprocess_message(message):
        if not shd.is_win():
            message = message.replace('=>', '➜').replace('<=', '✔')

        if message.endswith('\r\n') or message.endswith('\n'):
            message = message.rstrip()
        return message

    @staticmethod
    def info(message, _):
        message = SimpleLogger._preprocess_message(message)
        logger.info(message)

    @staticmethod
    def warning(message, bold=False):
        message = SimpleLogger._preprocess_message(message)
        message = SimpleLogger._color_message(message, 33, bold)
        logger.warning(message)

    @staticmethod
    def error(message, bold=False):
        if ErrorRaiseExcpetion:
            raise Exception(message)
        message = SimpleLogger._preprocess_message(message)
        message = SimpleLogger._color_message(message, 31, bold)
        logger.error(message)


def info(message, bold=False):
    SimpleLogger.info(message, bold)


def warning(message, bold=False):
    SimpleLogger.warning(message, bold)


def error(message, bold=False):
    SimpleLogger.error(message, bold)


def __hook__dispatch(assertion, original_func):
    class Restore:
        def __enter__(self):
            def real_hook_func(message, *args):
                """NOTE:ignore any parameters after 'message'

                Args:
                    message (_type_): _description_
                """
                assertion(message)
                original_func(message, *args)
            if original_func == SimpleLogger.warning:
                SimpleLogger.warning = real_hook_func
            elif original_func == SimpleLogger.info:
                SimpleLogger.info = real_hook_func
            elif original_func == SimpleLogger.error:
                SimpleLogger.error = real_hook_func

        def __exit__(self, exception_type, exception_value, traceback):
            if original_func == SimpleLogger.warning:
                SimpleLogger.warning = original_func
            elif original_func == SimpleLogger.info:
                SimpleLogger.info = original_func
            elif original_func == SimpleLogger.error:
                SimpleLogger.error = original_func
    return Restore()


def hook_info(assertion):
    """给 logger.info 加钩子以检测 info 信息是否符合预期"""
    return __hook__dispatch(assertion, SimpleLogger.info)


def hook_warning(assertion):
    """给 logger.warning 加钩子以检测 warning 信息是否符合预期

    Args:
        assertion (func(str)->None): 钩子函数

    Returns:
        class Restore: Restore class that can be used in with statement
    """
    return __hook__dispatch(assertion, SimpleLogger.warning)


def hook_error(assertion):
    """给 logger.error 加钩子

    Args:
        assertion (func(str)->None): 钩子函数

    Returns:
        class Restore: Restore class that can be used in with statement
    """
    return __hook__dispatch(assertion, SimpleLogger.error)
