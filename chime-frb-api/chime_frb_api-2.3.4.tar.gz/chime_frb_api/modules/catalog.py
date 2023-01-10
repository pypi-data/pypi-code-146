#!/usr/bin/env python
"""CHIME/FRB Catalog API."""

import logging

from chime_frb_api.core import API
from chime_frb_api.core.json_type import JSON

log = logging.getLogger(__name__)


class Catalog:
    """CHIME/FRB Catalog API.

    Args:
        API : chime_frb_api.core.API class-type

    Returns:
        object-type
    """

    def __init__(self, API: API):
        """Initialize the Catalog API."""
        self.API = API

    def get_catalog(self, version) -> JSON:
        """Fetches the CHIME/FRB Catalog.

        Args:
            version: Catalog version, e.g. rn3

        Returns:
            Catalog
        """
        assert version, AttributeError(
            "catalog verison number is required. Try version=1 in the kwargs"
        )
        return self.API.get(f"/catalog/{version}")
