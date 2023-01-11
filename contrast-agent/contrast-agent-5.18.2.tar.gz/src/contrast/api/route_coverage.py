# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.extern import structlog as logging

logger = logging.getLogger("contrast")


class Route(object):
    """
    Route object used for various TS messages
    """

    def __init__(self, verb, url, route):
        self.verb = verb or "GET"
        self.url = url or ""
        self.signature = route or ""
        self.sources = []

    def to_json_inventory(self):
        """json representation used in v1.0 ApplicationInventory.routes"""
        return {
            "signature": self.signature,
            "verb": self.verb,
            "url": self.url,
        }

    def to_json_traces(self):
        """json representation used in ng Traces.routes"""
        return {
            # "The number of times this route was observed; must be more than 0"
            "count": 1,
            "observations": [{"url": self.url, "verb": self.verb}],
            "signature": self.signature,
        }
