# SPDX-License-Identifier: MIT
# Copyright (c) 2023 David Lechner <david@lechnology.com>

import re
from importlib.metadata import version

__version__ = re.sub(r"\.post\d+", "", version(__name__))

del version
del re
