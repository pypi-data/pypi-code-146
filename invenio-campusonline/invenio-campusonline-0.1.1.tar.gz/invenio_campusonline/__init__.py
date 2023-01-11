# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Graz University of Technology.
#
# invenio-campusonline is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""This module is used to import/export from/to the CampusOnline System."""

from .api import fetch_all_ids, import_from_campusonline
from .ext import InvenioCampusonline
from .types import ThesesFilter, ThesesState

__version__ = "0.1.1"

__all__ = (
    "__version__",
    "InvenioCampusonline",
    "import_from_campusonline",
    "fetch_all_ids",
    "ThesesFilter",
    "ThesesState",
)
