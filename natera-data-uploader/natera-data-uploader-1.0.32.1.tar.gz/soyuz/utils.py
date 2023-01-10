#!/usr/bin/env python

import logging
import logging.config
import os
import re
import sys
import time

import jwt

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

MEASURED_TIME_LOG = "/tmp/measured_time.log"
SAMPLE_SIZE = 10


def get_instrument_type_from_name(instrument_name):
    if instrument_name.startswith("M"):
        return "MISEQ"
    if instrument_name.startswith("SN") \
            or instrument_name.startswith("D") \
            or instrument_name.startswith("L") \
            or instrument_name[0].isdigit() \
            or instrument_name.startswith("HSQ"):
        return "HISEQ"
    if instrument_name.startswith("K"):
        return "HISEQ4k"
    if instrument_name.startswith("HW"):
        return "GAIIX"
    if instrument_name.startswith("NS") \
            or instrument_name.startswith("NB") \
            or instrument_name.startswith("NDX"):
        return "NEXTSEQ"
    return None


def get_expected_time(class_name, func_name):
    if not os.path.isfile(MEASURED_TIME_LOG):
        return None
    times = []
    with open(MEASURED_TIME_LOG) as f:
        for line in f.readlines():
            if line.startswith("{} {} ".format(class_name, func_name)):
                times.append(int(line.lstrip("{} {} ".format(class_name, func_name))))
    result = times[-SAMPLE_SIZE:]
    return None if len(result) == 0 else int(round(sum(result)/float(len(result))))


def set_measured_time(class_name, func_name, measured_time):
    with open(MEASURED_TIME_LOG, 'a') as f:
        f.write("{} {} {}\n".format(class_name, func_name, measured_time))


def timeit(func):
    def timed(self, seq_folder):
        class_name = self.__class__.__name__
        func_name = func.__name__
        ts = time.time()
        result = func(self, seq_folder)
        te = time.time()
        measured_time = int(round(te - ts))
        set_measured_time(class_name, func_name, measured_time)
        return result
    return timed


def read_in_chunks(file_object, chunk_size=65536):
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


class _ExcludeErrorsFilter(logging.Filter):
    def filter(self, record):
        """Filters out log messages with log level ERROR (numeric value: 40) or higher."""
        return record.levelno < 40


class Logging(object):
    config = {
        'version': 1,
        'filters': {
            'exclude_errors': {
                '()': _ExcludeErrorsFilter
            }
        },
        'formatters': {
            'include_process': {
                'format': '(%(process)d) %(asctime)s %(name)s (line %(lineno)s) | %(asctime)s %(levelname)-8s %(message)s'
            }
        },
        'handlers': {
            'console_stderr': {
                # Sends log messages with log level ERROR or higher to stderr
                'class': 'logging.StreamHandler',
                'level': 'ERROR',
                'formatter': 'include_process',
                'stream': sys.stderr
            },
            'console_stdout': {
                # Sends log messages with log level lower than ERROR to stdout
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'include_process',
                'filters': ['exclude_errors'],
                'stream': sys.stdout
            },
            'file': {
                # Sends all log messages to a file
                'class': 'logging.FileHandler',
                'level': 'DEBUG',
                'formatter': 'include_process',
                'filename': 'uploader.log',
                'encoding': 'utf8'
            }
        },
        'root': {
            # In general, this should be kept at 'NOTSET'.
            # Otherwise it would interfere with the log levels set for each handler.
            'level': 'NOTSET',
            'handlers': ['console_stderr', 'console_stdout', 'file']
        },
    }

    def get_log_file(self):
        return self.config["handlers"]["file"]["filename"]

    def set_log_file(self, log_file_path):
        self.config["handlers"]["file"]["filename"] = log_file_path

    def initialize(self):
        logging.config.dictConfig(self.config)


class UploaderException(BaseException):
    pass


class FolderAlreadyExistsException(UploaderException):
    pass


class NotValidFolderException(UploaderException):
    pass


def parse_and_validate_jwt_token(jwt_token, public_key_path):
    # type: (str, str) -> dict

    if not re.match('^(eyJhbGci[a-zA-Z0-9_-]+)\\.([a-zA-Z0-9_-]+)\\.([a-zA-Z0-9_-]+)$', jwt_token):
        raise UploaderException('Provide correct JWT token')

    with open(public_key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )

    try:
        return jwt.decode(jwt_token, public_key)
    except Exception:
        raise UploaderException('JWT token has not been verified: {}'.format(jwt_token))


def stoppable_sleep(wait_time, wake_up_condition, interval=5):
    # type: (float, callable, int) -> None

    logging.info("Waiting for {} seconds".format(wait_time))

    for _ in range(0, int(wait_time / interval)):
        if wake_up_condition():
            break

        time.sleep(interval)
