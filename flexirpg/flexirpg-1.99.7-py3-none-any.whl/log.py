# FlexiRPG -- debug logging.
#
# Copyright (C) 2009 David Vrabel
# Copyright (C) 2000-2001 The OpenRPG Project
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import logging
import logging.handlers
import os.path

from orpg.config import Paths

logger = logging.getLogger("flexirpg")

def logger_setup():
    logger.setLevel(logging.DEBUG)
    handler = logging.handlers.TimedRotatingFileHandler(
        Paths.user(os.path.join("runlogs", "runlog.txt")),
        when="D", interval=1, backupCount=5)
    formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
