#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging.handlers
import os
import datetime


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

log_directory_path = os.getcwd() + '/logs'
if not os.path.exists(log_directory_path):
    os.makedirs(log_directory_path)

now = datetime.datetime.now()
date_str = datetime.datetime.strftime(now, '%Y-%m-%d')
log_file = (str(log_directory_path) + '/' + date_str + '.log')


rf_handler = logging.handlers.TimedRotatingFileHandler(str(log_directory_path) + '/' + 'sp.log',
                                                       when='midnight',
                                                       interval=1,
                                                       backupCount=7,
                                                       atTime=datetime.time(0, 0, 0, 0)
                                                       )
rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

s_handler = logging.StreamHandler()
f_handler = logging.FileHandler(log_file)
s_handler.setLevel(logging.DEBUG)
f_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
s_handler.setFormatter(formatter)
f_handler.setFormatter(formatter)
logger.addHandler(s_handler)
logger.addHandler(rf_handler)


def debug(msg):
    logger.debug('=====> ' + str(msg))


def info(msg):
    logger.info('=====> ' + str(msg))


def warning(msg):
    logger.warning('=====> ' + str(msg))


def error(msg):
    logger.error('=====> ' + str(msg))


if __name__ == '__main__':
    debug('logging')
    info('logging')
    warning('logging')
    error('logging')
