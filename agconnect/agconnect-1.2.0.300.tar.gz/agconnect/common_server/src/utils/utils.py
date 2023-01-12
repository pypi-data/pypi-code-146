# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

import os
import re

from agconnect.common_server.src.error.error import AGCException
from agconnect.common_server.src.error.error_message import ErrorCodeConstant
from agconnect.common_server.src.log_config.common_log import logger


def url_validate(url):
    logger.info('step into method urlValidate')
    _reg_default = r"^(ht)tp(s?)\:\/\/[0-9a-zA-Z]([-.\w]*[0-9a-zA-Z])*(:(0-9)*)*" \
                   r"(\/?)([a-zA-Z0-9\-\.\?\,\'\/\\\+&amp;%\$#_]*)?"
    s_reg = r"/\s/g"
    if re.match(s_reg, url):
        return False
    return regx(url, _reg_default)


def regx(url, reg):
    if len(reg) == 0:
        raise AGCException(ErrorCodeConstant.URL_VALIDATE_FAIL + ", RegEx pattern does not exist.")
    if re.match(reg, url):
        logger.info("step into method reg match in regx")
        return True
    return False


def validate_path(file_path):
    if not file_path:
        raise AGCException(ErrorCodeConstant.FILE_NOT_EXIST)
    if not os.path.exists(file_path):
        raise AGCException(ErrorCodeConstant.FILE_NOT_EXIST)
    import stat
    lstat_result = os.stat(file_path)
    if not stat.S_ISREG(lstat_result.st_mode):
        raise AGCException(ErrorCodeConstant.NOT_A_FILE)
    try:
        os.access(file_path, os.R_OK)
    except Exception as e:
        raise AGCException(ErrorCodeConstant.FILE_NO_READ_PERMISSION) from e
    return True


def add_headers(args_1: dict, args_2: dict) -> dict:
    logger.info("step into method addHeaders")
    args_1.update(args_2)
    return args_1


def default_to_json(obj):
    if hasattr(obj, 'to_json'):
        return obj.to_json()
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')
