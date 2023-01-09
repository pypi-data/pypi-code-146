#
# Copyright (c) 2020,2022 Jim Bauer <4985656-jim_bauer@users.noreply.gitlab.com>
# This software is licensed according to the included LICENSE file
# SPDX-License-Identifier: GPL-3.0-or-later
#


import logging
from logging.handlers import RotatingFileHandler


# These will be reassigned in init() and they will be functions
# used for logging messages at the corresponding level.  From other
# modules, they will be called like: logger.debug(msg)
debug = None
info = None
warning = None
error = None
critical = None

# Maps between log level string to actual level
log_level_map = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
}


def add_argparse_args(parse):
    parse.add_argument('--loglevel', default='info',
                       choices=['debug', 'info', 'warning',
                                'error', 'critical'],
                       help='log message minimum level')
    parse.add_argument('--logfile', help='path to logfile')
    parse.add_argument('--logkeep', default=1,
                       help='number of old log files to keep')
    parse.add_argument('--logmaxbytes', default=1000000,
                       help='maximum number of bytes in a log file '
                       'before rotation')


class Config:
    def __init__(self, logfile, level, keep, maxbytes):
        self.logfile = logfile
        self.level = level
        self.keep = keep
        self.maxbytes = maxbytes

    def set_from_args(self, args):
        if args is None:
            return

        self.logfile = args.logfile
        self.level = args.loglevel
        self.keep = args.logkeep
        self.maxbytes = args.logmaxbytes


def init(log_name,  logfile=None, level=logging.INFO, keep=1,
         maxbytes=1000000, args=None):
    # Initialize the logging infrastructure
    log = logging.getLogger(log_name)

    config = Config(logfile, level, keep, maxbytes)
    config.set_from_args(args)

    if isinstance(config.level, str):
        config.level = log_level_map[config.level]

    fmt = '{asctime} {levelname:5} {name}[{process}] {module}/' + \
        '{funcName}() {lineno} : {message}'
    log_formatter = logging.Formatter(fmt, style='{')

    if config.logfile:
        log_handler = RotatingFileHandler(config.logfile,
                                          maxBytes=config.maxbytes,
                                          backupCount=config.keep)

        # force rollover at startup
        #log_handler.doRollover()

        log_handler.setFormatter(log_formatter)
        log.addHandler(log_handler)
        log.info('Logging setup, log_name=%s, logfile=%s',
                 log_name, config.logfile)
    else:
        # stderr handler
        log_handler = logging.StreamHandler()
        log_handler.setFormatter(log_formatter)
        log.addHandler(log_handler)
        log.info('Logging setup to stderr')

    log.setLevel(config.level)

    global debug
    global info
    global warning
    global error
    global critical
    debug = log.debug
    info = log.info
    warning = log.warning
    error = log.error
    critical = log.critical
    return


def stop():
    logging.shutdown()
    return
