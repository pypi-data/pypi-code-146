# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at http://www.comet.ml
#  Copyright (C) 2021 Comet ML INC
#  This file can not be copied and/or distributed without the express
#  permission of Comet ML Inc.
# *******************************************************

__author__ = """Comet ML Inc."""
__email__ = "mail@comet.ml"
__version__ = "0.3.2b0"
__all__ = ["CometMPM"]

from ._logging import _setup_comet_mpm_logging
from .comet_mpm import CometMPM

_setup_comet_mpm_logging()
