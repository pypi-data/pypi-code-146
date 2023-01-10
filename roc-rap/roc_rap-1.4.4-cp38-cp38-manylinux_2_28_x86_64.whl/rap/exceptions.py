#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Exceptions definition for RAP plugin.
"""

from poppy.core.logger import logger

__all__ = ['MetadataException']

class MetadataException(Exception):
    """Exception raise if issue with metadata."""
    def __init__(self, message, *args, **kwargs):
        super(MetadataException, self).__init__(*args, **kwargs)
        logger.error(message)
        self.message = message