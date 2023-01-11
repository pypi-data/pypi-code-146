# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import ctypes
import sys
from contrast.extern import structlog as logging
from contrast.agent import agent_lib

logger = logging.getLogger("contrast")


__all__ = [
    "get_index_of_chained_cmd",
    "does_file_path_bypass_security",
    "does_command_contain_dangerous_path",
    "initialize_semantic_analysis",
]


def initialize_semantic_analysis():
    if agent_lib.LIB_CONTRAST is None:
        return

    agent_lib.LIB_CONTRAST.does_file_path_bypass_security.argtypes = (
        ctypes.c_char_p,
        ctypes.c_char,
    )
    agent_lib.LIB_CONTRAST.get_index_of_chained_command.argtypes = [ctypes.c_char_p]
    agent_lib.LIB_CONTRAST.does_command_contain_dangerous_path.argtypes = [
        ctypes.c_char_p
    ]

    agent_lib.LIB_CONTRAST.does_file_path_bypass_security.restype = ctypes.c_char
    agent_lib.LIB_CONTRAST.get_index_of_chained_command.restype = ctypes.c_longlong
    agent_lib.LIB_CONTRAST.does_command_contain_dangerous_path.restype = ctypes.c_char


def get_index_of_chained_cmd(command: str) -> int:
    """
    @param command: str which contains the user input of the command to be executed
    @rtype int: -1 if there is no chained command or an int >=0 of the starting index
    of the chained command
    """
    if not command:
        return -1

    command = ctypes.c_char_p(bytes(command, "utf8", errors="ignore"))

    def is_valid_return(code):
        return code >= -1

    return agent_lib.call(
        agent_lib.LIB_CONTRAST.get_index_of_chained_command,
        is_valid_return,
        command,
    )


def does_file_path_bypass_security(command: str, is_custom_code: object) -> int:
    """
    @param command: str which contains the user input of the command to be executed
    @param is_custom_code: object or none that indicates if code is coming from user code
    @rtype int: 1 if there is bypass in security or an int 0 if there is no security bypass
    """
    if not command:
        return 0

    command = ctypes.c_char_p(bytes(command, "utf8", errors="ignore"))

    is_custom_code_val = "0" if is_custom_code is None else "1"
    is_custom_code = ctypes.c_char(bytes(is_custom_code_val, "utf8", errors="ignore"))

    def is_valid_return(code):
        return 0 <= int.from_bytes(code, sys.byteorder) <= 1

    return int.from_bytes(
        agent_lib.call(
            agent_lib.LIB_CONTRAST.does_file_path_bypass_security,
            is_valid_return,
            command,
            is_custom_code,
        ),
        sys.byteorder,
    )


def does_command_contain_dangerous_path(command):
    if not command:
        return 0

    command = ctypes.c_char_p(bytes(command, "utf8", errors="ignore"))

    def is_valid_return(code):
        return 0 <= int.from_bytes(code, sys.byteorder) <= 1

    return int.from_bytes(
        agent_lib.call(
            agent_lib.LIB_CONTRAST.does_command_contain_dangerous_path,
            is_valid_return,
            command,
        ),
        sys.byteorder,
    )
