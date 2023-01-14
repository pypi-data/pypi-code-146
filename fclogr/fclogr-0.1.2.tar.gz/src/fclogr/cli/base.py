# SPDX-FileCopyrightText: 2023 Maxwell G <gotmax@e.email>
#
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import annotations

import abc
import argparse
import logging
from collections.abc import Callable

fmt = "{levelname}:{name}: {message}"
logging.basicConfig(format=fmt, style="{")
LOG = logging.getLogger("fclogr")


class InvalidArgumentError(Exception):
    """
    A problem parsing or validating a command line argument
    """


class Command(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def make_parser(
        cls, parser_func: Callable = argparse.ArgumentParser, standalone=False, **kwargs
    ):
        ...

    @abc.abstractmethod
    def run(self):
        ...
