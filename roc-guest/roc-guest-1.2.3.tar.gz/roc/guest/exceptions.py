#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""GUEST plugin exceptions."""

__all__ = ['GuestException',
           'ParseTestXmlError',
           'ClearTestError',
            'GuestNoInputError',
           'MebDbTransactionError',
           'RocDbTransactionError']


class GuestException(Exception):
    """
    Guest main exception
    """

class ParseTestXmlError(Exception):
    """
    Errors for parsing xml test for guest module
    """

class ClearTestError(Exception):
    """
    Errors for clearing test for guest module
    """

class GuestNoInputError(Exception):
    """
    Errors for No input for guest module
    """

class MebDbTransactionError(Exception):
    """
    Errors with MEB DB transaction
    """

class RocDbTransactionError(Exception):
    """
    Errors with ROC DB transaction
    """
