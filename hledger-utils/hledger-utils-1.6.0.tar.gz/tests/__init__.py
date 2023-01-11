# SPDX-FileCopyrightText: 2023 Yann Büchau <nobodyinperson@posteo.de>
# SPDX-License-Identifier: GPL-3.0-or-later

# system modules
import os
import logging

# internal modules

# external modules
from rich.logging import RichHandler
from rich.console import Console

console = Console(stderr=True)
logger = logging.getLogger(__name__)

logging.basicConfig(
    level=os.environ.get("HLEDGER_EDIT_LOGLEVEL", "CRITICAL"),
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(console=console)],
)
