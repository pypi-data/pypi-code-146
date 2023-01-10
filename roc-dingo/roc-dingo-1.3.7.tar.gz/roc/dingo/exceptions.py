#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from poppy.core.logger import logger

__all__ = ['DingoException',
           'DbInsertionError',
           'DbQueryError']


class DingoException(Exception):
    """Main exception for Dingo plugin"""
    pass


class DbInsertionError(Exception):
    """Exception raised if ROC data insertion has failed."""

    def __init__(self, message, *args, **kwargs):
        super(DbInsertionError, self).__init__(*args, **kwargs)
        logger.error(message)
        self.message = message

    #    logger_level = 'warning'
    #    use_traceback = True

    pass


class DbQueryError(Exception):
    """Exception raised if ROC data query has failed."""

    def __init__(self, message, *args, **kwargs):
        super(DbQueryError, self).__init__(*args, **kwargs)
        logger.error(message)
        self.message = message

    #    logger_level = 'warning'
    #    use_traceback = True

    pass
