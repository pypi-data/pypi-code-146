#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Exception definition for roc.idb plugin.
"""

from poppy.core.logger import logger

__all__ = ['NoIdbFound', 'MultipleIdbFound', 'IdbQueryError', 'IdbUpdateError']


class NoIdbFound(Exception):
    """Exception raised if an IDB release is not found in the database."""

    def __init__(self, message, *args, **kwargs):
        super(NoIdbFound, self).__init__(*args, **kwargs)
        logger.error(message)
        self.message = message

    pass


class MultipleIdbFound(Exception):
    """Exception raised if an IDB release is found more than one time in the database."""

    def __init__(self, message, *args, **kwargs):
        super(MultipleIdbFound, self).__init__(*args, **kwargs)
        logger.error(message)
        self.message = message


class IdbQueryError(Exception):
    """Exception raised if an IDB query has failed."""

    def __init__(self, message, *args, **kwargs):
        super(IdbQueryError, self).__init__(*args, **kwargs)
        logger.error(message)
        self.message = message


class IdbUpdateError(Exception):
    """Exception raised if an IDB update has failed."""

    def __init__(self, message, *args, **kwargs):
        super(IdbUpdateError, self).__init__(*args, **kwargs)
        logger.error(message)
        self.message = message


class SetTrangeIdbReleaseError(Exception):
    pass
