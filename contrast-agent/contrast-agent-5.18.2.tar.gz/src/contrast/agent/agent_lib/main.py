# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import os.path
import ctypes
from contrast.extern import structlog as logging
from contrast.agent import agent_lib

from contrast.agent.settings import Settings
from contrast.utils.loggers import DEFAULT_LOG_PATH, DEFAULT_LOG_LEVEL
from contrast.utils.decorators import fail_loudly


logger = logging.getLogger("contrast")


__all__ = ["call", "initialize"]


def init_with_options(enable_logging: bool, log_dir: str, log_level: str):
    """
    Python translation of `init_with_options` + error handling
    """
    c_enable_logging = ctypes.c_bool(enable_logging)
    c_log_dir = ctypes.c_char_p(bytes(log_dir, "utf8"))
    c_log_level = ctypes.c_char_p(bytes(log_level, "utf8"))

    def is_valid_return(code):
        return code == 0

    call(
        agent_lib.LIB_CONTRAST.init_with_options,
        is_valid_return,
        c_enable_logging,
        c_log_dir,
        c_log_level,
    )


@fail_loudly("Failed to import agent-lib")
def _import_lib_contrast():
    """
    This import loads the shared object file. For safety (for now), we only want to do
    this if the agent-lib is actually going to be used.
    """
    if agent_lib.LIB_CONTRAST is not None:
        return

    from contrast_agent_lib import lib_contrast as lib_contrast_module

    agent_lib.LIB_CONTRAST = lib_contrast_module


def initialize():
    """
    Import and initialize agent-lib
    """
    logger.debug("Initializing agent-lib")
    _import_lib_contrast()
    agent_lib.LIB_CONTRAST.init_with_options.argtypes = [
        ctypes.c_bool,
        ctypes.c_char_p,
        ctypes.c_char_p,
    ]
    agent_lib.LIB_CONTRAST.init_with_options.restype = ctypes.c_int
    init_with_options(
        enable_logging=True,
        log_dir=_get_log_dir(),
        log_level=_get_log_level(),
    )

    agent_lib.initialize_input_tracing()
    agent_lib.initialize_semantic_analysis()


def call(c_fn, is_valid_return, *args):
    """
    Calls the provided agent-lib function with the specified positional args.

    If the function returns normally, returns the result. Otherwise, retrieves the
    corresponding error message using `last_error_message` and logs profusely.
    @param is_valid_return: function used to handle the return from the agent lib call.
        This was added because different calls to agent lib have different return codes

    This function must remain synchronous - do not use `async def`! Error handling for
    agent-lib functions must occur without another task in the same thread interrupting.
    """
    if agent_lib.LIB_CONTRAST is None:
        logger.error("Calling agent lib without initializing it first")

    fn_result = c_fn(*args)

    if is_valid_return(fn_result):
        return fn_result

    logger.debug(
        "Error from agent-lib - will retrieve error message. "
        "function: %s; args: %s; return: %s",
        c_fn.__name__,
        [getattr(a, "value", a) for a in args],
        fn_result,
    )

    # +1 prevents off-by-1 edge cases
    message_length = agent_lib.LIB_CONTRAST.last_error_message_length() + 1
    stack_length = agent_lib.LIB_CONTRAST.last_error_stack_length() + 1

    c_message_length = ctypes.c_int(message_length)
    c_stack_length = ctypes.c_int(stack_length)

    c_message_buffer = ctypes.create_string_buffer(message_length)
    c_stack_buffer = ctypes.create_string_buffer(stack_length)

    result = agent_lib.LIB_CONTRAST.last_error_message(
        c_message_buffer,
        c_message_length,
        c_stack_buffer,
        c_stack_length,
    )

    if result >= 0:
        logger.debug(
            "Error message from agent-lib: %s; stack: %s",
            c_message_buffer.value.decode("utf8"),
            c_stack_buffer.value.decode("utf8") or "<no stack info>",
        )
    else:
        logger.debug(
            "Failed to retrieve agent-lib last error message. "
            "last_error_message return: %s",
            result,
        )

    return fn_result


def _get_log_dir():
    """
    For now, use the same directory as the agent logger specified in the local config.

    TODO: PYT-2266 This should be updated when we get new log info from TS. We may also
    want to separate this logging config from the agent logger's config.
    """
    agent_log_dir = Settings().config.get("agent.logger.path") or DEFAULT_LOG_PATH
    # works even for STDOUT because of `dirname`
    return os.path.abspath(os.path.dirname(agent_log_dir))


def _get_log_level():
    """
    TODO: PYT-2266 same as log dir
    """
    return Settings().config.get("agent.logger.level", "").upper() or DEFAULT_LOG_LEVEL
