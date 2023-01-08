# Copyright (C) 2021,2022,2023 Kian-Meng Ang
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Common helper functions."""

import logging
import sys
from importlib import import_module
from typing import Any

logger = logging.getLogger(__name__)


def to_classname(words: str, suffix: str) -> str:
    """Generate class name from words.

    Args:
        words (str): Words to be converted
        suffix (str): The suffix name to be appended

    Returns:
        str: A class name
    """
    return words.replace("-", " ").title().replace(" ", "") + suffix


def load_class(package_name: str, class_name: str) -> Any:
    """Load class dynamically.

    Args:
        package_name (str): A package name
        class_name (str): A class name

    Returns:
        any: A loaded class
    """
    try:
        package = import_module(package_name)
        klass = getattr(package, class_name)
        logger.debug("Load module: %s.%s", package_name, class_name)
        return klass
    except AttributeError:
        logger.error("Fail to load module: %s.%s", package_name, class_name)
        sys.exit()
