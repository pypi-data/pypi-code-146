#  Copyright (c) modalic 2022. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.

"""Custom Logger."""
import logging
import time
from typing import Dict


class CustomFormatter(logging.Formatter):
    r"""Custom formatting object."""

    faint = "\x1b[2m"
    green = "\x1b[32m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    def custom_format_str(self, color: str) -> str:
        r"""Returns a custom format string."""
        return (
            self.faint
            + "%(asctime)s.%(msecs)06dZ "
            + self.reset
            + color
            + " %(levelname)s"
            + self.reset
            + " %(message)s"
            + self.reset
        )

    def custom_format(self) -> Dict[int, str]:
        r"""."""
        return {
            logging.DEBUG: self.custom_format_str(self.yellow),
            logging.INFO: self.custom_format_str(self.green),
            logging.WARNING: self.custom_format_str(self.yellow),
            logging.ERROR: self.custom_format_str(self.red),
            logging.CRITICAL: self.custom_format_str(self.bold_red),
        }

    def format(self, record: logging.LogRecord) -> str:
        r"""."""
        log_fmt = self.custom_format().get(record.levelno)
        formatter = logging.Formatter(fmt=log_fmt, datefmt="%Y-%m-%dT%H:%M:%S")
        return formatter.format(record)


logger = logging.getLogger("modalic")

# logger configuration
logger.setLevel(level=logging.INFO)
# handler configuration
handler = logging.StreamHandler()
handler.setLevel(level=logging.INFO)
handler.setFormatter(CustomFormatter())
# adjust time settings to UTC.
logging.Formatter.converter = time.gmtime

logger.addHandler(handler)
