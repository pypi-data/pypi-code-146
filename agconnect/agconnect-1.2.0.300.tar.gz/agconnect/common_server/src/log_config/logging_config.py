# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

import json
import logging
import os
import time
from datetime import datetime
from logging.handlers import RotatingFileHandler

from agconnect.common_server.src.error.error import AGCException
from agconnect.common_server.src.error.error_message import ErrorCodeConstant

DEFAULT_LOG_DIR = '../logs'

DEFAULT_LOG_LEVEL = 'INFO'

DEFAULT_MAX_SIZE = '20m'

DEFAULT_MAX_FILES = '14d'

DEFAULT_PREFIX = 'common'

DEFAULT_META_INFO = 'common_server'

DEFAULT_FILE_SWITCH = 'off'

DEFAULT_CONSOLE_SWITCH = 'on'

DEFAULT_DIRECTORY = os.path.normpath(os.path.join(os.path.dirname(__file__), '../../logging_config.json'))

local_time = time.localtime()
now = datetime(local_time[0], local_time[1], local_time[2], local_time[3], local_time[4], local_time[5])
DT_STRING = now.strftime("-%m-%d-%Y-%H")


def update_config(logger_level=None, file_switch=None, console_switch=None, log_file_path=None):
    with open(DEFAULT_DIRECTORY, 'r') as file:
        data = json.load(file)
    if logger_level:
        data['logger_level'] = logger_level
    if file_switch:
        data['file_switch'] = file_switch
    if console_switch:
        data['console_switch'] = console_switch
    if log_file_path:
        data['path'] = log_file_path
    fd = os.open(DEFAULT_DIRECTORY, os.O_CREAT | os.O_WRONLY, 0o644)
    with os.fdopen(fd, 'w') as file:
        json.dump(data, file, indent=4)


def log_configuration(config_path: str) -> logging.Logger:
    logging_config = read_config_file(config_path)
    config_info = get_config_info(logging_config)
    log_directory = os.path.normpath(os.path.join(os.path.dirname(
        config_path), config_info[2]))
    try:
        os.mkdir(log_directory)
    except OSError:
        pass

    transports_config = None
    error_file = None
    log_file = None

    if config_info[0] == 'on' and isinstance(config_info[0], str):
        error_file = os.path.normpath(os.path.join(log_directory, 'error.log'))
        log_file = os.path.normpath(os.path.join(
            log_directory, config_info[1] + "{}.log".format(DT_STRING)))

    condition_1 = config_info[0] == 'on' and isinstance(config_info[0], str)
    condition_2 = config_info[8] == 'on' and isinstance(config_info[0], str)
    if condition_1 or condition_2:
        transports_config = log_transports_config(
            config_info, error_file, log_file)

    logger = create_instance(config_info=config_info, transports_config=transports_config)

    return logger


def read_config_file(config_path):
    try:
        with open(config_path, 'r') as file:
            data = json.load(file)
        logging_config = data
    except Exception as error:
        raise AGCException(ErrorCodeConstant.FS_READ_FAIL) from error
    return logging_config


def get_config_info(logging_config):
    file_switch = DEFAULT_FILE_SWITCH
    config_file_switch = logging_config['file_switch']
    if config_file_switch:
        file_switch = config_file_switch

    prefix = DEFAULT_PREFIX
    config_prefix = logging_config['file_name_prefix']
    if config_prefix:
        prefix = config_prefix

    log_dir = DEFAULT_LOG_DIR
    config_log_directory = logging_config['path']
    if config_log_directory:
        log_dir = config_log_directory

    file_log_level = DEFAULT_LOG_LEVEL
    config_file_log_level = logging_config['file_level']
    if config_file_log_level:
        file_log_level = config_file_log_level

    log_max_size = DEFAULT_MAX_SIZE
    config_log_max_size = logging_config['maxSize']
    if config_log_max_size:
        log_max_size = config_log_max_size

    log_max_files = DEFAULT_MAX_FILES
    config_log_max_files = logging_config['maxFiles']
    if config_log_max_files:
        log_max_files = config_log_max_files

    console_log_level = DEFAULT_LOG_LEVEL
    config_console_log_level = logging_config['console_level']
    if config_console_log_level:
        console_log_level = config_console_log_level

    meta_info = DEFAULT_META_INFO
    config_meta_info = logging_config['service']
    if config_meta_info:
        meta_info = config_meta_info

    console_switch = DEFAULT_CONSOLE_SWITCH
    config_console_switch = logging_config['console_switch']
    if config_console_switch:
        console_switch = config_console_switch

    logger_level = DEFAULT_LOG_LEVEL
    config_logger_level = logging_config['logger_level']
    if config_logger_level:
        logger_level = config_logger_level

    return_list = (file_switch, prefix, log_dir, file_log_level,
                   log_max_size, log_max_files, console_log_level,
                   meta_info, console_switch, logger_level)
    return return_list


def log_transports_config(config_info, error_file: str, log_file: str):
    file = None
    rotate_file = None

    if error_file:
        file = logging.FileHandler(filename=error_file, )
    if log_file:
        rotate_file = RotatingFileHandler(log_file, mode='a', maxBytes=int(config_info[4]),
                                          backupCount=int(config_info[5]), encoding=None, delay=False)

    log_transports = {
        'console_config': logging.StreamHandler(),
        'file': file,
        'rotate_file': rotate_file
    }
    print(log_transports)
    return log_transports


formatter = logging.Formatter(
    fmt='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
    datefmt='%m-%d %H:%M:%S')


def create_instance(config_info, transports_config):
    logger = logging.getLogger(__name__)
    logger.setLevel(config_info[9])
    if config_info[0] == 'on' and isinstance(config_info[0], str):
        file_handler = transports_config['file']
        file_handler.setLevel('ERROR')
        file_handler.setFormatter(formatter)

        rotate_file_handler = transports_config['rotate_file']
        rotate_file_handler.setLevel(config_info[3])
        rotate_file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(rotate_file_handler)

    if config_info[8] == 'on' and isinstance(config_info[8], str):
        console_handler = transports_config['console_config']
        console_handler.setLevel(config_info[6])
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
    return logger
