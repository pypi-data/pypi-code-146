#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# standard python imports


""" Rich Logging """
import logging
import os
import tempfile
from logging.handlers import TimedRotatingFileHandler

import click
from rich.logging import RichHandler
from rich.traceback import install

import exceptions.license_exception

install(suppress=[click, exceptions])


def create_logger():
    """Create a logger for use in all cases."""
    loglevel = os.environ.get("LOGLEVEL", "INFO").upper()
    rich_handler = RichHandler(rich_tracebacks=True, markup=True)
    file_handler = TimedRotatingFileHandler(
        filename=f"{tempfile.gettempdir()}{os.sep}RegScale.log",
        when="D",
        interval=3,
        backupCount=10,
    )
    logging.basicConfig(
        level=loglevel,
        format="%(asctime)s [%(levelname)-5.5s]  %(message)s",
        datefmt="[%Y/%m/%d %H:%M;%S]",
        handlers=[rich_handler, file_handler],
    )
    logger = logging.getLogger("rich")
    # logger.propagate = False
    return logger
